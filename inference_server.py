"""
Whisper Inference Server with Multi-GPU Workers (improved)

Key fixes vs original:
  - Caps CPU thread pools per worker process (prevents oversubscription under concurrency)
  - Replaces Manager().dict() + 1ms polling with response_queue + asyncio.Future
  - Adds CUDA-event GPU-only timing for generate()

Endpoints:
  POST /transcribe    - Multipart upload (.wav or .webm) with optional context
  GET  /health        - Health check (legacy)
  GET  /ping          - SageMaker health check
  POST /invocations   - SageMaker inference endpoint (raw audio bytes or JSON base64)

Usage:
  python inference_server.py --port 8000 --num-workers 8
"""

import os

# -----------------------------------------------------------------------------
# IMPORTANT: set threadpool caps BEFORE importing torch/numpy/librosa/transformers
# -----------------------------------------------------------------------------
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("NUMBA_NUM_THREADS", "1")

import uuid
import tempfile
import argparse
import asyncio
import base64
import logging
import time
import threading
from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse

import multiprocessing as mp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("whisper-server")

# ============================================================================
# Configuration
# ============================================================================

MODEL_ID = "openai/whisper-large-v3-turbo"
MAX_QUEUE_SIZE = 10000
REQUEST_TIMEOUT = 600  # seconds

# Global reference time for timeline
SERVER_START_TIME = time.perf_counter()

# ============================================================================
# Worker Process
# ============================================================================

