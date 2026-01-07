#!/usr/bin/env python3
"""
Convert a TTS output directory into a HuggingFace dataset with audio.

Expected input:
  - JSONL with "audio" or "audio_path", "transcription"/"corrected_phrase",
    "names" (context), and optionally "language" fields.
  - Default JSONL path: <input-dir>/dataset.jsonl

Output:
  - HuggingFace dataset on disk with columns:
    - audio: Audio feature (dict with 'array' and 'sampling_rate')
    - context: Names/context string (from 'names' field, joined)
    - transcription: The correct transcription (from 'corrected_phrase' or 'transcription')
    - language: Language code (defaults to 'auto' if not present)
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional

import librosa
import soundfile as sf
from datasets import Audio, Dataset, Features, Value


def _load_jsonl(path: str, base_dir: str, limit: Optional[int]) -> List[Dict[str, Any]]:
    """Load JSONL file and return list of records."""
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            
            # Get audio path
            audio_path = record.get("audio") or record.get("audio_path")
            if not audio_path:
                raise ValueError(f"Missing audio path in record: {record}")
            if not os.path.isabs(audio_path):
                audio_path = os.path.join(base_dir, audio_path)
            
            # Get transcription - prefer corrected_phrase for training
            transcription = (
                record.get("corrected_phrase") 
                or record.get("transcription") 
                or record.get("text")
            )
            if not transcription:
                raise ValueError(f"Missing transcription in record: {record}")
            
            # Get context from names field
            names = record.get("names", [])
            if isinstance(names, list):
                context = ", ".join(names)
            else:
                context = str(names) if names else ""
            
            # Get language
            language = record.get("language", "auto")
            
            rows.append({
                "audio_path": audio_path,
                "context": context,
                "transcription": transcription,
                "language": language,
                # Keep original record for reference
                "_original": record,
            })
            
            if limit is not None and len(rows) >= limit:
                break
    return rows


def _load_audio(audio_path: str, target_sr: int = 16000) -> Dict[str, Any]:
    """Load audio file and return dict compatible with HuggingFace Audio feature."""
    audio_array, sr = sf.read(audio_path)
    
    # Convert to mono if stereo
    if audio_array.ndim > 1:
        audio_array = audio_array.mean(axis=1)
    
    # Resample to target sample rate if needed
    if sr != target_sr:
        audio_array = librosa.resample(audio_array, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    
    return {
        "array": audio_array,
        "sampling_rate": sr,
    }


def _prepare_dataset(
    rows: List[Dict[str, Any]],
    target_sr: int = 16000,
) -> Dataset:
    """Prepare HuggingFace dataset from rows."""
    
    # Process all rows
    processed_rows = []
    for i, row in enumerate(rows):
        if (i + 1) % 100 == 0 or i == 0:
            print(f"Processing row {i + 1}/{len(rows)}...")
        
        try:
            audio_data = _load_audio(row["audio_path"], target_sr=target_sr)
            processed_rows.append({
                "audio": audio_data,
                "context": row["context"],
                "transcription": row["transcription"],
                "language": row["language"],
            })
        except Exception as e:
            print(f"Warning: Failed to load audio for row {i}: {e}")
            continue
    
    if not processed_rows:
        raise ValueError("No rows were successfully processed!")
    
    # Create dataset with Audio feature
    # Note: We create with the audio dict format, then cast to Audio feature
    dataset = Dataset.from_list(processed_rows)
    
    # Cast the audio column to proper Audio feature
    dataset = dataset.cast_column("audio", Audio(sampling_rate=target_sr))
    
    return dataset


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert TTS output JSONL into a HuggingFace dataset with audio.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--input-dir",
        default="tts_out",
        help="Directory containing dataset.jsonl (default: tts_out).",
    )
    parser.add_argument(
        "--jsonl",
        default=None,
        help="Path to dataset JSONL (overrides --input-dir for JSONL location).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for the HuggingFace dataset (default: <input-dir>/hf_dataset).",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Target audio sample rate (default: 16000).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of rows processed (for testing).",
    )
    args = parser.parse_args(argv)

    input_dir = os.path.abspath(args.input_dir)
    jsonl_path = args.jsonl or os.path.join(input_dir, "dataset.jsonl")
    output_dir = args.output_dir or os.path.join(input_dir, "hf_dataset")

    print(f"Loading JSONL from: {jsonl_path}")
    rows = _load_jsonl(jsonl_path, base_dir=input_dir, limit=args.limit)
    if not rows:
        raise SystemExit("No rows found in JSONL.")
    print(f"Loaded {len(rows)} rows from JSONL.")

    print(f"Processing audio files (target sample rate: {args.sample_rate} Hz)...")
    dataset = _prepare_dataset(rows, target_sr=args.sample_rate)
    
    print(f"\nDataset info:")
    print(f"  - Number of examples: {len(dataset)}")
    print(f"  - Features: {dataset.features}")
    
    # Show a sample
    if len(dataset) > 0:
        sample = dataset[0]
        print(f"\nSample row:")
        print(f"  - context: {sample['context'][:100]}...")
        print(f"  - transcription: {sample['transcription']}")
        print(f"  - language: {sample['language']}")
        print(f"  - audio shape: {sample['audio']['array'].shape}")
        print(f"  - audio sample_rate: {sample['audio']['sampling_rate']}")

    os.makedirs(output_dir, exist_ok=True)
    dataset.save_to_disk(output_dir)
    print(f"\nSaved HuggingFace dataset to: {output_dir}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

