FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3-pip \
    ca-certificates \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 11

WORKDIR /opt/program

COPY requirements.txt /opt/program/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -U pip && \
    python3.11 -m pip install --no-cache-dir -r /opt/program/requirements.txt

COPY inference_server.py /opt/program/inference_server.py

EXPOSE 8080

CMD ["sh", "-c", "python3.11 inference_server.py --host 0.0.0.0 --port ${PORT}"]


