"""
Test script for Whisper Inference Server

Warms up the server and measures transcription speed.

Usage:
  python test_server.py --url http://localhost:8000 --audio MLKDream_20s.wav
"""

import argparse
import time
import statistics
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def health_check(base_url: str) -> dict:
    resp = requests.get(f"{base_url}/health", timeout=10)
    resp.raise_for_status()
    return resp.json()


def transcribe(base_url: str, audio_path: str, context: str = None):
    """
    Send transcription request and return (transcription, latency_seconds, timing_dict).
    """
    with open(audio_path, "rb") as f:
        files = {"audio": (Path(audio_path).name, f, "audio/wav")}
        data = {}
        if context is not None:
            data["context"] = context

        start = time.perf_counter()
        resp = requests.post(
            f"{base_url}/transcribe",
            files=files,
            data=data if data else None,
            timeout=300,
        )
        elapsed = time.perf_counter() - start

    resp.raise_for_status()
    result = resp.json()
    timing = result.get("timing", {})
    return result["transcription"], elapsed, timing


def warmup(base_url: str, audio_path: str, num_requests: int = 24, max_workers: int = 8):
    print(f"\n{'='*60}")
    print("WARMUP PHASE")
    print(f"{'='*60}")
    print(f"Sending {num_requests} concurrent warmup requests (max {max_workers} workers)...")

    completed = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(transcribe, base_url, audio_path, None)
            for _ in range(num_requests)
        ]

        for i, future in enumerate(as_completed(futures)):
            try:
                _, latency, _ = future.result()
                completed += 1
                print(f"  Warmup {i+1}/{num_requests}: {latency*1000:.1f}ms")
            except Exception as e:
                failed += 1
                print(f"  Warmup {i+1}/{num_requests}: FAILED - {e}")

    print(f"Warmup complete. ({completed} succeeded, {failed} failed)\n")


def _fmt_gen(timing: dict) -> str:
    if not timing:
        return ""
    gw = timing.get("generate_wall_ms", None)
    gg = timing.get("generate_gpu_ms", None)
    if gw is None and gg is None:
        return ""
    if gw is not None and gg is not None:
        return f"gen_wall={gw:.0f}ms gen_gpu={gg:.0f}ms"
    if gw is not None:
        return f"gen_wall={gw:.0f}ms"
    return f"gen_gpu={gg:.0f}ms"


def benchmark_sequential(base_url: str, audio_path: str, num_requests: int = 10, context: str = None):
    print(f"\n{'='*60}")
    print("SEQUENTIAL BENCHMARK")
    print(f"{'='*60}")
    print(f"Running {num_requests} sequential requests...")
    if context:
        print(f"Context: {context[:50]}..." if len(context) > 50 else f"Context: {context}")

    latencies = []
    all_timings = []
    transcription = None

    for i in range(num_requests):
        try:
            text, latency, timing = transcribe(base_url, audio_path, context)
            latencies.append(latency)
            all_timings.append(timing)
            transcription = text

            if timing:
                w_id = timing.get("worker_id", "?")
                g_id = timing.get("gpu_id", "?")
                tl = timing.get("timeline", {})
                gen_range = ""
                if tl:
                    gen_range = f"gen@[{tl.get('generate_start', 0):.0f}-{tl.get('generate_end', 0):.0f}]"
                gen_str = _fmt_gen(timing)
                pp = timing.get("preprocess_ms", 0)
                print(f"  Request {i+1}/{num_requests}: {latency*1000:.1f}ms W{w_id}/G{g_id} "
                      f"[pp={pp:.0f}ms, {gen_str}] {gen_range}")
            else:
                print(f"  Request {i+1}/{num_requests}: {latency*1000:.1f}ms")
        except Exception as e:
            print(f"  Request {i+1}/{num_requests}: FAILED - {e}")

    return latencies, transcription, all_timings


