# slackbot-inference


### Installation

See `requirements.txt`. If you are on Hyperpod, you can also look at `/fsx/home/aginart/miniconda3/envs/project-sleeper/bin/python` to get the exact python env.

### Server (local)

To run server: 

`python inference_server.py`

Assumes 8 Hopper GPUs are available on the serving node.

### Endpoints

- `GET /health`: legacy health check
- `GET /ping`: SageMaker-style health check
- `POST /transcribe`: multipart upload (`audio`) + optional form field `context`
- `POST /invocations`: SageMaker inference endpoint (raw audio bytes or JSON base64)

### SageMaker container

This repo can be built as a BYOC (bring-your-own-container) image for Amazon SageMaker.

- The container listens on port `8080`
- Health check: `GET /ping`
- Inference: `POST /invocations`

Build:

`docker build -t slackbot-inference:latest .`

Run:

`docker run --gpus all -p 8080:8080 slackbot-inference:latest`

Example invocation (raw wav bytes):

`curl -sS -X POST "http://localhost:8080/invocations" -H "Content-Type: audio/wav" --data-binary @MLKDream_20s.wav`

Example invocation (JSON base64):

`python - << 'PY'
import base64, json, pathlib, requests
p = pathlib.Path("MLKDream_20s.wav")
payload = {"audio_base64": base64.b64encode(p.read_bytes()).decode("ascii"), "audio_format": "wav"}
print(requests.post("http://localhost:8080/invocations", json=payload, timeout=600).json())
PY`

### Benchmarking

Start server and then on the node run `python test_server.py`.

See `test_results.txt` for reference performance numbers from Hyperpod (12/17/25).

### Custom Prompt Prefill

Support for benchmarking purposes but not supported by base whisper model. Fine-tuning in progress...

### TODOs

- Add support for more audio formats beyond `.wav` / `.webm`