def worker_main(
    worker_id: int,
    gpu_id: int,
    request_queue: "mp.Queue",
    response_queue: "mp.Queue",
):
    """
    Worker process that loads model on a specific GPU and processes requests.
    """
    worker_logger = logging.getLogger(f"worker-{worker_id}")
    worker_logger.info(f"Starting worker {worker_id} on GPU {gpu_id}")

    try:
        import numpy as np
        import subprocess
        import torch
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        import librosa

        # Hard cap torch CPU threads inside each worker (critical for concurrency)
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)

        # Device setup
        device = torch.device(f"cuda:{gpu_id}")
        torch.cuda.set_device(gpu_id)

        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

        # Increase dynamo cache for variable sequence lengths (optional)
        try:
            import torch._dynamo
            torch._dynamo.config.cache_size_limit = 128
        except Exception:
            pass

        # Load model + processor
        worker_logger.info(f"Loading model {MODEL_ID}...")
        processor = WhisperProcessor.from_pretrained(MODEL_ID)
        model = WhisperForConditionalGeneration.from_pretrained(MODEL_ID, torch_dtype=dtype)
        model.config.forced_decoder_ids = None
        model.to(device)
        model.eval()

        # Compile model (optional)
        try:
            compiled_model = torch.compile(
                model,
                mode="reduce-overhead",
                fullgraph=False,
                dynamic=True,
            )
            worker_logger.info("Model compiled successfully")
        except Exception as e:
            compiled_model = model
            worker_logger.warning(f"torch.compile failed, using eager mode: {e}")

        # Warmup
        worker_logger.info("Warming up model...")
        dummy_audio = np.zeros(16000, dtype=np.float32)  # 1 second silence
        dummy_inputs = processor(dummy_audio, sampling_rate=16000, return_tensors="pt")
        dummy_features = dummy_inputs.input_features.to(device, non_blocking=True)

        with torch.inference_mode(), torch.autocast(device_type="cuda", dtype=dtype):
            _ = compiled_model.generate(
                dummy_features,
                do_sample=False,
                num_beams=1,
                temperature=0.0,
            )
        torch.cuda.synchronize()

        actual_device = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(actual_device)
        worker_logger.info(f"Worker {worker_id} ready on cuda:{gpu_id} (actual: {actual_device}, {device_name})")

        # Main processing loop
        while True:
            request = request_queue.get()
            if request is None:  # Shutdown signal
                break

            request_id = request["request_id"]
            audio_path = request["audio_path"]
            context = request.get("context")
            language = request.get("language")  # Optional: force specific language
            queued_at = request.get("queued_at", 0.0)
            server_start = request.get("server_start", queued_at)

            picked_up_time = time.perf_counter()
            queue_wait_ms = (picked_up_time - queued_at) * 1000 if queued_at else 0.0

            try:
                # ---------------------
                # Load audio (CPU)
                # ---------------------
                t0 = time.perf_counter()
                ext = os.path.splitext(audio_path)[1].lower()
                if ext == ".webm":
                    cmd = [
                        "ffmpeg",
                        "-hide_banner",
                        "-loglevel", "error",
                        "-i", audio_path,
                        "-f", "f32le",
                        "-ac", "1",
                        "-ar", "16000",
                        "pipe:1",
                    ]
                    proc = subprocess.run(cmd, capture_output=True, check=False)
                    if proc.returncode != 0:
                        raise RuntimeError(
                            f"ffmpeg decode failed (rc={proc.returncode}): {proc.stderr.decode('utf-8', errors='replace')}"
                        )
                    audio_array = np.frombuffer(proc.stdout, dtype=np.float32)
                    if audio_array.size == 0:
                        raise RuntimeError("ffmpeg decode produced empty audio")
                else:
                    audio_array, _sr = librosa.load(audio_path, sr=16000, mono=True)
                t_load = time.perf_counter()

                # ---------------------
                # Preprocess (CPU -> GPU)
                # ---------------------
                inputs = processor(audio_array, sampling_rate=16000, return_tensors="pt")
                input_features = inputs.input_features.to(device, non_blocking=True)
                t_preprocess = time.perf_counter()

                # prompt_ids (optional context)
                prompt_ids = None
                if context is not None and context.strip():
                    # get_prompt_ids properly prepends <|startofprev|> token
                    prompt_ids = processor.get_prompt_ids(context, return_tensors="pt").to(device)

                # forced_decoder_ids (optional language forcing)
                # When language is specified, force the model to use that language
                # instead of auto-detecting from audio
                forced_decoder_ids = None
                if language is not None and language.strip():
                    # Returns list of (position, token_id) tuples like [(1, lang_id), (2, task_id)]
                    forced_decoder_ids = processor.get_decoder_prompt_ids(
                        language=language.strip().lower(),
                        task="transcribe"
                    )

                # ---------------------
                # Generate (GPU + CPU orchestration)
                # Add CUDA-event timing for GPU-only measurement
                # ---------------------
                generate_kwargs = {
                    "do_sample": False,
                    "num_beams": 1,
                    "temperature": 0.0,
                }
                if prompt_ids is not None:
                    generate_kwargs["prompt_ids"] = prompt_ids
                if forced_decoder_ids is not None:
                    generate_kwargs["forced_decoder_ids"] = forced_decoder_ids

                torch.cuda.synchronize()
                t_pre_generate = time.perf_counter()

                start_evt = torch.cuda.Event(enable_timing=True)
                end_evt = torch.cuda.Event(enable_timing=True)

                start_evt.record()
                with torch.inference_mode(), torch.autocast(device_type="cuda", dtype=dtype):
                    predicted_ids = compiled_model.generate(input_features, **generate_kwargs)
                end_evt.record()

                torch.cuda.synchronize()
                t_post_generate = time.perf_counter()

                gpu_generate_ms = float(start_evt.elapsed_time(end_evt))
                wall_generate_ms = (t_post_generate - t_pre_generate) * 1000.0

                # ---------------------
                # Decode (CPU)
                # ---------------------
                predicted_ids_cpu = predicted_ids.detach().cpu()
                transcription = processor.batch_decode(predicted_ids_cpu, skip_special_tokens=True)[0]
                t_decode = time.perf_counter()

                # Durations
                load_ms = (t_load - t0) * 1000.0
                preprocess_ms = (t_preprocess - t_load) * 1000.0
                decode_ms = (t_decode - t_post_generate) * 1000.0
                total_worker_ms = (t_decode - t0) * 1000.0

                # Absolute timeline (ms from server start)
                timeline = {
                    "picked_up": round((picked_up_time - server_start) * 1000, 1),
                    "load_start": round((t0 - server_start) * 1000, 1),
                    "load_end": round((t_load - server_start) * 1000, 1),
                    "preprocess_end": round((t_preprocess - server_start) * 1000, 1),
                    "generate_start": round((t_pre_generate - server_start) * 1000, 1),
                    "generate_end": round((t_post_generate - server_start) * 1000, 1),
                    "done": round((t_decode - server_start) * 1000, 1),
                }

                # Log
                worker_logger.info(
                    f"Request {request_id} W{worker_id} GPU{gpu_id} "
                    f"q={queue_wait_ms:.0f}ms ld={load_ms:.0f}ms pp={preprocess_ms:.0f}ms "
                    f"gen_wall={wall_generate_ms:.0f}ms gen_gpu={gpu_generate_ms:.0f}ms "
                    f"dec={decode_ms:.0f}ms total={total_worker_ms:.0f}ms | "
                    f"TIMELINE gen=[{timeline['generate_start']:.0f}-{timeline['generate_end']:.0f}]"
                )

                result = {
                    "transcription": transcription,
                    "error": None,
                    "done": True,
                    "worker_done_at": time.perf_counter(),
                    "timing": {
                        "worker_id": worker_id,
                        "gpu_id": gpu_id,
                        "queue_wait_ms": round(queue_wait_ms, 1),
                        "load_ms": round(load_ms, 1),
                        "preprocess_ms": round(preprocess_ms, 1),
                        "generate_wall_ms": round(wall_generate_ms, 1),
                        "generate_gpu_ms": round(gpu_generate_ms, 1),
                        "decode_ms": round(decode_ms, 1),
                        "total_worker_ms": round(total_worker_ms, 1),
                        "timeline": timeline,
                    },
                }

                response_queue.put((request_id, result))

            except Exception as e:
                worker_logger.exception(f"Error processing request {request_id}: {e}")
                response_queue.put((request_id, {
                    "transcription": None,
                    "error": str(e),
                    "done": True,
                    "timing": {
                        "worker_id": worker_id,
                        "gpu_id": gpu_id,
                    }
                }))
            finally:
                # Clean up temp audio file
                try:
                    if audio_path and os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception:
                    pass

    except Exception as e:
        worker_logger.exception(f"Worker {worker_id} failed to initialize: {e}")
        raise

    worker_logger.info(f"Worker {worker_id} shutting down")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Whisper Inference Server",
    description="Multi-GPU Whisper transcription service",
    version="2.0.0",
)