def benchmark_concurrent(base_url: str, audio_path: str, num_requests: int = 16, max_workers: int = 8, context: str = None, verbose: bool = True, label: str = None):
    if label is None:
        label = "CONCURRENT"
    print(f"\n{'='*60}")
    print(f"{label} BENCHMARK")
    print(f"{'='*60}")
    print(f"Running {num_requests} concurrent requests (max {max_workers} workers)...")

    latencies = []
    all_timings = []

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(transcribe, base_url, audio_path, context)
            for _ in range(num_requests)
        ]

        for i, future in enumerate(as_completed(futures)):
            try:
                _, latency, timing = future.result()
                latencies.append(latency)
                all_timings.append(timing)

                if verbose:
                    if timing:
                        w_id = timing.get("worker_id", "?")
                        g_id = timing.get("gpu_id", "?")
                        tl = timing.get("timeline", {})
                        gen_range = ""
                        if tl:
                            gen_range = f"gen@[{tl.get('generate_start', 0):.0f}-{tl.get('generate_end', 0):.0f}]"
                        gen_str = _fmt_gen(timing)
                        pp = timing.get("preprocess_ms", 0)
                        print(f"  Completed {i+1}/{num_requests}: {latency*1000:.1f}ms W{w_id}/G{g_id} "
                              f"[pp={pp:.0f}ms, {gen_str}] {gen_range}")
                    else:
                        print(f"  Completed {i+1}/{num_requests}: {latency*1000:.1f}ms")
            except Exception as e:
                if verbose:
                    print(f"  Failed {i+1}/{num_requests}: {e}")

    total_time = time.perf_counter() - start_time
    if not verbose:
        print(f"  Completed {len(latencies)}/{num_requests} requests")
    return latencies, total_time, all_timings


def print_stats(latencies, label: str, total_time: float = None):
    if not latencies:
        print(f"\n{label}: No successful requests")
        return

    print(f"\n{'-'*60}")
    print(f"{label} STATISTICS ({len(latencies)} requests)")
    print(f"{'-'*60}")
    print(f"  Min latency    : {min(latencies)*1000:8.1f} ms")
    print(f"  Max latency    : {max(latencies)*1000:8.1f} ms")
    print(f"  Mean latency   : {statistics.mean(latencies)*1000:8.1f} ms")
    print(f"  Median latency : {statistics.median(latencies)*1000:8.1f} ms")

    if len(latencies) > 1:
        print(f"  Std dev        : {statistics.stdev(latencies)*1000:8.1f} ms")

    if total_time:
        throughput = len(latencies) / total_time
        print(f"  Total time     : {total_time*1000:8.1f} ms")
        print(f"  Throughput     : {throughput:8.2f} req/s")


def print_timing_stats(timings, label: str):
    if not timings or not any(timings):
        return

    valid = [t for t in timings if t]
    if not valid:
        return

    print(f"\n{'-'*60}")
    print(f"{label} SERVER-SIDE TIMING BREAKDOWN (avg ms)")
    print(f"{'-'*60}")

    workers_used = sorted(set(t.get("worker_id") for t in valid if "worker_id" in t))
    gpus_used = sorted(set(t.get("gpu_id") for t in valid if "gpu_id" in t))
    print(f"  Workers used: {workers_used}")
    print(f"  GPUs used: {gpus_used}")
    print()

    keys = [
        "queue_wait_ms",
        "load_ms",
        "preprocess_ms",
        "generate_wall_ms",
        "generate_gpu_ms",
        "decode_ms",
        "total_worker_ms",
        "http_wait_ms",
    ]

    for key in keys:
        values = [t.get(key, None) for t in valid if key in t]
        values = [v for v in values if v is not None]
        if values:
            avg_val = statistics.mean(values)
            min_val = min(values)
            max_val = max(values)
            label_name = key.replace("_ms", "").replace("_", " ")
            print(f"  {label_name:18s}: avg={avg_val:7.1f}, min={min_val:7.1f}, max={max_val:7.1f}")


