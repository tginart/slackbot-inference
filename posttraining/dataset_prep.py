import os
import argparse
import torch
from datasets import load_dataset, load_from_disk, Audio


# Language mapping for dataset mode
LANG_CODE_MAP = {
    "English": "en", "English(US)": "en",
    "Chinese": "zh", "Chinese(Mandarin)": "zh",
    "Japanese": "ja",
    "Korean": "ko"
}


def _is_local_dataset(path: str) -> bool:
    """Check if the path is a local HuggingFace dataset directory."""
    if os.path.isdir(path):
        # Check for HuggingFace dataset files
        return (
            os.path.exists(os.path.join(path, "dataset_info.json")) or
            os.path.exists(os.path.join(path, "state.json")) or
            any(f.endswith(".arrow") for f in os.listdir(path))
        )
    return False


def load_and_prepare_dataset(
    dataset_name: str,
    processor,
    model,
    language_option: str = "auto",
):
    """
    Load and prepare the dataset for Whisper fine-tuning.
    
    Supports two input formats:
    1. HuggingFace Hub dataset name (e.g., "simon3000/genshin-voice")
    2. Local HuggingFace dataset path (saved with save_to_disk)
       - Raw audio format: columns (audio, context, transcription, language)
       - Pre-processed format: columns (input_features, labels)
    
    Args:
        dataset_name: HuggingFace dataset name or local path
        processor: WhisperProcessor instance
        model: WhisperForConditionalGeneration instance (can be wrapped in DataParallel)
        language_option: 'auto' for no explicit language, 'dataset' to use dataset's language per sample
    
    Returns:
        Prepared dataset with input_features and labels
    """
    print("Loading dataset and preparing data...", flush=True)
    
    # Check if this is a local dataset or a HuggingFace Hub dataset
    if _is_local_dataset(dataset_name):
        print(f"Loading local dataset from: {dataset_name}", flush=True)
        dataset = load_from_disk(dataset_name)
        
        # Check if dataset is already preprocessed (has input_features and labels)
        if "input_features" in dataset.column_names and "labels" in dataset.column_names:
            print("Dataset is already preprocessed (has input_features and labels).", flush=True)
            print(f"Loaded {len(dataset)} samples.", flush=True)
            return dataset
        
        # Otherwise, it's a raw audio dataset that needs processing
        print(f"Raw audio dataset detected. Columns: {dataset.column_names}", flush=True)
    else:
        print(f"Loading dataset from HuggingFace Hub: {dataset_name}", flush=True)
        dataset = load_dataset(dataset_name, split="train", streaming=False)

    # Determine number of workers (use SLURM allocation if available)
    num_workers = int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count() // 2 or 1))

    # Filter out entries with empty or missing transcription
    if "transcription" in dataset.column_names:
        print(f"Filtering {len(dataset)} samples using {num_workers} workers...", flush=True)
        dataset = dataset.filter(
            lambda x: x["transcription"] is not None and x["transcription"] != "",
            num_proc=num_workers,
            desc="Filtering",
        )
        print(f"After filtering: {len(dataset)} samples remain", flush=True)
    else:
        raise ValueError("Dataset does not contain 'transcription' field.")

    # Resample audio to 16 kHz (Whisper expects 16kHz audio)
    # Check if audio column exists and cast to Audio type
    if "audio" in dataset.column_names:
        # Check if it's already an Audio feature or needs casting
        from datasets import Audio as AudioFeature
        if not isinstance(dataset.features.get("audio"), AudioFeature):
            print("Casting audio column to Audio feature...", flush=True)
        dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

    # Get language and task token mappings from model
    lang_to_id = model.module.generation_config.lang_to_id if isinstance(model, torch.nn.DataParallel) else model.generation_config.lang_to_id
    task_to_id = model.module.generation_config.task_to_id if isinstance(model, torch.nn.DataParallel) else model.generation_config.task_to_id
    transcribe_token_id = task_to_id.get("transcribe", None)
    
    # Get startofprev token id for context handling
    startofprev_id = processor.tokenizer.convert_tokens_to_ids("<|startofprev|>")
    if startofprev_id is None:
        raise ValueError("Could not find <|startofprev|> token in tokenizer vocabulary.")

    # Extract bos_id and eos_id BEFORE creating closure to avoid capturing model
    bos_id_precomputed = model.module.config.decoder_start_token_id if isinstance(model, torch.nn.DataParallel) else model.config.decoder_start_token_id
    eos_id_precomputed = processor.tokenizer.eos_token_id

    # Create the prepare function with closure over required variables
    def prepare_dataset(batch):
        """Process each dataset entry: compute features and encode labels."""
        audio = batch["audio"]
        # Compute log-Mel spectrogram features from the audio
        batch["input_features"] = processor.feature_extractor(
            audio["array"], sampling_rate=audio["sampling_rate"]
        ).input_features[0]
        
        text = batch["transcription"]
        
        # Handle context field (optional)
        context = batch.get("context")
        if context and context.strip():
            context_ids = processor.tokenizer(context, add_special_tokens=False).input_ids
            prefix = [startofprev_id] + context_ids
        else:
            prefix = []
        
        if language_option == "dataset":
            # Determine language code for this sample
            lang_str = batch.get("language") or batch.get("language_name") or batch.get("locale")
            if lang_str is None or lang_str.lower() == "auto":
                # Fall back to auto mode for this sample
                if prefix:
                    text_ids = processor.tokenizer(text, add_special_tokens=False).input_ids
                    standard_ids = processor.tokenizer(text).input_ids
                    batch["labels"] = prefix + standard_ids
                else:
                    batch["labels"] = processor.tokenizer(text).input_ids
                return batch
            
            # Map to standardized code if needed
            if lang_str in LANG_CODE_MAP:
                lang_code = LANG_CODE_MAP[lang_str]
            else:
                lang_code = lang_str.lower()[:2]
            
            if f"<|{lang_code}|>" not in lang_to_id:
                raise ValueError(f"Language code '{lang_code}' not recognized by model.")
            lang_token_id = lang_to_id[f"<|{lang_code}|>"]
            
            # Encode text without special tokens
            text_ids = processor.tokenizer(text, add_special_tokens=False).input_ids
            
            # Construct full label sequence: [<|startofprev|> context...] <start_of_transcript> <language> <task> ... text ... <end_of_transcript>
            # Use precomputed values instead of accessing model inside closure
            bos_id = bos_id_precomputed
            eos_id = eos_id_precomputed
            
            if bos_id is None or eos_id is None or transcribe_token_id is None:
                raise ValueError("Special token ids not properly loaded from model config.")
            
            batch["labels"] = prefix + [bos_id, lang_token_id, transcribe_token_id] + text_ids + [eos_id]
        else:
            # Auto mode: tokenize text, then prepend context if present
            if prefix:
                # Tokenize text without special tokens to manually construct sequence
                text_ids = processor.tokenizer(text, add_special_tokens=False).input_ids
                # Get the standard sequence from tokenizer (includes bos, lang, task, eos)
                standard_ids = processor.tokenizer(text).input_ids
                # Insert context prefix after bos but before the rest
                # Standard format is: [bos, lang?, task?, ...text..., eos]
                # With context: [prefix..., bos, lang?, task?, ...text..., eos]
                # For auto mode, we prepend the context prefix to the standard tokenized sequence
                batch["labels"] = prefix + standard_ids
            else:
                # No context, use standard tokenization
                batch["labels"] = processor.tokenizer(text).input_ids
        
        return batch

    # Apply preprocessing to dataset
    # WORKAROUND: Disable multiprocessing for map to avoid fork-related deadlocks
    # with numpy/librosa/feature_extractor (even without CUDA)
    # For small datasets this is acceptable; for large datasets consider using spawn
    map_workers = None  # Single process mode
    total_samples = len(dataset)
    print(f"Processing {total_samples} samples (single-process mode to avoid fork issues)...", flush=True)
    
    # Process first sample to check for errors
    print("Testing with first sample...", flush=True)
    try:
        test_result = prepare_dataset(dataset[0])
        print(f"Test successful! Features shape: {len(test_result['input_features'])}, Labels: {len(test_result['labels'])} tokens", flush=True)
    except Exception as e:
        print(f"ERROR processing first sample: {e}", flush=True)
        raise
    
    print("Starting full processing...", flush=True)
    dataset = dataset.map(
        prepare_dataset,
        remove_columns=dataset.column_names,
        num_proc=map_workers,
        desc="Processing audio",
        load_from_cache_file=False,
    )
    print(f"Processing complete!", flush=True)
    
    return dataset