# Global state
ctx: Optional[mp.context.BaseContext] = None
request_queue: Optional["mp.Queue"] = None
response_queue: Optional["mp.Queue"] = None
workers: list[mp.Process] = []

pending_futures: Dict[str, asyncio.Future] = {}
pending_lock = threading.Lock()
response_thread: Optional[threading.Thread] = None


def _response_pump(loop: asyncio.AbstractEventLoop):
    """
    Runs in a background thread.
    Drains response_queue and completes the matching asyncio.Future.
    """
    global response_queue, pending_futures

    while True:
        item = response_queue.get()
        if item is None:
            break

        request_id, result = item

        with pending_lock:
            fut = pending_futures.pop(request_id, None)

        if fut is not None and not fut.done():
            try:
                loop.call_soon_threadsafe(fut.set_result, result)
            except RuntimeError:
                # event loop is closed
                pass


@app.on_event("startup")
async def startup_event():
    """Initialize queues, response pump, and workers on startup."""
    global ctx, request_queue, response_queue, workers, response_thread

    num_workers = int(os.environ.get("NUM_WORKERS", "8"))

    # Use a dedicated spawn context (works well with CUDA)
    ctx = mp.get_context("spawn")

    # Discover GPUs without importing torch globally at module import time
    try:
        import torch
        num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 0
    except Exception:
        num_gpus = int(os.environ.get("NUM_GPUS", "0"))

    if num_gpus <= 0:
        raise RuntimeError("No CUDA GPUs detected (torch.cuda.device_count() == 0).")

    num_workers = min(num_workers, num_gpus)
    logger.info(f"Starting {num_workers} workers on {num_gpus} GPUs")

    request_queue = ctx.Queue(maxsize=MAX_QUEUE_SIZE)
    response_queue = ctx.Queue(maxsize=MAX_QUEUE_SIZE)

    loop = asyncio.get_running_loop()
    response_thread = threading.Thread(target=_response_pump, args=(loop,), daemon=True)
    response_thread.start()

    workers = []
    for i in range(num_workers):
        gpu_id = i % num_gpus
        p = ctx.Process(
            target=worker_main,
            args=(i, gpu_id, request_queue, response_queue),
            daemon=True,
        )
        p.start()
        workers.append(p)
        logger.info(f"Started worker {i} (PID: {p.pid}) on GPU {gpu_id}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up workers and background response thread."""
    global workers, request_queue, response_queue, response_thread, pending_futures

    logger.info("Shutting down...")

    # Fail any in-flight requests
    with pending_lock:
        for req_id, fut in list(pending_futures.items()):
            if not fut.done():
                fut.set_exception(HTTPException(status_code=503, detail="Server shutting down"))
        pending_futures.clear()

    # Stop workers
    if request_queue is not None:
        for _ in workers:
            try:
                request_queue.put(None, timeout=1)
            except Exception:
                pass

    for w in workers:
        w.join(timeout=5)
        if w.is_alive():
            w.terminate()

    # Stop response pump thread
    if response_queue is not None:
        try:
            response_queue.put(None, timeout=1)
        except Exception:
            pass

    if response_thread is not None:
        response_thread.join(timeout=2)

    logger.info("All workers shut down")


@app.get("/health")
async def health_check():
    alive_workers = sum(1 for w in workers if w.is_alive())
    return {
        "status": "healthy" if alive_workers > 0 else "degraded",
        "workers_alive": alive_workers,
        "workers_total": len(workers),
    }

@app.get("/ping")
async def ping():
    """
    SageMaker health check endpoint.
    SageMaker expects HTTP 200 for a healthy container.
    """
    alive_workers = sum(1 for w in workers if w.is_alive())
    if alive_workers <= 0:
        raise HTTPException(status_code=503, detail="No workers available")
    return {"status": "ok", "workers_alive": alive_workers, "workers_total": len(workers)}


async def _run_transcription(
    audio_bytes: bytes,
    suffix: str,
    context: Optional[str],
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Shared request path for /transcribe and /invocations.
    Writes bytes to a temp file, enqueues to a GPU worker, and awaits the result.
    
    Args:
        audio_bytes: Raw audio file bytes
        suffix: File extension (.wav or .webm)
        context: Optional context/prompt text for conditioning transcription
        language: Optional language code (e.g., "en", "es", "zh") to force.
                  If None, auto-detects language from audio.
    """
    if request_queue is None or response_queue is None:
        raise HTTPException(status_code=503, detail="Server not initialized yet")

    # Check workers
    alive_workers = sum(1 for w in workers if w.is_alive())
    if alive_workers == 0:
        raise HTTPException(status_code=503, detail="No workers available to process request")

    request_id = str(uuid.uuid4())

    # Save audio to temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, prefix=f"whisper_{request_id}_") as tmp:
            tmp.write(audio_bytes)
            audio_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save audio bytes: {e}")

    # Create per-request future
    loop = asyncio.get_running_loop()
    fut = loop.create_future()

    with pending_lock:
        pending_futures[request_id] = fut

    # Enqueue request
    queued_at = time.perf_counter()
    request_data = {
        "request_id": request_id,
        "audio_path": audio_path,
        "context": context,
        "language": language,
        "queued_at": queued_at,
        "server_start": SERVER_START_TIME,
    }

    try:
        request_queue.put(request_data, timeout=5)
    except Exception:
        with pending_lock:
            pending_futures.pop(request_id, None)
        try:
            os.remove(audio_path)
        except Exception:
            pass
        raise HTTPException(status_code=503, detail="Request queue is full. Please try again later.")

    # Await response (no polling)
    try:
        result = await asyncio.wait_for(fut, timeout=REQUEST_TIMEOUT)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out waiting for transcription")
    finally:
        with pending_lock:
            pending_futures.pop(request_id, None)

    # Error handling
    if result.get("error"):
        raise HTTPException(status_code=500, detail=f"Transcription failed: {result['error']}")

    # Add HTTP timing
    response_received_at = time.perf_counter()
    http_wait_ms = (response_received_at - queued_at) * 1000.0

    response_data: Dict[str, Any] = {
        "request_id": request_id,
        "transcription": result["transcription"],
    }
    if "timing" in result:
        response_data["timing"] = dict(result["timing"])
        response_data["timing"]["http_wait_ms"] = round(http_wait_ms, 1)

    return response_data


@app.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(..., description="Audio file (.wav or .webm)"),
    context: Optional[str] = Form(None, description="Optional context/prompt text"),
    language: Optional[str] = Form(None, description="Optional language code (e.g., 'en', 'es', 'zh'). If not specified, auto-detects from audio."),
):
    # Validate extension
    filename = audio.filename or ""
    if not filename.lower().endswith((".wav", ".webm")):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .wav or .webm supported.")
    suffix = ".wav" if filename.lower().endswith(".wav") else ".webm"
    audio_bytes = await audio.read()
    response_data = await _run_transcription(audio_bytes=audio_bytes, suffix=suffix, context=context, language=language)
    return JSONResponse(response_data)


@app.post("/invocations")
async def invocations(request: Request):
    """
    SageMaker inference endpoint.

    Supported request formats:
      - Raw bytes with Content-Type: audio/wav, audio/webm, application/octet-stream
      - JSON with base64 audio:
          {
            "audio_base64": "<base64>",
            "audio_format": "wav" | "webm",   // optional, defaults to "wav"
            "context": "optional prompt",
            "language": "en" | "es" | ...     // optional, auto-detects if not specified
          }
    """
    content_type = (request.headers.get("content-type") or "").lower()

    # JSON payload
    if "application/json" in content_type:
        try:
            payload = await request.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="JSON body must be an object")

        audio_b64 = payload.get("audio_base64") or payload.get("audio")
        if not audio_b64:
            raise HTTPException(status_code=400, detail="Missing 'audio_base64' (or 'audio') in JSON body")

        audio_format = (payload.get("audio_format") or "wav").lower()
        if audio_format not in ("wav", "webm"):
            raise HTTPException(status_code=400, detail="audio_format must be 'wav' or 'webm'")

        try:
            audio_bytes = base64.b64decode(audio_b64, validate=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 audio: {e}")

        context = payload.get("context")
        language = payload.get("language")  # Optional language code
        suffix = ".wav" if audio_format == "wav" else ".webm"
        return JSONResponse(await _run_transcription(audio_bytes=audio_bytes, suffix=suffix, context=context, language=language))

    # Raw bytes payload
    audio_bytes = await request.body()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty request body")

    # Infer suffix from content-type; default to wav if unknown.
    if "audio/webm" in content_type:
        suffix = ".webm"
    else:
        suffix = ".wav"

    return JSONResponse(await _run_transcription(audio_bytes=audio_bytes, suffix=suffix, context=None))


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper Inference Server")
    # SageMaker expects the container to listen on 8080 by default.
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8080")), help="Server port")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host")
    parser.add_argument("--num-workers", type=int, default=8, help="Number of worker processes")
    args = parser.parse_args()

    os.environ["NUM_WORKERS"] = str(args.num_workers)
    os.environ["PORT"] = str(args.port)

    logger.info(f"Starting Whisper Inference Server on {args.host}:{args.port}")
    logger.info(f"Configured for {args.num_workers} workers")

    # NOTE: Do NOT run uvicorn with multiple server workers for this design.
    # Use a single FastAPI/uvicorn process that spawns GPU workers itself.
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info",
        workers=1,
    )