def print_timeline(timings, label: str):
    valid = [t for t in timings if t and "timeline" in t]
    if not valid:
        return

    print(f"\n{'-'*80}")
    print(f"{label} TIMELINE (generate phase, sorted by start time)")
    print(f"{'-'*80}")

    sorted_timings = sorted(valid, key=lambda t: t["timeline"].get("generate_start", 0))
    min_time = min(t["timeline"].get("generate_start", 0) for t in sorted_timings)
    max_time = max(t["timeline"].get("generate_end", 0) for t in sorted_timings)
    span = max_time - min_time if max_time > min_time else 1

    print(f"  {'W/G':>5} {'gen_start':>10} {'gen_end':>10} {'dur':>6}  GANTT")
    print(f"  {'-'*5} {'-'*10} {'-'*10} {'-'*6}  |{'='*50}|")

    bar_width = 50
    for t in sorted_timings:
        w_id = t.get("worker_id", "?")
        g_id = t.get("gpu_id", "?")
        tl = t["timeline"]
        s = tl.get("generate_start", 0)
        e = tl.get("generate_end", 0)
        d = e - s

        start_pos = int((s - min_time) / span * bar_width)
        end_pos = int((e - min_time) / span * bar_width)
        bar_len = max(1, end_pos - start_pos)

        bar = [" "] * bar_width
        for i in range(start_pos, min(start_pos + bar_len, bar_width)):
            bar[i] = "█"
        print(f"  W{w_id}/G{g_id} {s:10.0f} {e:10.0f} {d:6.0f}  |{''.join(bar)}|")

    print(f"  {' '*5} {' '*10} {' '*10} {' '*6}  |{'='*50}|")
    print(f"  Timeline spans {min_time:.0f}ms to {max_time:.0f}ms (range: {span:.0f}ms)")


