#!/usr/bin/env python3
"""
Whisper Checkpoint Evaluation Script

Evaluates a fine-tuned Whisper checkpoint against a HuggingFace dataset,
computing Word Error Rate (WER) and Character Error Rate (CER).

Usage:
    python evaluate_checkpoint.py \
        --dataset_path ~/slackbot-inference/tts_out/hf_dataset \
        --checkpoint_path /path/to/checkpoint \
        --output_file results.json

    # Use base model (no checkpoint):
    python evaluate_checkpoint.py \
        --dataset_path ~/slackbot-inference/tts_out/hf_dataset \
        --model_id openai/whisper-large-v3-turbo \
        --output_file baseline_results.json

    # Limit samples for quick testing:
    python evaluate_checkpoint.py \
        --dataset_path ~/slackbot-inference/tts_out/hf_dataset \
        --checkpoint_path /path/to/checkpoint \
        --max_samples 50
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

import torch
import numpy as np
from tqdm import tqdm
from datasets import load_from_disk, Audio
from transformers import WhisperProcessor, WhisperForConditionalGeneration


def compute_wer(reference: str, hypothesis: str) -> float:
    """
    Compute Word Error Rate between reference and hypothesis.
    WER = (S + D + I) / N where S=substitutions, D=deletions, I=insertions, N=words in reference
    """
    ref_words = reference.lower().split()
    hyp_words = hypothesis.lower().split()
    
    # Handle edge cases
    if len(ref_words) == 0:
        return 0.0 if len(hyp_words) == 0 else 1.0
    
    # Dynamic programming for edit distance
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
    
    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j
    
    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i-1] == hyp_words[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + 1,      # deletion
                    d[i][j-1] + 1,      # insertion
                    d[i-1][j-1] + 1     # substitution
                )
    
    return d[len(ref_words)][len(hyp_words)] / len(ref_words)


def compute_cer(reference: str, hypothesis: str) -> float:
    """
    Compute Character Error Rate between reference and hypothesis.
    """
    ref_chars = list(reference.lower())
    hyp_chars = list(hypothesis.lower())
    
    if len(ref_chars) == 0:
        return 0.0 if len(hyp_chars) == 0 else 1.0
    
    d = [[0] * (len(hyp_chars) + 1) for _ in range(len(ref_chars) + 1)]
    
    for i in range(len(ref_chars) + 1):
        d[i][0] = i
    for j in range(len(hyp_chars) + 1):
        d[0][j] = j
    
    for i in range(1, len(ref_chars) + 1):
        for j in range(1, len(hyp_chars) + 1):
            if ref_chars[i-1] == hyp_chars[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + 1,
                    d[i][j-1] + 1,
                    d[i-1][j-1] + 1
                )
    
    return d[len(ref_chars)][len(hyp_chars)] / len(ref_chars)


def load_model(
    model_id: str,
    checkpoint_path: Optional[str] = None,
    device: str = "cuda",
    dtype: torch.dtype = torch.float16
) -> tuple:
    """
    Load Whisper model and processor.
    
    Args:
        model_id: Base model ID (e.g., "openai/whisper-large-v3-turbo")
        checkpoint_path: Optional path to fine-tuned checkpoint (.pt file or HuggingFace directory)
        device: Device to load model on
        dtype: Model dtype
    
    Returns:
        (model, processor)
    """
    print(f"Loading processor from {model_id}...")
    processor = WhisperProcessor.from_pretrained(model_id)
    
    if checkpoint_path:
        # Check if checkpoint_path is a .pt file (PyTorch state dict) or a directory
        actual_checkpoint_file = None
        
        if os.path.isfile(checkpoint_path) and checkpoint_path.endswith('.pt'):
            actual_checkpoint_file = checkpoint_path
        elif os.path.isdir(checkpoint_path):
            # Look for checkpoint files in the directory (prefer final, then last, then any .pt)
            preferred_files = [
                os.path.join(checkpoint_path, "checkpoint_final.pt"),
                os.path.join(checkpoint_path, "checkpoint_last.pt"),
            ]
            
            # Try preferred files first
            for ckpt_file in preferred_files:
                if os.path.isfile(ckpt_file):
                    actual_checkpoint_file = ckpt_file
                    break
            
            # If no preferred file found, look for any .pt file
            if actual_checkpoint_file is None:
                try:
                    for f in os.listdir(checkpoint_path):
                        if f.endswith('.pt'):
                            actual_checkpoint_file = os.path.join(checkpoint_path, f)
                            break
                except OSError:
                    pass
            
            if actual_checkpoint_file is None:
                # No .pt file found, try loading as HuggingFace model directory
                print(f"No .pt checkpoint file found in {checkpoint_path}, trying HuggingFace format...")
                try:
                    model = WhisperForConditionalGeneration.from_pretrained(
                        checkpoint_path,
                        dtype=dtype
                    )
                    model.config.forced_decoder_ids = None
                    model.to(device)
                    model.eval()
                    return model, processor
                except Exception as e:
                    raise ValueError(
                        f"Could not load checkpoint from {checkpoint_path}. "
                        f"Expected a .pt file or HuggingFace model directory. Error: {e}"
                    )
        
        if actual_checkpoint_file:
            # Load base model first, then load state dict
            print(f"Loading base model: {model_id}")
            model = WhisperForConditionalGeneration.from_pretrained(
                model_id,
                dtype=dtype
            )
            print(f"Loading checkpoint state dict from: {actual_checkpoint_file}")
            checkpoint = torch.load(actual_checkpoint_file, map_location=device)
            
            # Handle both formats: direct state_dict or wrapped in "model_state"
            state_dict = checkpoint.get("model_state", checkpoint)
            
            # Handle DataParallel keys (remove "module." prefix if present)
            if any(k.startswith("module.") for k in state_dict.keys()):
                state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
            
            model.load_state_dict(state_dict, strict=False)
            print("Checkpoint loaded successfully")
        else:
            raise ValueError(f"Checkpoint path must be a .pt file or directory containing .pt files: {checkpoint_path}")
    else:
        print(f"Loading base model: {model_id}")
        model = WhisperForConditionalGeneration.from_pretrained(
            model_id,
            dtype=dtype
        )
    
    model.config.forced_decoder_ids = None
    model.to(device)
    model.eval()
    
    return model, processor


def transcribe_sample(
    model,
    processor,
    audio_array: np.ndarray,
    sampling_rate: int,
    context: Optional[str] = None,
    language: Optional[str] = None,
    device: str = "cuda",
    dtype: torch.dtype = torch.float16
) -> str:
    """
    Transcribe a single audio sample.
    """
    # Preprocess audio
    inputs = processor(audio_array, sampling_rate=sampling_rate, return_tensors="pt")
    input_features = inputs.input_features.to(device)
    
    # Build generation kwargs
    generate_kwargs = {
        "do_sample": False,
        "num_beams": 1,
        "temperature": 0.0,
    }
    
    # Add context/prompt if provided
    if context is not None and context.strip():
        prompt_ids = processor.get_prompt_ids(context, return_tensors="pt").to(device)
        generate_kwargs["prompt_ids"] = prompt_ids
    
    # Add language forcing if provided
    if language is not None and language.strip():
        forced_decoder_ids = processor.get_decoder_prompt_ids(
            language=language.strip().lower(),
            task="transcribe"
        )
        generate_kwargs["forced_decoder_ids"] = forced_decoder_ids
    
    # Generate
    with torch.inference_mode(), torch.autocast(device_type="cuda", dtype=dtype):
        predicted_ids = model.generate(input_features, **generate_kwargs)
    
    # Decode
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription


def evaluate_dataset(
    dataset_path: str,
    model_id: str = "openai/whisper-large-v3-turbo",
    checkpoint_path: Optional[str] = None,
    max_samples: Optional[int] = None,
    use_context: bool = False,
    use_language: bool = False,
    include_default_reference: bool = False,
    include_context_variants: bool = False,
    device: str = "cuda",
    show_samples: int = 10,
) -> Dict[str, Any]:
    """
    Evaluate a Whisper model/checkpoint on a dataset.
    
    Args:
        dataset_path: Path to HuggingFace dataset
        model_id: Base model ID
        checkpoint_path: Optional path to fine-tuned checkpoint
        max_samples: Limit number of samples to evaluate
        use_context: Whether to use context field for conditioning
        use_language: Whether to force language from dataset
        include_default_reference: If True, also run base model (ignoring context) as reference
        include_context_variants: If True, also capture transcriptions with/without context when available
        device: Device to run on
        show_samples: Number of sample comparisons to display
    
    Returns:
        Dictionary with evaluation results
    """
    # Load dataset
    print(f"Loading dataset from {dataset_path}...")
    dataset = load_from_disk(dataset_path)
    
    # Cast audio column to proper format
    dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
    
    total_samples = len(dataset)
    if max_samples is not None:
        total_samples = min(max_samples, len(dataset))
    
    print(f"Evaluating {total_samples} samples...")
    
    # Load model
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    model, processor = load_model(model_id, checkpoint_path, device, dtype)
    
    # Load base model for default reference if requested
    base_model = None
    base_processor = None
    if include_default_reference and checkpoint_path:
        print("Loading base model for default reference comparison...")
        base_model, base_processor = load_model(model_id, None, device, dtype)
        # Warmup base model
        dummy_audio = np.zeros(16000, dtype=np.float32)
        _ = transcribe_sample(base_model, base_processor, dummy_audio, 16000, device=device, dtype=dtype)
        torch.cuda.synchronize()
    
    # Warmup
    print("Warming up model...")
    dummy_audio = np.zeros(16000, dtype=np.float32)
    _ = transcribe_sample(model, processor, dummy_audio, 16000, device=device, dtype=dtype)
    torch.cuda.synchronize()
    
    # Evaluate
    results = []
    total_wer = 0.0
    total_cer = 0.0
    total_time = 0.0
    perfect_matches = 0
    
    # Metrics for comparison with default reference (base model)
    total_default_wer = 0.0
    total_default_cer = 0.0
    improvements_vs_default = 0
    
    print("\nRunning evaluation...")
    for i in tqdm(range(total_samples)):
        sample = dataset[i]
        
        audio = sample["audio"]
        audio_array = audio["array"]
        sampling_rate = audio["sampling_rate"]
        reference = sample["transcription"]
        
        # Always extract context and language from dataset (for storage in results)
        context_value = sample.get("context")
        language_value = sample.get("language")
        context_present = bool(context_value and str(context_value).strip())
        
        # Only use for conditioning if flags are set
        context_for_transcription = context_value if use_context else None
        language_for_transcription = language_value if use_language else None
        
        # Transcribe with main model
        if include_context_variants and context_present:
            if use_context:
                start_time = time.perf_counter()
                hypothesis = transcribe_sample(
                    model, processor, audio_array, sampling_rate,
                    context=context_for_transcription, language=language_for_transcription, device=device, dtype=dtype
                )
                inference_time = time.perf_counter() - start_time
                alternate_hypothesis = transcribe_sample(
                    model, processor, audio_array, sampling_rate,
                    context=None, language=language_for_transcription, device=device, dtype=dtype
                )
            else:
                start_time = time.perf_counter()
                hypothesis = transcribe_sample(
                    model, processor, audio_array, sampling_rate,
                    context=None, language=language_for_transcription, device=device, dtype=dtype
                )
                inference_time = time.perf_counter() - start_time
                alternate_hypothesis = transcribe_sample(
                    model, processor, audio_array, sampling_rate,
                    context=context_value, language=language_for_transcription, device=device, dtype=dtype
                )
        else:
            start_time = time.perf_counter()
            hypothesis = transcribe_sample(
                model, processor, audio_array, sampling_rate,
                context=context_for_transcription, language=language_for_transcription, device=device, dtype=dtype
            )
            inference_time = time.perf_counter() - start_time
            alternate_hypothesis = None
        
        # Compute metrics
        wer = compute_wer(reference, hypothesis)
        cer = compute_cer(reference, hypothesis)
        
        total_wer += wer
        total_cer += cer
        total_time += inference_time
        
        if reference.lower().strip() == hypothesis.lower().strip():
            perfect_matches += 1
        
        result = {
            "index": i,
            "reference": reference,
            "hypothesis": hypothesis,
            "wer": round(wer, 4),
            "cer": round(cer, 4),
            "inference_time_ms": round(inference_time * 1000, 1),
            "context": context_value,  # Always store actual context from dataset
            "language": language_value,  # Always store actual language from dataset
        }

        if include_context_variants and context_present:
            if use_context:
                result["hypothesis_with_context"] = hypothesis
                result["hypothesis_without_context"] = alternate_hypothesis
            else:
                result["hypothesis_without_context"] = hypothesis
                result["hypothesis_with_context"] = alternate_hypothesis
        
        # Run base model for default reference if requested
        if include_default_reference and base_model is not None:
            # Base model always ignores context (no conditioning)
            default_hypothesis = transcribe_sample(
                base_model, base_processor, audio_array, sampling_rate,
                context=None, language=None, device=device, dtype=dtype
            )
            base_with_context = None
            if include_context_variants and context_present:
                base_with_context = transcribe_sample(
                    base_model, base_processor, audio_array, sampling_rate,
                    context=context_value, language=None, device=device, dtype=dtype
                )
            
            default_wer = compute_wer(reference, default_hypothesis)
            default_cer = compute_cer(reference, default_hypothesis)
            
            total_default_wer += default_wer
            total_default_cer += default_cer
            
            # Compare: improvement if fine-tuned model has lower WER
            if wer < default_wer:
                improvements_vs_default += 1
            
            result["base_model"] = {
                "hypothesis": default_hypothesis,
                "wer": round(default_wer, 4),
                "cer": round(default_cer, 4),
                "wer_improvement": round(default_wer - wer, 4),  # Positive = improvement
                "cer_improvement": round(default_cer - cer, 4),  # Positive = improvement
            }
            if include_context_variants and context_present:
                result["base_model"]["hypothesis_without_context"] = default_hypothesis
                result["base_model"]["hypothesis_with_context"] = base_with_context
        
        results.append(result)
    
    # Compute aggregate metrics
    avg_wer = total_wer / total_samples
    avg_cer = total_cer / total_samples
    avg_time = total_time / total_samples
    accuracy = perfect_matches / total_samples
    
    # Compute default reference metrics if included
    default_summary = None
    if include_default_reference and base_model is not None:
        avg_default_wer = total_default_wer / total_samples
        avg_default_cer = total_default_cer / total_samples
        wer_improvement = avg_default_wer - avg_wer
        cer_improvement = avg_default_cer - avg_cer
        improvement_rate = improvements_vs_default / total_samples
        
        default_summary = {
            "avg_wer": round(avg_default_wer, 4),
            "avg_cer": round(avg_default_cer, 4),
            "wer_improvement": round(wer_improvement, 4),
            "cer_improvement": round(cer_improvement, 4),
            "improvement_rate": round(improvement_rate, 4),  # Fraction of samples improved
        }
    
    # Print summary
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"Model: {checkpoint_path or model_id}")
    print(f"Dataset: {dataset_path}")
    print(f"Samples evaluated: {total_samples}")
    print(f"Use context: {use_context}")
    print(f"Use language: {use_language}")
    print(f"Include context variants: {include_context_variants}")
    if include_default_reference:
        print(f"Base model comparison: Enabled")
    print("-" * 60)
    print(f"Average WER: {avg_wer:.4f} ({avg_wer*100:.2f}%)")
    print(f"Average CER: {avg_cer:.4f} ({avg_cer*100:.2f}%)")
    print(f"Exact match accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Perfect matches: {perfect_matches}/{total_samples}")
    print(f"Average inference time: {avg_time*1000:.1f}ms")
    print(f"Total inference time: {total_time:.1f}s")
    
    if default_summary:
        print("-" * 60)
        print("COMPARISON vs BASE MODEL (default reference):")
        print(f"  Base model WER: {default_summary['avg_wer']:.4f} ({default_summary['avg_wer']*100:.2f}%)")
        print(f"  Base model CER: {default_summary['avg_cer']:.4f} ({default_summary['avg_cer']*100:.2f}%)")
        print(f"  WER improvement: {default_summary['wer_improvement']:+.4f} ({default_summary['wer_improvement']*100:+.2f}%)")
        print(f"  CER improvement: {default_summary['cer_improvement']:+.4f} ({default_summary['cer_improvement']*100:+.2f}%)")
        print(f"  Samples improved: {improvements_vs_default}/{total_samples} ({default_summary['improvement_rate']*100:.1f}%)")
    
    print("=" * 60)
    
    # Show sample comparisons (worst WER first)
    if show_samples > 0:
        print(f"\nSample comparisons (showing {min(show_samples, len(results))} samples, sorted by WER):")
        print("-" * 60)
        
        sorted_results = sorted(results, key=lambda x: x["wer"], reverse=True)
        for result in sorted_results[:show_samples]:
            print(f"\n[Sample {result['index']}] WER={result['wer']:.2%}, CER={result['cer']:.2%}")
            print(f"  REF: {result['reference'][:100]}{'...' if len(result['reference']) > 100 else ''}")
            print(f"  HYP: {result['hypothesis'][:100]}{'...' if len(result['hypothesis']) > 100 else ''}")
            if "hypothesis_with_context" in result and "hypothesis_without_context" in result:
                print(f"  HYP (ctx): {result['hypothesis_with_context'][:100]}{'...' if len(result['hypothesis_with_context']) > 100 else ''}")
                print(f"  HYP (no ctx): {result['hypothesis_without_context'][:100]}{'...' if len(result['hypothesis_without_context']) > 100 else ''}")
            if "base_model" in result:
                base_ref = result["base_model"]
                print(f"  BASE: {base_ref['hypothesis'][:100]}{'...' if len(base_ref['hypothesis']) > 100 else ''}")
                if "hypothesis_with_context" in base_ref and "hypothesis_without_context" in base_ref:
                    print(f"  BASE (ctx): {base_ref['hypothesis_with_context'][:100]}{'...' if len(base_ref['hypothesis_with_context']) > 100 else ''}")
                    print(f"  BASE (no ctx): {base_ref['hypothesis_without_context'][:100]}{'...' if len(base_ref['hypothesis_without_context']) > 100 else ''}")
                print(f"       (WER={base_ref['wer']:.2%}, improvement={base_ref['wer_improvement']:+.4f})")
            if result['context']:
                print(f"  CTX: {result['context'][:50]}{'...' if len(result['context']) > 50 else ''}")
    
    # Return full results
    summary = {
        "model": checkpoint_path or model_id,
        "dataset": dataset_path,
        "total_samples": total_samples,
        "use_context": use_context,
        "use_language": use_language,
        "include_context_variants": include_context_variants,
        "avg_wer": round(avg_wer, 4),
        "avg_cer": round(avg_cer, 4),
        "exact_match_accuracy": round(accuracy, 4),
        "perfect_matches": perfect_matches,
        "avg_inference_time_ms": round(avg_time * 1000, 1),
        "total_inference_time_s": round(total_time, 1),
    }
    
    if default_summary:
        summary["base_model"] = default_summary
    
    return {
        "summary": summary,
        "samples": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate Whisper checkpoint against a dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate checkpoint:
  python evaluate_checkpoint.py \\
      --dataset_path ~/slackbot-inference/tts_out/hf_dataset \\
      --checkpoint_path /path/to/whisper-finetune-337

  # Evaluate base model (no fine-tuning):
  python evaluate_checkpoint.py \\
      --dataset_path ~/slackbot-inference/tts_out/hf_dataset \\
      --model_id openai/whisper-large-v3-turbo

  # Quick test with limited samples:
  python evaluate_checkpoint.py \\
      --dataset_path ~/slackbot-inference/tts_out/hf_dataset \\
      --checkpoint_path /path/to/checkpoint \\
      --max_samples 20

  # Use context and language from dataset:
  python evaluate_checkpoint.py \\
      --dataset_path ~/slackbot-inference/tts_out/hf_dataset \\
      --checkpoint_path /path/to/checkpoint \\
      --use_context --use_language

  # Compare fine-tuned model vs base model (default reference):
  python evaluate_checkpoint.py \\
      --dataset_path ~/slackbot-inference/tts_out/hf_dataset \\
      --checkpoint_path /path/to/checkpoint \\
      --include_default_reference

  # Include both context/no-context completions when context is available:
  python evaluate_checkpoint.py \\
      --dataset_path ~/slackbot-inference/tts_out/hf_dataset \\
      --checkpoint_path /path/to/checkpoint \\
      --use_context \\
      --include_context_variants
        """
    )
    
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Path to HuggingFace dataset (local)"
    )
    parser.add_argument(
        "--checkpoint_path",
        type=str,
        default=None,
        help="Path to fine-tuned checkpoint (if not specified, uses base model)"
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default="openai/whisper-large-v3-turbo",
        help="Base model ID (default: openai/whisper-large-v3-turbo)"
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="Limit number of samples to evaluate (for quick testing)"
    )
    parser.add_argument(
        "--use_context",
        action="store_true",
        help="Use context field from dataset for conditioning"
    )
    parser.add_argument(
        "--use_language",
        action="store_true",
        help="Force language from dataset (instead of auto-detect)"
    )
    parser.add_argument(
        "--include_default_reference",
        action="store_true",
        help="Also run base model (ignoring context) as reference for comparison"
    )
    parser.add_argument(
        "--include_context_variants",
        action="store_true",
        help="Also capture transcriptions with/without context when available"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to run on (default: cuda)"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=None,
        help="Save full results to JSON file"
    )
    parser.add_argument(
        "--show_samples",
        type=int,
        default=10,
        help="Number of sample comparisons to display (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Expand paths
    dataset_path = os.path.expanduser(args.dataset_path)
    checkpoint_path = os.path.expanduser(args.checkpoint_path) if args.checkpoint_path else None
    
    # Validate paths
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path does not exist: {dataset_path}")
        sys.exit(1)
    
    if checkpoint_path and not os.path.exists(checkpoint_path):
        print(f"Error: Checkpoint path does not exist: {checkpoint_path}")
        sys.exit(1)
    
    # Run evaluation
    results = evaluate_dataset(
        dataset_path=dataset_path,
        model_id=args.model_id,
        checkpoint_path=checkpoint_path,
        max_samples=args.max_samples,
        use_context=args.use_context,
        use_language=args.use_language,
        include_default_reference=args.include_default_reference,
        include_context_variants=args.include_context_variants,
        device=args.device,
        show_samples=args.show_samples,
    )
    
    # Save results if requested
    if args.output_file:
        output_path = os.path.expanduser(args.output_file)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")
    
    # Return WER for scripting
    return results["summary"]["avg_wer"]


if __name__ == "__main__":
    main()