def create_collate_fn(processor):
    """
    Create a collate function for the DataLoader.
    
    Args:
        processor: WhisperProcessor instance
    
    Returns:
        Collate function for batching
    """
    def collate_fn(features):
        """Collate function to pad inputs and labels in a batch."""
        # Stack input_features (already 2D tensors of identical shape due to Whisper 30s padding)
        input_features = [torch.tensor(f["input_features"], dtype=torch.float32) for f in features]
        input_features = torch.stack(input_features)
        
        # Pad labels to the max length in this batch
        label_lists = [f["labels"] for f in features]
        max_len = max(len(l) for l in label_lists)
        
        padded_labels = []
        pad_id = processor.tokenizer.pad_token_id if processor.tokenizer.pad_token_id is not None else processor.tokenizer.eos_token_id
        
        for labels in label_lists:
            padded = labels + [pad_id] * (max_len - len(labels))
            padded_labels.append(padded)
        
        labels_tensor = torch.tensor(padded_labels, dtype=torch.long)
        
        # Replace padding token ids with -100 so they are ignored in loss computation
        if processor.tokenizer.pad_token_id is not None:
            labels_tensor[labels_tensor == processor.tokenizer.pad_token_id] = -100
        else:
            labels_tensor[labels_tensor == processor.tokenizer.eos_token_id] = -100
        
        return {"input_features": input_features, "labels": labels_tensor}
    
    return collate_fn


