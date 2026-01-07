#!/usr/bin/env python3
"""
Convert a TTS output directory into a prepared Whisper dataset.

Expected input:
  - JSONL with "audio" or "audio_path" and "transcription" fields.
  - Default JSONL path: <input-dir>/dataset.jsonl

Output:
  - HuggingFace dataset on disk with columns: input_features, labels
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional

import librosa
import soundfile as sf
from datasets import Dataset
from transformers import WhisperForConditionalGeneration, WhisperProcessor


def _load_jsonl(path: str, base_dir: str, limit: Optional[int]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            audio_path = record.get("audio") or record.get("audio_path")
            if not audio_path:
                raise ValueError(f"Missing audio path in record: {record}")
            if not os.path.isabs(audio_path):
                audio_path = os.path.join(base_dir, audio_path)
            transcription = record.get("transcription") or record.get("text")
            if not transcription:
                raise ValueError(f"Missing transcription in record: {record}")
            rows.append({"audio_path": audio_path, "transcription": transcription, **record})
            if limit is not None and len(rows) >= limit:
                break
    return rows


def _prepare_sample(
    sample: Dict[str, Any],
    *,
    processor: WhisperProcessor,
    model: WhisperForConditionalGeneration,
    language_option: str,
    default_language: Optional[str],
) -> Dict[str, Any]:
    audio_array, sr = sf.read(sample["audio_path"])
    if audio_array.ndim > 1:
        audio_array = audio_array.mean(axis=1)
    if sr != 16000:
        audio_array = librosa.resample(audio_array, orig_sr=sr, target_sr=16000)
        sr = 16000

    input_features = processor.feature_extractor(
        audio_array, sampling_rate=sr
    ).input_features[0]

    text = sample["transcription"]
    if language_option == "dataset":
        lang_str = sample.get("language") or default_language
        if not lang_str:
            raise ValueError("Missing language for dataset mode.")
        lang_to_id = model.generation_config.lang_to_id
        task_to_id = model.generation_config.task_to_id
        lang_code = lang_str.lower()[:2]
        lang_token = f"<|{lang_code}|>"
        if lang_token not in lang_to_id:
            raise ValueError(f"Language code '{lang_code}' not recognized by model.")
        bos_id = model.config.decoder_start_token_id
        eos_id = processor.tokenizer.eos_token_id
        transcribe_token_id = task_to_id.get("transcribe")
        if bos_id is None or eos_id is None or transcribe_token_id is None:
            raise ValueError("Special token ids not properly loaded from model config.")
        text_ids = processor.tokenizer(text, add_special_tokens=False).input_ids
        labels = [bos_id, lang_to_id[lang_token], transcribe_token_id] + text_ids + [eos_id]
    else:
        labels = processor.tokenizer(text).input_ids

    return {"input_features": input_features, "labels": labels}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert TTS output JSONL into a prepared Whisper dataset.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--input-dir", default="tts_out", help="Directory containing dataset.jsonl.")
    parser.add_argument("--jsonl", default=None, help="Path to dataset JSONL (overrides input-dir).")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for the prepared dataset (default: <input-dir>/prepared_dataset).",
    )
    parser.add_argument(
        "--model-id",
        default="openai/whisper-large-v3-turbo",
        help="Whisper model id for feature extraction and tokenization.",
    )
    parser.add_argument("--language-option", choices=["auto", "dataset"], default="auto")
    parser.add_argument("--language", default="en", help="Default language for dataset mode.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of rows processed.")
    args = parser.parse_args(argv)

    input_dir = os.path.abspath(args.input_dir)
    jsonl_path = args.jsonl or os.path.join(input_dir, "dataset.jsonl")
    output_dir = args.output_dir or os.path.join(input_dir, "prepared_dataset")

    rows = _load_jsonl(jsonl_path, base_dir=input_dir, limit=args.limit)
    if not rows:
        raise SystemExit("No rows found in JSONL.")

    processor = WhisperProcessor.from_pretrained(
        args.model_id,
        task="transcribe",
        language=None if args.language_option == "auto" else "auto",
    )
    model = WhisperForConditionalGeneration.from_pretrained(args.model_id)

    dataset = Dataset.from_list(rows)
    dataset = dataset.map(
        lambda sample: _prepare_sample(
            sample,
            processor=processor,
            model=model,
            language_option=args.language_option,
            default_language=args.language if args.language_option == "dataset" else None,
        ),
        remove_columns=dataset.column_names,
    )

    os.makedirs(output_dir, exist_ok=True)
    dataset.save_to_disk(output_dir)
    print(f"Saved prepared dataset to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
