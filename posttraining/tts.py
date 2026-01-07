#!/usr/bin/env python3
"""
tts_examples_with_english_voice_luts.py

Single-file examples for OpenAI, Cartesia, and ElevenLabs TTS,
PLUS an "English voice registry" (dict/LUT) per provider.

--------------------------------------------------------------------------------
INSTALL
  pip install requests

ENV VARS
  export OPENAI_API_KEY="..."
  export CARTESIA_API_KEY="..."
  export ELEVENLABS_API_KEY="..."

USAGE
  # Print English voice registry (dict/LUT) across all providers
  python tts_examples_with_english_voice_luts.py english-voices

  # Provider voice listing (full)
  python tts_examples_with_english_voice_luts.py openai   list-voices
  python tts_examples_with_english_voice_luts.py cartesia list-voices
  python tts_examples_with_english_voice_luts.py eleven   list-voices

  # Synthesize (each provider)
  python tts_examples_with_english_voice_luts.py openai tts   --text "Hello!" --voice marin --out openai.mp3
  python tts_examples_with_english_voice_luts.py cartesia tts --text "Hello!" --voice-id <cartesia-voice-uuid> --out cartesia.wav
  python tts_examples_with_english_voice_luts.py eleven tts   --text "Hello!" --voice-id <eleven-voice-id> --out eleven.mp3

--------------------------------------------------------------------------------
HOW TO THINK ABOUT "VOICES" (practical)

OpenAI:
  - You select a *built-in preset* by name (string), e.g. "marin".
  - These voices are currently optimized for English; they can still speak other languages,
    but English is the primary target.

Cartesia:
  - Voices are *resources* returned by GET /voices; you select them by ID (UUID).
  - Each voice has a `language` field (e.g. "en"), so "English voices" can be filtered reliably.

ElevenLabs:
  - Voices are *account-scoped resources* returned by GET /v1/voices; you select them by voice_id.
  - Many voices include `verified_languages` (or camelCase `verifiedLanguages`) entries.
    Each entry contains a language, modelId, and accent. If present, this is the best way
    to filter "English voices".
  - If verified languages are absent, we optionally fall back to labels["language"] if present.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


# ==============================================================================
# 0) ENGLISH VOICE REGISTRY (dict/LUT requested)
# ==============================================================================

# OpenAI's built-in TTS voices (13). Docs note these voices are currently optimized for English.
OPENAI_BUILTIN_TTS_VOICES: List[str] = [
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "nova",
    "onyx",
    "sage",
    "shimmer",
    "verse",
    "marin",
    "cedar",
]

# For OpenAI, treat all built-in voices as "English-supported" because they’re optimized for English.
OPENAI_ENGLISH_VOICES: List[str] = list(OPENAI_BUILTIN_TTS_VOICES)


def _norm_lang_token(x: Any) -> str:
    """
    Normalize language-ish values to a comparison token.
    Examples:
      "English" -> "english"
      "en"      -> "en"
      "en-US"   -> "en-us"
    """
    if x is None:
        return ""
    s = str(x).strip().lower().replace("_", "-")
    return s


def cartesia_fetch_all_voices(
    *,
    api_version: str = "2025-04-16",
    page_limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    Fetch *all* Cartesia voices accessible to your key, using pagination via starting_after.
    """
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key:
        raise RuntimeError("Missing CARTESIA_API_KEY")

    url = "https://api.cartesia.ai/voices"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Cartesia-Version": api_version,
        "Content-Type": "application/json",
    }

    voices: List[Dict[str, Any]] = []
    starting_after: Optional[str] = None

    while True:
        params: Dict[str, Any] = {"limit": min(max(page_limit, 1), 100)}
        if starting_after:
            params["starting_after"] = starting_after

        r = requests.get(url, headers=headers, params=params, timeout=60)
        if not r.ok:
            raise RuntimeError(f"Cartesia error {r.status_code}: {r.text}")

        payload = r.json()
        batch = payload.get("data", [])
        voices.extend(batch)

        if not payload.get("has_more") or not batch:
            break
        starting_after = batch[-1].get("id")

    return voices


def cartesia_english_voice_registry(
    *,
    api_version: str = "2025-04-16",
) -> List[Dict[str, str]]:
    """
    Returns a list of English Cartesia voices in a "registry" format:
      [{"id": "...", "name": "..."} , ...]

    Cartesia voice objects have an explicit "language" field, so filtering is straightforward.
    """
    voices = cartesia_fetch_all_voices(api_version=api_version)
    out: List[Dict[str, str]] = []
    for v in voices:
        if _norm_lang_token(v.get("language")) == "en":
            vid = v.get("id")
            name = v.get("name", "")
            if vid:
                out.append({"id": str(vid), "name": str(name)})
    # Stable output order helps diffing.
    out.sort(key=lambda x: (x["name"].lower(), x["id"]))
    return out


