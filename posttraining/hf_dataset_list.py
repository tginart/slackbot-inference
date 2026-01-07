'''
All functions should return a HuggingFace Dataset object
that matches the columns spec of a raw audio dataset as described in DATASET_FORMAT.md
This includes the audio column, context column, transcription column, and language column. ('auto' if missing)
'''
import datasets
import os
from pathlib import Path
import random
import time
from functools import lru_cache
import argparse

import httpx

_LLM_CLIENT = None
_LLM_BASE_URL = None
_LLM_MODEL = None
_LLM_SYSTEM_PROMPT = (
    "You are a careful copy editor. Fix capitalization, punctuation, and grammar, "
    "while preserving meaning. Do not add or remove named entities. "
    "Output only the corrected sentence(s), with no quotes or extra text."
)


def _ensure_llm_client(*, api_key: str, base_url: str, model: str) -> httpx.Client:
    global _LLM_CLIENT, _LLM_BASE_URL, _LLM_MODEL
    base_url = (base_url or "https://api.openai.com/v1").rstrip("/")

    if _LLM_CLIENT is None or _LLM_BASE_URL != base_url or _LLM_MODEL != model:
        if _LLM_CLIENT is not None:
            try:
                _LLM_CLIENT.close()
            finally:
                _LLM_CLIENT = None

        _LLM_BASE_URL = base_url
        _LLM_MODEL = model
        _correct_text_cached.cache_clear()

        _LLM_CLIENT = httpx.Client(
            base_url=_LLM_BASE_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=10.0),
        )

    return _LLM_CLIENT


def _close_llm_client() -> None:
    global _LLM_CLIENT
    if _LLM_CLIENT is None:
        return
    try:
        _LLM_CLIENT.close()
    finally:
        _LLM_CLIENT = None


@lru_cache(maxsize=10_000)
def _correct_text_cached(text: str) -> str:
    if text is None:
        return ""

    original = str(text).strip()
    if not original:
        return ""

    if _LLM_CLIENT is None or _LLM_MODEL is None:
        raise RuntimeError("LLM client not initialized. Call _ensure_llm_client() first.")

    payload = {
        "model": _LLM_MODEL,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": _LLM_SYSTEM_PROMPT},
            {"role": "user", "content": original},
        ],
    }

    backoff_s = 1.0
    last_error = None
    for _ in range(6):
        try:
            resp = _LLM_CLIENT.post("/chat/completions", json=payload)
            if resp.status_code in (429, 500, 502, 503, 504):
                last_error = RuntimeError(f"LLM API error {resp.status_code}: {resp.text[:200]}")
                time.sleep(backoff_s)
                backoff_s = min(backoff_s * 2, 30.0)
                continue
            resp.raise_for_status()
            data = resp.json()
            out = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
            out = (out or "").strip()
            if (out.startswith('"') and out.endswith('"')) or (out.startswith("'") and out.endswith("'")):
                out = out[1:-1].strip()
            return out or original
        except Exception as e:
            last_error = e
            time.sleep(backoff_s)
            backoff_s = min(backoff_s * 2, 30.0)

    raise RuntimeError(f"Failed to correct text via LLM after retries: {last_error}")


def _librispeech_to_training_format(batch, *, api_key: str, base_url: str, model: str):
    _ensure_llm_client(api_key=api_key, base_url=base_url, model=model)
    corrected = [_correct_text_cached(t) for t in batch["text"]]
    n = len(corrected)
    return {
        "transcription": corrected,
        "context": [""] * n,
        "language": ["en"] * n,
    }