def main():
    parser = argparse.ArgumentParser(description="Test Whisper Inference Server")
    parser.add_argument("--url", type=str, default="http://localhost:8000", help="Server URL")
    parser.add_argument("--audio", type=str, default="MLKDream_20s.wav", help="Audio file to use for testing")
    parser.add_argument("--warmup-requests", type=int, default=80, help="Number of warmup requests")
    parser.add_argument("--sequential-requests", type=int, default=10, help="Number of sequential benchmark requests")
    parser.add_argument("--concurrent-requests", type=int, default=16, help="Number of concurrent benchmark requests")
    parser.add_argument("--max-workers", type=int, default=8, help="Max concurrency in the client")
    parser.add_argument("--context", type=str, default=None, help="Optional context text for transcription (overrides prompt scenarios)")
    parser.add_argument("--skip-prompt-scenarios", action="store_true", help="Skip running tests with different prompt scenarios")
    parser.add_argument("--skip-warmup", action="store_true", help="Skip warmup phase")
    parser.add_argument("--skip-sequential", action="store_true", help="Skip sequential benchmark")
    parser.add_argument("--skip-8-concurrent", action="store_true", help="Skip 8 concurrent requests benchmark")
    parser.add_argument("--skip-concurrent", action="store_true", help="Skip 16 concurrent requests benchmark")
    parser.add_argument("--skip-256-concurrent", action="store_true", help="Skip 256 concurrent requests benchmark")
    parser.add_argument("--concurrent-256-requests", type=int, default=256, help="Number of concurrent requests for 256 test")
    parser.add_argument("--max-workers-256", type=int, default=128, help="Max concurrency in the client for 256 test")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.is_absolute():
        audio_path = Path(__file__).parent / args.audio

    if not audio_path.exists():
        print(f"ERROR: Audio file not found: {audio_path}")
        return 1

    print(f"\n{'='*60}")
    print("WHISPER INFERENCE SERVER TEST")
    print(f"{'='*60}")
    print(f"Server URL : {args.url}")
    print(f"Audio file : {audio_path}")
    print(f"Audio size : {audio_path.stat().st_size / 1024:.1f} KB")

    print("\nChecking server health...")
    try:
        health = health_check(args.url)
        print(f"  Status: {health['status']}")
        print(f"  Workers alive: {health['workers_alive']}/{health['workers_total']}")
    except Exception as e:
        print(f"ERROR: Server health check failed: {e}")
        return 1

    if not args.skip_warmup:
        warmup(args.url, str(audio_path), args.warmup_requests, args.max_workers)

    # Define prompt scenarios: (name, context)
    if args.context is not None:
        # If user provided a specific context, use that for all tests
        prompt_scenarios = [("custom", args.context)]
    elif args.skip_prompt_scenarios:
        # If skipping prompt scenarios, just use None
        prompt_scenarios = [("no prompt", None)]
    else:
        # Run with 3 different prompt scenarios
        prompt_scenarios = [
            ("no prompt", None),
            ("8 char prompt", " " * 8),
            ("256 char prompt", " " * 256),
        ]

    # Run each test type with each prompt scenario
    for scenario_idx, (prompt_name, prompt_context) in enumerate(prompt_scenarios):
        prompt_label = f" [{prompt_name}]" if prompt_name != "no prompt" else ""
        
        if not args.skip_sequential:
            print(f"\n{'#'*60}")
            print(f"# SEQUENTIAL TEST{prompt_label}")
            print(f"{'#'*60}")
            seq_latencies, transcription, seq_timings = benchmark_sequential(
                args.url, str(audio_path), args.sequential_requests, prompt_context
            )
            print_stats(seq_latencies, f"SEQUENTIAL{prompt_label}")
            print_timing_stats(seq_timings, f"SEQUENTIAL{prompt_label}")
            print_timeline(seq_timings, f"SEQUENTIAL{prompt_label}")

            if transcription and scenario_idx == 0:  # Only show transcription for first scenario
                print(f"\n{'-'*60}")
                print("SAMPLE TRANSCRIPTION")
                print(f"{'-'*60}")
                print(transcription[:500] + "..." if len(transcription) > 500 else transcription)

        if not args.skip_8_concurrent:
            print(f"\n{'#'*60}")
            print(f"# CONCURRENT 8 TEST{prompt_label}")
            print(f"{'#'*60}")
            conc8_latencies, total_time8, conc8_timings = benchmark_concurrent(
                args.url, str(audio_path), 8, 8, prompt_context, label=f"CONCURRENT 8{prompt_label}"
            )
            print_stats(conc8_latencies, f"CONCURRENT 8{prompt_label}", total_time8)
            print_timing_stats(conc8_timings, f"CONCURRENT 8{prompt_label}")
            print_timeline(conc8_timings, f"CONCURRENT 8{prompt_label}")

        if not args.skip_concurrent:
            print(f"\n{'#'*60}")
            print(f"# CONCURRENT 16 TEST{prompt_label}")
            print(f"{'#'*60}")
            conc_latencies, total_time, conc_timings = benchmark_concurrent(
                args.url, str(audio_path), args.concurrent_requests, args.max_workers, prompt_context, label=f"CONCURRENT 16{prompt_label}"
            )
            print_stats(conc_latencies, f"CONCURRENT 16{prompt_label}", total_time)
            print_timing_stats(conc_timings, f"CONCURRENT 16{prompt_label}")
            print_timeline(conc_timings, f"CONCURRENT 16{prompt_label}")

        if not args.skip_256_concurrent:
            print(f"\n{'#'*60}")
            print(f"# CONCURRENT 256 TEST{prompt_label}")
            print(f"{'#'*60}")
            conc256_latencies, total_time256, conc256_timings = benchmark_concurrent(
                args.url, str(audio_path), args.concurrent_256_requests, args.max_workers_256, prompt_context, verbose=False, label=f"CONCURRENT 256{prompt_label}"
            )
            print_stats(conc256_latencies, f"CONCURRENT 256{prompt_label}", total_time256)
            print_timing_stats(conc256_timings, f"CONCURRENT 256{prompt_label}")
            print_timeline(conc256_timings, f"CONCURRENT 256{prompt_label}")

    print(f"\n{'='*60}")
    print("TEST COMPLETE")
    print(f"{'='*60}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

