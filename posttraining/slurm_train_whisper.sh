#!/bin/bash
#SBATCH --job-name=whisper-finetune
#SBATCH --nodes=1
#SBATCH --gpus-per-node=8
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=96
#SBATCH --exclude=airvmds001-a4u-12,airvmds001-a4u-17
#SBATCH --mem=0
#SBATCH --time=24:00:00
#SBATCH --partition=a4u
#SBATCH --output=logs/whisper_finetune_%j.out
#SBATCH --error=logs/whisper_finetune_%j.err

set -euo pipefail

# Example command: DATASET_PATH=/mnt/lustre/airvmds001lstre/aginart/datasets/whisper-assembled-jan-6-hf sbatch slurm_train_whisper.sh

# Get script directory - use SLURM_SUBMIT_DIR if available (where sbatch was run from)
# Otherwise fall back to the directory containing this script
if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  SCRIPT_DIR="${SLURM_SUBMIT_DIR}"
else
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

# --- User configuration -------------------------------------------------------
# Model configuration
MODEL_ID=${MODEL_ID:-"openai/whisper-large-v3-turbo"}
DATASET_NAME=${DATASET_NAME:-"simon3000/genshin-voice"}
# DATASET_PATH: Local path to a HuggingFace dataset directory (overrides DATASET_NAME)
# Supports raw audio format (audio, context, transcription, language) or preprocessed format
DATASET_PATH=${DATASET_PATH:-""}
LANGUAGE_OPTION=${LANGUAGE_OPTION:-"dataset"}  # "auto" or "dataset"

# Output configuration
# Append job ID or datetime to prevent overwriting
if [[ -n "${SLURM_JOB_ID:-}" ]]; then
  JOB_SUFFIX="${SLURM_JOB_ID}"
else
  JOB_SUFFIX="$(date +%Y%m%d_%H%M%S)"
fi
OUTPUT_DIR=${OUTPUT_DIR:-"/mnt/lustre/airvmds001lstre/aginart/checkpoints/whisper-checkpoints/whisper-finetune-${JOB_SUFFIX}"}
LOG_DIR=${LOG_DIR:-"${OUTPUT_DIR}/tensorboard"}
CACHE_DIR=${CACHE_DIR:-"/home/aginart_salesforce_com/hf-cache"}

# Training hyperparameters
BATCH_SIZE=${BATCH_SIZE:-16}
LEARNING_RATE=${LEARNING_RATE:-1e-50} # tiny LR
NUM_EPOCHS=${NUM_EPOCHS:-1}
MAX_STEPS=${MAX_STEPS:-""}  # Leave empty to use num_epochs, or set to a number
SAVE_STEPS=${SAVE_STEPS:-1000}
LOGGING_STEPS=${LOGGING_STEPS:-10}  # Log every 10 steps (use lower value for small datasets)

# Resume from checkpoint (optional)
RESUME_FROM=${RESUME_FROM:-""}

TRAIN_SCRIPT="${SCRIPT_DIR}/train.py"

# Verify the training script exists
if [[ ! -f "${TRAIN_SCRIPT}" ]]; then
  echo "[$(date)] ERROR: Training script not found at ${TRAIN_SCRIPT}"
  echo "[$(date)] Current directory: $(pwd)"
  echo "[$(date)] SLURM_SUBMIT_DIR: ${SLURM_SUBMIT_DIR:-not set}"
  echo "[$(date)] Script directory: ${SCRIPT_DIR}"
  exit 1
fi

# --- Diagnostics --------------------------------------------------------------
echo "[$(date)] ============================================================"
echo "[$(date)] WHISPER FINE-TUNING"
echo "[$(date)] ============================================================"
echo "[$(date)] SLURM job ${SLURM_JOB_ID:-unknown} launching on ${SLURM_JOB_NODELIST:-local}"
echo "[$(date)] Script directory: ${SCRIPT_DIR}"
echo "[$(date)] Training script: ${TRAIN_SCRIPT}"
echo "[$(date)] Model: ${MODEL_ID}"
if [[ -n "${DATASET_PATH}" ]]; then
  echo "[$(date)] Dataset path: ${DATASET_PATH} (local)"
else
  echo "[$(date)] Dataset: ${DATASET_NAME} (HuggingFace Hub)"
fi
echo "[$(date)] Output directory: ${OUTPUT_DIR}"
echo "[$(date)] Queue snapshot:"
squeue --me || true
echo
echo "[$(date)] Partition summary:"
sinfo || true
echo
if [[ -n "${SLURM_JOB_ID:-}" ]]; then
  echo "[$(date)] Job detail:"
  scontrol show job "${SLURM_JOB_ID}" || true
  echo
fi

# --- Environment setup --------------------------------------------------------
# Activate conda environment
CONDA_BASE="${CONDA_BASE:-/fsx/home/aginart/miniconda3}"
# Try alternative paths if miniconda3 doesn't exist
if [[ ! -d "${CONDA_BASE}" ]]; then
  CONDA_BASE="/fsx/home/aginart/anaconda3"