def get_ds_librispeech_asr():
    # from hf datasets load_dataset('openslr/librispeech_asr')
    # use the clean subset
    # Use LLM via API to correct the captualization, punctuation, and grammer in the `text` field
    # context is null/empty for all of these
    # language is 'en' for all of these
    # filter down to random 1000 rows
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Temporary convenience: fall back to reading posttraining/apikeys.txt
        apikeys_path = Path(__file__).resolve().parent / "apikeys.txt"
        if apikeys_path.exists():
            for line in apikeys_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "OPENAI_API_KEY" and v.strip():
                    api_key = v.strip()
                    break

    if not api_key:
        raise ValueError(
            "Missing OPENAI_API_KEY env var (required for LLM text correction), "
            "and no OPENAI_API_KEY found in posttraining/apikeys.txt."
        )

    model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    try:
        def load_random_1000():
            try:
                ids = datasets.load_dataset(
                    "openslr/librispeech_asr",
                    "clean",
                    split="train.100",
                    streaming=True,
                )
                ids = ids.shuffle(seed=42, buffer_size=10_000)
                return datasets.Dataset.from_list(list(ids.take(1000)))
            except Exception:
                ds = datasets.load_dataset("openslr/librispeech_asr", "clean", split="train.100")
                return ds.shuffle(seed=42).select(range(1000))

        ds = load_random_1000()

        try:
            n_parallel = int(os.environ.get("N_PARALLEL", "8"))
        except ValueError:
            n_parallel = 8
        n_parallel = max(1, n_parallel)
        num_proc = n_parallel if n_parallel > 1 else None

        ds = ds.map(
            _librispeech_to_training_format,
            fn_kwargs={"api_key": api_key, "base_url": base_url, "model": model},
            batched=True,
            batch_size=10,
            num_proc=num_proc,
            desc=f"Correcting text via LLM (num_proc={n_parallel})",
            load_from_cache_file=False,
        )

        keep = {"audio", "context", "transcription", "language"}
        drop = [c for c in ds.column_names if c not in keep]
        if drop:
            ds = ds.remove_columns(drop)

        return ds
    finally:
        _close_llm_client()


def get_ds_genshin_voice():
    ds = datasets.load_dataset('simon3000/genshin-voice')
    # randomly subsample 5000 rows from the 'train' split (DatasetDict object)
    ds = ds["train"].select(random.sample(range(len(ds["train"])), 1000))

    # filter to those with non-empty 'transcription' field
    ds = ds.filter(lambda x: bool(x.get('transcription', '').strip()))

    return ds

def get_synthetic_names_data_jan_5_hf():
    ds = datasets.load_from_disk('/home/aginart_salesforce_com/slackbot-inference/synthetic_names_data_jan_5_hf')
    return ds

def _prepare_for_concat(ds: datasets.Dataset, *, columns: list[str]) -> datasets.Dataset:
    missing = [c for c in columns if c not in ds.column_names]
    if missing:
        # Only auto-fill common metadata columns.
        num_rows = ds.num_rows
        for col in missing:
            if col == "context":
                ds = ds.add_column("context", [""] * num_rows)
            elif col == "language":
                ds = ds.add_column("language", ["auto"] * num_rows)
            else:
                raise ValueError(f"Dataset missing required column for concat: {col}")

    if "audio" in columns and "audio" in ds.column_names:
        # Normalize audio feature so concatenate_datasets can align schemas.
        ds = ds.cast_column("audio", datasets.Audio(sampling_rate=16_000))

    drop = [c for c in ds.column_names if c not in columns]
    if drop:
        ds = ds.remove_columns(drop)

    # Enforce consistent column order across all datasets.
    return ds.select_columns(columns)

def final_assembly_and_processing() -> datasets.Dataset:
    ds1 = get_ds_librispeech_asr()
    ds2 = get_ds_genshin_voice()
    ds3 = get_synthetic_names_data_jan_5_hf()

    # Columns to keep when concatenating datasets.
    stack_columns = ["audio", "transcription", "context", "language"]

    ds1 = _prepare_for_concat(ds1, columns=stack_columns)
    ds2 = _prepare_for_concat(ds2, columns=stack_columns)
    ds3 = _prepare_for_concat(ds3, columns=stack_columns)

    # stack the datasets
    ds = datasets.concatenate_datasets([ds1, ds2, ds3])

    # for each non-auto row, with a chance of 10%, convert language to 'auto'
    def maybe_autodetect_language(batch):
        languages = []
        for lang in batch["language"]:
            if random.random() < 0.1 and lang != "auto":
                languages.append("auto")
            else:
                languages.append(lang)
        return {"language": languages}

    ds = ds.map(maybe_autodetect_language, batched=True, batch_size=100)

    return ds


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble and save a combined HF dataset.")
    parser.add_argument(
        "--output_path",
        required=True,
        help="Path to save the assembled dataset (HuggingFace save_to_disk format).",
    )
    args = parser.parse_args()

    ds = final_assembly_and_processing()
    os.makedirs(args.output_path, exist_ok=True)
    ds.save_to_disk(args.output_path)
    print(f"Saved dataset with {len(ds)} rows to {args.output_path}")


if __name__ == "__main__":
    main()
