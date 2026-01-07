#!/bin/bash
#SBATCH --job-name=whisper-eval
#SBATCH --output=logs/whisper_eval_%j.out
#SBATCH --error=logs/whisper_eval_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gpus-per-node=1
#SBATCH --mem=64G
#SBATCH --exclude=airvmds001-a4u-12,airvmds001-a4u-17
#SBATCH --time=01:00:00
#SBATCH --partition=a4u

# =============================================================================
# Whisper Checkpoint Evaluation SLURM Script
# =============================================================================
#
# Usage Examples:
#
#   # Evaluate a specific checkpoint:
#   DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset \
#   CHECKPOINT_PATH=/mnt/lustre/.../whisper-checkpoints/whisper-finetune-337 \
#   sbatch slurm_evaluate_whisper.sh
#
#   # Evaluate base model (no checkpoint):
#   DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset \
#   sbatch slurm_evaluate_whisper.sh
#
#   # Quick test with limited samples:
#   DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset \
#   CHECKPOINT_PATH=/path/to/checkpoint \
#   MAX_SAMPLES=50 \
#   sbatch slurm_evaluate_whisper.sh
#
#   # Compare base vs fine-tuned:
#   DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset \
#   COMPARE_BASE=1 \
#   CHECKPOINT_PATH=/path/to/checkpoint \
#   sbatch slurm_evaluate_whisper.sh
#
#   # Include default reference (base model) in same evaluation:
#   DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset \
#   CHECKPOINT_PATH=/path/to/checkpoint \
#   INCLUDE_DEFAULT_REFERENCE=1 \
#   sbatch slurm_evaluate_whisper.sh
#
# Environment Variables:
#   DATASET_PATH            - Path to HuggingFace dataset (REQUIRED)
#   CHECKPOINT_PATH         - Path to fine-tuned checkpoint (optional, uses base if not set)
#   MODEL_ID                - Base model ID (default: openai/whisper-large-v3-turbo)
#   MAX_SAMPLES             - Limit samples for quick testing (optional)
#   USE_CONTEXT             - Set to 1 to use context field (default: 0)
#   USE_LANGUAGE            - Set to 1 to force language from dataset (default: 0)
#   INCLUDE_CONTEXT_VARIANTS - Set to 1 to include both context/no-context completions when context exists (default: 1)
#   OUTPUT_DIR              - Directory for output files (default: ./eval_results)
#   COMPARE_BASE            - Set to 1 to also evaluate base model for comparison
#   INCLUDE_DEFAULT_REFERENCE - Set to 1 to include base model as reference in same eval (default: 0)
#   CONDA_ENV               - Conda environment name (default: whisper-ft)
#
# =============================================================================



# Example cmd:
# DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset CHECKPOINT_PATH=/mnt/lustre/airvmds001lstre/aginart/checkpoints/whisper-checkpoints/whisper-finetune-478 INCLUDE_DEFAULT_REFERENCE=1 INCLUDE_CONTEXT_VARIANTS=1 sbatch slurm_evaluate_whisper.sh


set -e

# Job info
JOB_SUFFIX="${SLURM_JOB_ID:-local}"
echo "=============================================="
echo "Whisper Evaluation Job: ${JOB_SUFFIX}"
echo "=============================================="
echo "Start time: $(date)"
echo "Hostname: $(hostname)"
echo "Working directory: $(pwd)"

# Create logs directory
mkdir -p logs

# Configuration with defaults
MODEL_ID=${MODEL_ID:-"openai/whisper-large-v3-turbo"}
OUTPUT_DIR=${OUTPUT_DIR:-"./eval_results"}
CONDA_ENV=${CONDA_ENV:-"whisper-ft"}
USE_CONTEXT=${USE_CONTEXT:-0}
USE_LANGUAGE=${USE_LANGUAGE:-0}
INCLUDE_CONTEXT_VARIANTS=${INCLUDE_CONTEXT_VARIANTS:-1}
COMPARE_BASE=${COMPARE_BASE:-0}
INCLUDE_DEFAULT_REFERENCE=${INCLUDE_DEFAULT_REFERENCE:-0}

# Validate required parameters
if [ -z "${DATASET_PATH}" ]; then
    echo "ERROR: DATASET_PATH environment variable is required"
    echo "Example: DATASET_PATH=~/slackbot-inference/tts_out/hf_dataset sbatch slurm_evaluate_whisper.sh"
    exit 1
fi

# Expand paths
DATASET_PATH=$(eval echo "${DATASET_PATH}")
if [ -n "${CHECKPOINT_PATH}" ]; then
    CHECKPOINT_PATH=$(eval echo "${CHECKPOINT_PATH}")
fi
OUTPUT_DIR=$(eval echo "${OUTPUT_DIR}")

# Print configuration
echo ""
echo "Configuration:"
echo "  DATASET_PATH: ${DATASET_PATH}"
echo "  CHECKPOINT_PATH: ${CHECKPOINT_PATH:-'(using base model)'}"
echo "  MODEL_ID: ${MODEL_ID}"
echo "  OUTPUT_DIR: ${OUTPUT_DIR}"
echo "  MAX_SAMPLES: ${MAX_SAMPLES:-'(all)'}"
echo "  USE_CONTEXT: ${USE_CONTEXT}"
echo "  USE_LANGUAGE: ${USE_LANGUAGE}"
echo "  INCLUDE_CONTEXT_VARIANTS: ${INCLUDE_CONTEXT_VARIANTS}"
echo "  COMPARE_BASE: ${COMPARE_BASE}"
echo "  INCLUDE_DEFAULT_REFERENCE: ${INCLUDE_DEFAULT_REFERENCE}"
echo ""

