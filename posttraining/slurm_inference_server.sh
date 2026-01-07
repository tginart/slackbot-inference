#!/bin/bash
#SBATCH --job-name=whisper-inference
#SBATCH --output=logs/whisper_inference_%j.out
#SBATCH --error=logs/whisper_inference_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=32
#SBATCH --gpus-per-node=8
#SBATCH --mem=128G
#SBATCH --exclude=airvmds001-a4u-12,airvmds001-a4u-17
#SBATCH --time=24:00:00
#SBATCH --partition=a4u

# =============================================================================
# Whisper Inference Server SLURM Script
# =============================================================================
#
# Usage:
#   PORT=8080 NUM_WORKERS=8 sbatch slurm_inference_server.sh
#
#   # Use a checkpoint:
#   MODEL_ID=/mnt/lustre/.../whisper-finetune-530 PORT=8080 NUM_WORKERS=8 sbatch slurm_inference_server.sh
#
# Environment Variables:
#   PORT              - Server port (default: 8080)
#   NUM_WORKERS       - Number of GPU worker processes (default: 8)
#   CONDA_ENV         - Conda environment name (default: whisper-ft)
#   MODEL_ID          - Model ID or checkpoint path (default: openai/whisper-large-v3-turbo)
#
# After submission, use the helper script to set up port forwarding:
#   ./setup_port_forward.sh <job_id>
#
# =============================================================================

set -euo pipefail

# Get script directory
if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  SCRIPT_DIR="${SLURM_SUBMIT_DIR}"
else
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

# Configuration with defaults
PORT=${PORT:-8080}
NUM_WORKERS=${NUM_WORKERS:-8}
CONDA_ENV=${CONDA_ENV:-"whisper-ft"}
MODEL_ID=${MODEL_ID:-"openai/whisper-large-v3-turbo"}

# Get the node name where this job is running
NODE_NAME=$(scontrol show hostnames "${SLURM_JOB_NODELIST}" | head -n 1)

# Create logs directory
mkdir -p logs

# Job info
echo "=============================================="
echo "Whisper Inference Server Job: ${SLURM_JOB_ID}"
echo "=============================================="
echo "Start time: $(date)"
echo "Node: ${NODE_NAME}"
echo "Hostname: $(hostname)"
echo "Working directory: $(pwd)"
echo "Port: ${PORT}"
echo "Workers: ${NUM_WORKERS}"
echo "Model: ${MODEL_ID}"
echo ""
echo "=============================================="
echo "CONNECTION INFORMATION"
echo "=============================================="
echo "Server is running on node: ${NODE_NAME}"
echo "Server port: ${PORT}"
echo ""
echo "To set up port forwarding from login node, run:"
echo "  ssh -L ${PORT}:${NODE_NAME}:${PORT} ${NODE_NAME} -N"
echo ""
echo "Or use the helper script:"
echo "  ./setup_port_forward.sh ${SLURM_JOB_ID}"
echo "=============================================="
echo ""

# Activate conda environment
echo "Activating conda environment: ${CONDA_ENV}"
source ~/miniconda3/etc/profile.d/conda.sh || source /opt/conda/etc/profile.d/conda.sh || true
conda activate "${CONDA_ENV}" || {
    echo "Warning: Failed to activate conda env ${CONDA_ENV}, trying default python"
}

# Show GPU info
echo ""
echo "GPU Information:"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
echo ""

# Find inference_server.py (check common locations)
INFERENCE_SCRIPT=""
if [[ -f "${SCRIPT_DIR}/../inference_server.py" ]]; then
  INFERENCE_SCRIPT="${SCRIPT_DIR}/../inference_server.py"
elif [[ -f "${SCRIPT_DIR}/inference_server.py" ]]; then
  INFERENCE_SCRIPT="${SCRIPT_DIR}/inference_server.py"
elif [[ -f "./inference_server.py" ]]; then
  INFERENCE_SCRIPT="./inference_server.py"
else
  echo "ERROR: Could not find inference_server.py"
  echo "Searched:"
  echo "  ${SCRIPT_DIR}/../inference_server.py"
  echo "  ${SCRIPT_DIR}/inference_server.py"
  echo "  ./inference_server.py"
  exit 1
fi

echo "Using inference script: ${INFERENCE_SCRIPT}"
echo ""

# Run the inference server
echo "=============================================="
echo "Starting Whisper Inference Server"
echo "=============================================="
echo "Command: python ${INFERENCE_SCRIPT} --port ${PORT} --num-workers ${NUM_WORKERS} --model-id ${MODEL_ID}"
echo ""

python "${INFERENCE_SCRIPT}" --port "${PORT}" --num-workers "${NUM_WORKERS}" --model-id "${MODEL_ID}"

echo ""
echo "=============================================="
echo "Inference server stopped at $(date)"
echo "=============================================="

