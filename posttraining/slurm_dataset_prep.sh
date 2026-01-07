#!/bin/bash
#SBATCH --job-name=whisper-dataset-prep
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=50
#SBATCH --exclude=airvmds001-a4u-17
#SBATCH --mem=0
#SBATCH --time=4:00:00
#SBATCH --partition=a4u
#SBATCH --output=logs/dataset_prep_%j.out
#SBATCH --error=logs/dataset_prep_%j.err

set -euo pipefail

# Get script directory
if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  SCRIPT_DIR="${SLURM_SUBMIT_DIR}"
else
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

# --- User configuration -------------------------------------------------------
MODEL_ID=${MODEL_ID:-"openai/whisper-large-v3-turbo"}
DATASET_NAME=${DATASET_NAME:-"simon3000/genshin-voice"}
LANGUAGE_OPTION=${LANGUAGE_OPTION:-"auto"}  # "auto" or "dataset"

# Output configuration
if [[ -n "${SLURM_JOB_ID:-}" ]]; then
  JOB_SUFFIX="${SLURM_JOB_ID}"
else
  JOB_SUFFIX="$(date +%Y%m%d_%H%M%S)"
fi
OUTPUT_PATH=${OUTPUT_PATH:-"/mnt/lustre/airvmds001lstre/aginart/datasets/whisper-prepared-${JOB_SUFFIX}"}
CACHE_DIR=${CACHE_DIR:-"/home/aginart_salesforce_com/.cache/huggingface"}

PREP_SCRIPT="${SCRIPT_DIR}/dataset_prep.py"

# Verify the script exists
if [[ ! -f "${PREP_SCRIPT}" ]]; then
  echo "[$(date)] ERROR: Dataset prep script not found at ${PREP_SCRIPT}"
  echo "[$(date)] Current directory: $(pwd)"
  echo "[$(date)] SLURM_SUBMIT_DIR: ${SLURM_SUBMIT_DIR:-not set}"
  echo "[$(date)] Script directory: ${SCRIPT_DIR}"
  exit 1
fi

# --- Diagnostics --------------------------------------------------------------
echo "[$(date)] ============================================================"
echo "[$(date)] WHISPER DATASET PREPARATION"
echo "[$(date)] ============================================================"
echo "[$(date)] SLURM job ${SLURM_JOB_ID:-unknown} launching on ${SLURM_JOB_NODELIST:-local}"
echo "[$(date)] Script directory: ${SCRIPT_DIR}"
echo "[$(date)] Prep script: ${PREP_SCRIPT}"
echo "[$(date)] Model: ${MODEL_ID}"
echo "[$(date)] Dataset: ${DATASET_NAME}"
echo "[$(date)] Output path: ${OUTPUT_PATH}"
echo "[$(date)] CPUs allocated: ${SLURM_CPUS_PER_TASK:-50}"
echo "[$(date)] Queue snapshot:"
squeue --me || true
echo

# --- Environment setup --------------------------------------------------------
CONDA_BASE="${CONDA_BASE:-/fsx/home/aginart/miniconda3}"
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
    echo "[$(date)] ERROR: conda command not found."
    exit 1
  fi
fi

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

# Disable Python output buffering for real-time logs
export PYTHONUNBUFFERED=1

# Set number of threads for parallel processing
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-50}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-50}

echo "[$(date)] ============================================================"
echo "[$(date)] CONFIGURATION"
echo "[$(date)] ============================================================"
echo "[$(date)] Model ID: ${MODEL_ID}"
echo "[$(date)] Dataset: ${DATASET_NAME}"
echo "[$(date)] Language option: ${LANGUAGE_OPTION}"
echo "[$(date)] Output path: ${OUTPUT_PATH}"
echo "[$(date)] Parallel workers: ${SLURM_CPUS_PER_TASK:-50}"
echo "[$(date)] ============================================================"
echo

mkdir -p "$(dirname "${OUTPUT_PATH}")"
mkdir -p logs

# --- Launch -------------------------------------------------------------------
echo "[$(date)] Launching dataset preparation..."
echo

srun --cpu-bind=cores python "${PREP_SCRIPT}" \
  --model_id "${MODEL_ID}" \
  --dataset_name "${DATASET_NAME}" \
  --language_option "${LANGUAGE_OPTION}" \
  --output_path "${OUTPUT_PATH}"

echo
echo "[$(date)] ============================================================"
echo "[$(date)] Dataset preparation completed successfully!"
echo "[$(date)] ============================================================"
echo "[$(date)] Prepared dataset saved to: ${OUTPUT_PATH}"
echo "[$(date)] "
echo "[$(date)] To use in training, load with:"
echo "[$(date)]   from datasets import load_from_disk"
echo "[$(date)]   dataset = load_from_disk('${OUTPUT_PATH}')"
echo "[$(date)] ============================================================"
echo