# Validate paths
if [ ! -d "${DATASET_PATH}" ]; then
    echo "ERROR: Dataset path does not exist: ${DATASET_PATH}"
    exit 1
fi

if [ -n "${CHECKPOINT_PATH}" ] && [ ! -d "${CHECKPOINT_PATH}" ]; then
    echo "ERROR: Checkpoint path does not exist: ${CHECKPOINT_PATH}"
    exit 1
fi

# Create output directory
mkdir -p "${OUTPUT_DIR}"

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

# Build base command
CMD="python evaluate_checkpoint.py"
CMD="${CMD} --dataset_path ${DATASET_PATH}"
CMD="${CMD} --model_id ${MODEL_ID}"

if [ -n "${MAX_SAMPLES}" ]; then
    CMD="${CMD} --max_samples ${MAX_SAMPLES}"
fi

if [ "${USE_CONTEXT}" = "1" ]; then
    CMD="${CMD} --use_context"
fi

if [ "${USE_LANGUAGE}" = "1" ]; then
    CMD="${CMD} --use_language"
fi

if [ "${INCLUDE_CONTEXT_VARIANTS}" = "1" ]; then
    CMD="${CMD} --include_context_variants"
fi

if [ "${INCLUDE_DEFAULT_REFERENCE}" = "1" ]; then
    CMD="${CMD} --include_default_reference"
fi

# Run base model evaluation if COMPARE_BASE is set or no checkpoint provided
if [ "${COMPARE_BASE}" = "1" ] || [ -z "${CHECKPOINT_PATH}" ]; then
    echo "=============================================="
    echo "Evaluating BASE model: ${MODEL_ID}"
    echo "=============================================="
    
    BASE_OUTPUT="${OUTPUT_DIR}/eval_base_${JOB_SUFFIX}.json"
    BASE_CMD="${CMD} --output_file ${BASE_OUTPUT}"
    
    echo "Command: ${BASE_CMD}"
    echo ""
    
    eval "${BASE_CMD}"
    
    echo ""
    echo "Base model results saved to: ${BASE_OUTPUT}"
    echo ""
fi

# Run checkpoint evaluation if provided
if [ -n "${CHECKPOINT_PATH}" ]; then
    echo "=============================================="
    echo "Evaluating CHECKPOINT: ${CHECKPOINT_PATH}"
    echo "=============================================="
    
    CKPT_NAME=$(basename "${CHECKPOINT_PATH}")
    CKPT_OUTPUT="${OUTPUT_DIR}/eval_${CKPT_NAME}_${JOB_SUFFIX}.json"
    CKPT_CMD="${CMD} --checkpoint_path ${CHECKPOINT_PATH} --output_file ${CKPT_OUTPUT}"
    
    echo "Command: ${CKPT_CMD}"
    echo ""
    
    eval "${CKPT_CMD}"
    
    echo ""
    echo "Checkpoint results saved to: ${CKPT_OUTPUT}"
fi

# Summary comparison if both were run
if [ "${COMPARE_BASE}" = "1" ] && [ -n "${CHECKPOINT_PATH}" ]; then
    echo ""
    echo "=============================================="
    echo "COMPARISON SUMMARY"
    echo "=============================================="
    
    if command -v python3 &> /dev/null; then
        python3 << EOF
import json
import sys

try:
    with open("${BASE_OUTPUT}") as f:
        base = json.load(f)["summary"]
    with open("${CKPT_OUTPUT}") as f:
        ckpt = json.load(f)["summary"]
    
    print(f"{'Metric':<25} {'Base Model':>15} {'Checkpoint':>15} {'Improvement':>15}")
    print("-" * 70)
    
    for metric in ["avg_wer", "avg_cer", "exact_match_accuracy"]:
        base_val = base[metric]
        ckpt_val = ckpt[metric]
        
        if metric in ["avg_wer", "avg_cer"]:
            # Lower is better
            improvement = base_val - ckpt_val
            pct = (improvement / base_val * 100) if base_val > 0 else 0
            sign = "+" if improvement > 0 else ""
            print(f"{metric:<25} {base_val:>14.4f} {ckpt_val:>14.4f} {sign}{improvement:>+.4f} ({pct:+.1f}%)")
        else:
            # Higher is better
            improvement = ckpt_val - base_val
            pct = (improvement / base_val * 100) if base_val > 0 else 0
            sign = "+" if improvement > 0 else ""
            print(f"{metric:<25} {base_val:>14.4f} {ckpt_val:>14.4f} {sign}{improvement:>+.4f} ({pct:+.1f}%)")
    
    print("-" * 70)
except Exception as e:
    print(f"Could not generate comparison: {e}")
EOF
    fi
fi

echo ""
echo "=============================================="
echo "Evaluation completed at $(date)"
echo "=============================================="