if __name__ == "__main__":
    from transformers import WhisperForConditionalGeneration, WhisperProcessor

    parser = argparse.ArgumentParser(description="Download and prepare dataset for Whisper fine-tuning")
    parser.add_argument("--model_id", type=str, default="openai/whisper-large-v3-turbo",
                        help="Hugging Face model name or path for Whisper (needed for tokenization).")
    parser.add_argument("--dataset_name", type=str, default="simon3000/genshin-voice",
                        help="Dataset name on HuggingFace Hub.")
    parser.add_argument("--language_option", choices=["auto", "dataset"], default="auto",
                        help="How to handle language tokens: 'auto' for no explicit language, 'dataset' to use dataset's language per sample.")
    parser.add_argument("--output_path", type=str, default="prepared_dataset",
                        help="Path to save the prepared dataset.")
    args = parser.parse_args()

    print(f"Loading model and processor from {args.model_id}...", flush=True)
    model = WhisperForConditionalGeneration.from_pretrained(args.model_id)
    
    if args.language_option == "auto":
        processor = WhisperProcessor.from_pretrained(args.model_id, task="transcribe")
    else:
        processor = WhisperProcessor.from_pretrained(args.model_id, task="transcribe", language="auto")

    # Prepare the dataset
    dataset = load_and_prepare_dataset(
        dataset_name=args.dataset_name,
        processor=processor,
        model=model,
        language_option=args.language_option,
    )

    # Save to disk
    print(f"Saving prepared dataset to {args.output_path}...")
    dataset.save_to_disk(args.output_path)
    print(f"Done! Dataset saved to {args.output_path}")
    print(f"To load later: dataset = load_from_disk('{args.output_path}')")