def eleven_fetch_all_voices() -> List[Dict[str, Any]]:
    """
    Fetch *all* ElevenLabs voices accessible to your account:
      GET https://api.elevenlabs.io/v1/voices

    Response includes a `voices` list (each has voice_id, name, labels, etc).
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ELEVENLABS_API_KEY")

    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": api_key, "Accept": "application/json"}

    r = requests.get(url, headers=headers, timeout=60)
    if not r.ok:
        raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text}")

    payload = r.json()
    return payload.get("voices", [])


def _eleven_voice_is_english(v: Dict[str, Any]) -> bool:
    """
    Best-effort English detection for an ElevenLabs voice.

    Preferred:
      - v["verified_languages"] (snake_case) OR v["verifiedLanguages"] (camelCase)
        Each entry typically has: language, model_id/modelId, accent.
        If ANY entry language is English-ish -> voice considered English-supported.

    Fallback:
      - v["labels"]["language"] if present.

    If neither exists, returns False (strict).
    """
    # 1) Prefer "verified languages" (stronger signal)
    verified = (
        v.get("verified_languages")
        or v.get("verifiedLanguages")
        or v.get("verified_languages".upper())  # defensive
    )
    if isinstance(verified, list) and verified:
        for entry in verified:
            if not isinstance(entry, dict):
                continue
            lang = _norm_lang_token(entry.get("language"))
            # Accept common ways languages appear.
            if lang in ("en", "english") or lang.startswith("en-"):
                return True

    # 2) Fallback: labels["language"]
    labels = v.get("labels")
    if isinstance(labels, dict):
        lang = _norm_lang_token(labels.get("language"))
        if lang in ("en", "english") or lang.startswith("en-"):
            return True

    return False


def eleven_english_voice_registry(
    *,
    include_unknown_as_english: bool = False,
) -> List[Dict[str, str]]:
    """
    Returns a list of English ElevenLabs voices in "registry" format:
      [{"voice_id": "...", "name": "..."} , ...]

    By default, this is STRICT: only includes voices where we can confirm English support
    from verified_languages / labels.language.
    If include_unknown_as_english=True, we include voices with unknown language metadata.
    """
    voices = eleven_fetch_all_voices()
    out: List[Dict[str, str]] = []
    unknown: List[Dict[str, str]] = []

    for v in voices:
        vid = v.get("voice_id") or v.get("voiceId")
        name = v.get("name", "")
        if not vid:
            continue

        if _eleven_voice_is_english(v):
            out.append({"voice_id": str(vid), "name": str(name)})
        else:
            unknown.append({"voice_id": str(vid), "name": str(name)})

    if include_unknown_as_english:
        # If your account’s voices don’t carry language metadata, you can switch this on.
        out.extend(unknown)

    out.sort(key=lambda x: (x["name"].lower(), x["voice_id"]))
    return out


def build_english_voice_lut() -> Dict[str, Any]:
    """
    This is the "dict/LUT from each provider -> list of supported English voices".

    Shape:
      {
        "openai": ["marin", "cedar", ...],
        "cartesia": [{"id": "...", "name": "..."}, ...],
        "elevenlabs": [{"voice_id": "...", "name": "..."}, ...]
      }
    """
    return {
        "openai": OPENAI_ENGLISH_VOICES,
        "cartesia": cartesia_english_voice_registry(),
        "elevenlabs": eleven_english_voice_registry(include_unknown_as_english=False),
    }


# ==============================================================================
# 1) OPENAI
# ==============================================================================

def openai_list_voices() -> None:
    print("OpenAI built-in TTS voices (also treated as English voices):")
    for v in OPENAI_BUILTIN_TTS_VOICES:
        print(f"  - {v}")


def openai_tts(
    *,
    text: str,
    out_path: str,
    model: str = "gpt-4o-mini-tts",
    voice_name: str = "marin",
    custom_voice_id: Optional[str] = None,
    instructions: Optional[str] = None,
    response_format: str = "mp3",
    speed: Optional[float] = None,
    stream: bool = True,
) -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    url = "https://api.openai.com/v1/audio/speech"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    voice: Any = {"id": custom_voice_id} if custom_voice_id else voice_name

    payload: Dict[str, Any] = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }
    if instructions:
        payload["instructions"] = instructions
    if speed is not None:
        payload["speed"] = speed

    with requests.post(url, headers=headers, json=payload, stream=stream, timeout=300) as r:
        if not r.ok:
            raise RuntimeError(f"OpenAI error {r.status_code}: {r.text}")
        with open(out_path, "wb") as f:
            if stream:
                for chunk in r.iter_content(chunk_size=1024 * 32):
                    if chunk:
                        f.write(chunk)
            else:
                f.write(r.content)


# ==============================================================================
# 2) CARTESIA (Sonic-3)
# ==============================================================================

def cartesia_list_voices(api_version: str = "2025-04-16") -> None:
    voices = cartesia_fetch_all_voices(api_version=api_version)
    print(f"Cartesia voices returned: {len(voices)}")
    for v in voices:
        vid = v.get("id")
        name = v.get("name", "")
        lang = v.get("language", "")
        desc = v.get("description", "") or ""
        desc = (desc[:80] + "…") if len(desc) > 80 else desc
        print(f"- {name} | id={vid} | language={lang} | {desc}")


def cartesia_tts(
    *,
    text: str,
    voice_id: str,
    out_path: str,
    model_id: str = "sonic-3",
    language: str = "en",
    api_version: str = "2025-04-16",
    volume: Optional[float] = None,
    speed: Optional[float] = None,
    emotion: Optional[str] = None,
    sample_rate: int = 44100,
) -> None:
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key:
        raise RuntimeError("Missing CARTESIA_API_KEY")

    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Cartesia-Version": api_version,
        "Content-Type": "application/json",
    }

    payload: Dict[str, Any] = {
        "model_id": model_id,
        "transcript": text,
        "voice": {"mode": "id", "id": voice_id},
        "language": language,
        "output_format": {"container": "wav", "encoding": "pcm_f32le", "sample_rate": sample_rate},
    }

    generation_config: Dict[str, Any] = {}
    if volume is not None:
        generation_config["volume"] = volume
    if speed is not None:
        generation_config["speed"] = speed
    if emotion is not None:
        generation_config["emotion"] = emotion
    if generation_config:
        payload["generation_config"] = generation_config

    r = requests.post(url, headers=headers, json=payload, timeout=300)
    if not r.ok:
        raise RuntimeError(f"Cartesia error {r.status_code}: {r.text}")
    with open(out_path, "wb") as f:
        f.write(r.content)


# ==============================================================================
# 3) ELEVENLABS
# ==============================================================================

def eleven_list_voices() -> None:
    voices = eleven_fetch_all_voices()
    print(f"ElevenLabs voices returned: {len(voices)}")
    for v in voices:
        name = v.get("name", "")
        vid = v.get("voice_id") or v.get("voiceId", "")
        category = v.get("category", "")
        labels = v.get("labels", {}) or {}
        # verified_languages may exist; show a compact hint if present
        verified = v.get("verified_languages") or v.get("verifiedLanguages") or []
        verified_hint = ""
        if isinstance(verified, list) and verified:
            langs = []
            for entry in verified:
                if isinstance(entry, dict) and entry.get("language"):
                    langs.append(str(entry["language"]))
            if langs:
                verified_hint = f" | verified_languages={','.join(langs)}"

        labels_str = ", ".join([f"{k}={labels[k]}" for k in sorted(labels.keys())]) if labels else ""
        if labels_str:
            print(f"- {name} | id={vid} | category={category} | {labels_str}{verified_hint}")
        else:
            print(f"- {name} | id={vid} | category={category}{verified_hint}")


def eleven_tts_stream(
    *,
    text: str,
    voice_id: str,
    out_path: str,
    model_id: str = "eleven_v3",
    output_format: Optional[str] = None,
    optimize_streaming_latency: Optional[int] = None,
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    style: Optional[float] = None,
    use_speaker_boost: Optional[bool] = None,
) -> None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ELEVENLABS_API_KEY")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    params: Dict[str, Any] = {}
    if output_format:
        params["output_format"] = output_format
    if optimize_streaming_latency is not None:
        params["optimize_streaming_latency"] = optimize_streaming_latency

    headers = {"xi-api-key": api_key, "Accept": "application/json"}

    payload: Dict[str, Any] = {"text": text, "model_id": model_id}
    voice_settings: Dict[str, Any] = {}
    if stability is not None:
        voice_settings["stability"] = stability
    if similarity_boost is not None:
        voice_settings["similarity_boost"] = similarity_boost
    if style is not None:
        voice_settings["style"] = style
    if use_speaker_boost is not None:
        voice_settings["use_speaker_boost"] = use_speaker_boost
    if voice_settings:
        payload["voice_settings"] = voice_settings

    with requests.post(url, headers=headers, params=params, json=payload, stream=True, timeout=300) as r:
        if not r.ok:
            raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text}")
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 32):
                if chunk:
                    f.write(chunk)


# ==============================================================================
# CLI
# ==============================================================================

def _add_common_tts_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--text", required=True, help="Text to synthesize.")
    p.add_argument("--out", required=True, help="Output audio file path (e.g. out.mp3, out.wav).")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="TTS examples + English voice LUTs for OpenAI, Cartesia, and ElevenLabs.",
    )

    # Top-level command: english-voices
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_english = sub.add_parser("english-voices", help="Print dict/LUT of English voices per provider")
    p_english.set_defaults(fn=lambda args: print(json.dumps(build_english_voice_lut(), indent=2)))

    # Provider commands
    p_openai = sub.add_parser("openai", help="OpenAI Speech API")
    p_cart = sub.add_parser("cartesia", help="Cartesia Sonic TTS")
    p_el = sub.add_parser("eleven", help="ElevenLabs TTS")

    # OpenAI subcommands
    so = p_openai.add_subparsers(dest="action", required=True)
    so.add_parser("list-voices", help="Print OpenAI built-in voices").set_defaults(fn=lambda args: openai_list_voices())
    po_tts = so.add_parser("tts", help="Synthesize TTS with OpenAI")
    _add_common_tts_args(po_tts)
    po_tts.add_argument("--model", default="gpt-4o-mini-tts")
    po_tts.add_argument("--voice", default="marin", help="Built-in voice name (e.g. marin).")
    po_tts.add_argument("--custom-voice-id", default=None, help="Optional custom voice id (voice_...).")
    po_tts.add_argument("--instructions", default=None, help="Optional delivery guidance (tone, pace, etc).")
    po_tts.add_argument("--format", default="mp3", help="response_format: mp3|wav|opus|aac|flac|pcm")
    po_tts.add_argument("--speed", type=float, default=None, help="0.25..4.0 (1.0 default).")
    po_tts.set_defaults(
        fn=lambda args: openai_tts(
            text=args.text,
            out_path=args.out,
            model=args.model,
            voice_name=args.voice,
            custom_voice_id=args.custom_voice_id,
            instructions=args.instructions,
            response_format=args.format,
            speed=args.speed,
            stream=True,
        )
    )

    # Cartesia subcommands
    sc = p_cart.add_subparsers(dest="action", required=True)
    pc_lv = sc.add_parser("list-voices", help="Fetch & print Cartesia voices (full list)")
    pc_lv.add_argument("--api-version", default="2025-04-16")
    pc_lv.set_defaults(fn=lambda args: cartesia_list_voices(api_version=args.api_version))

    pc_tts = sc.add_parser("tts", help="Synthesize TTS with Cartesia (sonic-3)")
    _add_common_tts_args(pc_tts)
    pc_tts.add_argument("--api-version", default="2025-04-16")
    pc_tts.add_argument("--model", default="sonic-3")
    pc_tts.add_argument("--voice-id", required=True, help="Voice UUID from `cartesia list-voices`.")
    pc_tts.add_argument("--language", default="en")
    pc_tts.add_argument("--volume", type=float, default=None)
    pc_tts.add_argument("--speed", type=float, default=None)
    pc_tts.add_argument("--emotion", default=None)
    pc_tts.add_argument("--sample-rate", type=int, default=44100)
    pc_tts.set_defaults(
        fn=lambda args: cartesia_tts(
            text=args.text,
            voice_id=args.voice_id,
            out_path=args.out,
            model_id=args.model,
            language=args.language,
            api_version=args.api_version,
            volume=args.volume,
            speed=args.speed,
            emotion=args.emotion,
            sample_rate=args.sample_rate,
        )
    )

    # ElevenLabs subcommands
    se = p_el.add_subparsers(dest="action", required=True)
    se.add_parser("list-voices", help="Fetch & print ElevenLabs voices (full list)").set_defaults(
        fn=lambda args: eleven_list_voices()
    )

    pe_tts = se.add_parser("tts", help="Stream TTS with ElevenLabs")
    _add_common_tts_args(pe_tts)
    pe_tts.add_argument("--voice-id", required=True, help="Voice ID from `eleven list-voices`.")
    pe_tts.add_argument("--model", default="eleven_v3")
    pe_tts.add_argument("--output-format", default=None, help='Optional query param, e.g. "mp3_44100_128"')
    pe_tts.add_argument("--optimize-streaming-latency", type=int, default=None)
    pe_tts.add_argument("--stability", type=float, default=None)
    pe_tts.add_argument("--similarity-boost", type=float, default=None)
    pe_tts.add_argument("--style", type=float, default=None)
    pe_tts.add_argument("--use-speaker-boost", action="store_true", default=None)
    pe_tts.set_defaults(
        fn=lambda args: eleven_tts_stream(
            text=args.text,
            voice_id=args.voice_id,
            out_path=args.out,
            model_id=args.model,
            output_format=args.output_format,
            optimize_streaming_latency=args.optimize_streaming_latency,
            stability=args.stability,
            similarity_boost=args.similarity_boost,
            style=args.style,
            use_speaker_boost=args.use_speaker_boost if args.use_speaker_boost is not None else None,
        )
    )

    args = parser.parse_args(argv)

    try:
        args.fn(args)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())