fi
if [[ ! -d "${CONDA_BASE}" ]]; then
  CONDA_BASE="${HOME}/miniconda3"
fi
if [[ ! -d "${CONDA_BASE}" ]]; then
  CONDA_BASE="${HOME}/anaconda3"
fi

if [[ -f "${CONDA_BASE}/etc/profile.d/conda.sh" ]]; then
  source "${CONDA_BASE}/etc/profile.d/conda.sh"
  echo "[$(date)] Sourced conda from: ${CONDA_BASE}/etc/profile.d/conda.sh"
else
  echo "[$(date)] WARNING: Could not find conda.sh. Trying to use conda from PATH..."
  if ! command -v conda &> /dev/null; then
    echo "[$(date)] ERROR: conda command not found. Please ensure conda is installed and accessible."
    exit 1
  fi
fi

# Activate the conda environment (adjust name as needed)
CONDA_ENV=${CONDA_ENV:-"whisper-ft"}
if conda env list | grep -q "^${CONDA_ENV} "; then
  conda activate "${CONDA_ENV}"
  echo "[$(date)] Activated conda environment: ${CONDA_ENV}"
  echo "[$(date)] Python path: $(which python)"
  echo "[$(date)] Python version: $(python --version 2>&1)"
else
  echo "[$(date)] WARNING: Conda environment '${CONDA_ENV}' not found. Using base."
  conda activate base
fi

export HF_HOME="${CACHE_DIR}"
export TRANSFORMERS_CACHE="${CACHE_DIR}"
export PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"

# Show GPU info
echo "[$(date)] ============================================================"
echo "[$(date)] GPU INFORMATION"
echo "[$(date)] ============================================================"
nvidia-smi || true
echo

echo "[$(date)] ============================================================"
echo "[$(date)] TRAINING CONFIGURATION"
echo "[$(date)] ============================================================"
echo "[$(date)] Model ID: ${MODEL_ID}"
if [[ -n "${DATASET_PATH}" ]]; then
  echo "[$(date)] Dataset path: ${DATASET_PATH} (local)"
else
  echo "[$(date)] Dataset: ${DATASET_NAME} (HuggingFace Hub)"
fi
echo "[$(date)] Language option: ${LANGUAGE_OPTION}"
echo
echo "[$(date)] Hyperparameters:"
echo "[$(date)]   Batch size (per GPU): ${BATCH_SIZE}"
echo "[$(date)]   Learning rate: ${LEARNING_RATE}"
echo "[$(date)]   Number of epochs: ${NUM_EPOCHS}"
if [[ -n "${MAX_STEPS}" ]]; then
  echo "[$(date)]   Max steps: ${MAX_STEPS}"
fi
echo "[$(date)]   Save steps: ${SAVE_STEPS}"
echo "[$(date)]   Logging steps: ${LOGGING_STEPS}"
echo
echo "[$(date)] Directories:"
echo "[$(date)]   Output directory: ${OUTPUT_DIR}"
echo "[$(date)]   TensorBoard logs: ${LOG_DIR}"
if [[ -n "${RESUME_FROM}" ]]; then
  echo "[$(date)]   Resuming from: ${RESUME_FROM}"
fi
echo "[$(date)] ============================================================"
echo

mkdir -p "${OUTPUT_DIR}"
mkdir -p "${LOG_DIR}"
mkdir -p logs

# --- Launch -------------------------------------------------------------------
echo "[$(date)] Launching training..."
echo

# Build command with optional arguments
CMD=(
  python "${TRAIN_SCRIPT}"
  --model_id "${MODEL_ID}"
  --language_option "${LANGUAGE_OPTION}"
  --output_dir "${OUTPUT_DIR}"
  --log_dir "${LOG_DIR}"
  --batch_size "${BATCH_SIZE}"
  --learning_rate "${LEARNING_RATE}"
  --num_epochs "${NUM_EPOCHS}"
  --save_steps "${SAVE_STEPS}"
  --logging_steps "${LOGGING_STEPS}"
)

# Use local dataset path if provided, otherwise use HuggingFace Hub dataset name
if [[ -n "${DATASET_PATH}" ]]; then
  CMD+=(--dataset_path "${DATASET_PATH}")
else
  CMD+=(--dataset_name "${DATASET_NAME}")
fi

if [[ -n "${MAX_STEPS}" ]]; then
  CMD+=(--max_steps "${MAX_STEPS}")
fi

if [[ -n "${RESUME_FROM}" ]]; then
  CMD+=(--resume_from "${RESUME_FROM}")
fi

# Run the training script
# Using srun for proper SLURM integration even on single node
srun --cpu-bind=cores "${CMD[@]}"

echo
echo "[$(date)] ============================================================"
echo "[$(date)] Training completed successfully!"
echo "[$(date)] ============================================================"
echo "[$(date)] Model saved to: ${OUTPUT_DIR}"
echo "[$(date)] TensorBoard logs: ${LOG_DIR}"
echo "[$(date)] "
echo "[$(date)] View training metrics:"
echo "[$(date)]   tensorboard --logdir ${LOG_DIR} --port 6006"
echo "[$(date)] ============================================================"
echo



