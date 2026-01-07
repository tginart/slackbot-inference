#!/bin/bash
# =============================================================================
# Port Forwarding Helper for SLURM Inference Server
# =============================================================================
#
# This script sets up SSH port forwarding from the login node to a worker node
# running a SLURM job. It can also provide instructions for chaining forwarding
# from your local desktop.
#
# Usage:
#   ./setup_port_forward.sh <job_id> [local_port]
#
# Examples:
#   # Forward to default port 8080 on login node
#   ./setup_port_forward.sh 12345
#
#   # Forward to custom port 9000 on login node
#   ./setup_port_forward.sh 12345 9000
#
#   # Check if forwarding is already set up
#   ./setup_port_forward.sh 12345 --check
#
#   # Kill existing forwarding
#   ./setup_port_forward.sh 12345 --kill
#
# =============================================================================

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <job_id> [local_port] [--check|--kill]"
    echo ""
    echo "Examples:"
    echo "  $0 12345              # Forward job 12345's port to 8080 on login node"
    echo "  $0 12345 9000         # Forward to port 9000 on login node"
    echo "  $0 12345 --check      # Check if forwarding is active"
    echo "  $0 12345 --kill       # Kill existing forwarding"
    exit 1
fi

JOB_ID="$1"

# Parse arguments - handle --check and --kill flags
if [[ "${2:-}" == "--check" ]] || [[ "${2:-}" == "--kill" ]]; then
    LOCAL_PORT="${3:-8080}"
    ACTION="${2}"
elif [[ "${3:-}" == "--check" ]] || [[ "${3:-}" == "--kill" ]]; then
    LOCAL_PORT="${2:-8080}"
    ACTION="${3}"
else
    LOCAL_PORT="${2:-8080}"
    ACTION="${3:-forward}"
fi

# Get job information
if ! scontrol show job "${JOB_ID}" &>/dev/null; then
    echo "ERROR: Job ${JOB_ID} not found or not accessible"
    exit 1
fi

# Extract node name from job
# Use squeue first (more reliable), fallback to scontrol
NODE_NAME=$(squeue -j "${JOB_ID}" -h -o "%N" 2>/dev/null | head -n 1 | xargs)

# If squeue didn't work or returned empty/null, try scontrol
if [[ -z "${NODE_NAME}" ]] || [[ "${NODE_NAME}" == "(null)" ]] || [[ "${NODE_NAME}" == "NODELIST" ]]; then
    NODE_LIST=$(scontrol show job "${JOB_ID}" 2>/dev/null | grep "^   NodeList=" | awk -F'=' '{print $2}' | awk '{print $1}')
    if [[ -n "${NODE_LIST}" ]] && [[ "${NODE_LIST}" != "(null)" ]]; then
        # If NodeList contains a range or list, get first hostname
        NODE_NAME=$(scontrol show hostnames "${NODE_LIST}" 2>/dev/null | head -n 1)
    fi
fi

# Final validation
if [[ -z "${NODE_NAME}" ]] || [[ "${NODE_NAME}" == "(null)" ]] || [[ "${NODE_NAME}" == "NODELIST" ]]; then
    echo "ERROR: Could not determine node name for job ${JOB_ID}"
    echo "Job may not be running yet or hasn't been allocated a node."
    echo ""
    echo "Job status:"
    squeue -j "${JOB_ID}" 2>/dev/null || echo "Job not found in queue"
    echo ""
    echo "Full job info:"
    scontrol show job "${JOB_ID}" 2>/dev/null | grep -E "JobState|NodeList|NodeName" || true
    exit 1
fi

# Try to get the port from the job's output file
JOB_OUTPUT=$(scontrol show job "${JOB_ID}" | grep -oP "StdOut=\K[^\s]+" || echo "")
SERVER_PORT="${LOCAL_PORT}"  # Default to same port

if [[ -n "${JOB_OUTPUT}" ]] && [[ -f "${JOB_OUTPUT}" ]]; then
    # Try to extract port from job output
    EXTRACTED_PORT=$(grep -oP "Server port: \K[0-9]+" "${JOB_OUTPUT}" | head -n 1 || echo "")
    if [[ -n "${EXTRACTED_PORT}" ]]; then
        SERVER_PORT="${EXTRACTED_PORT}"
    fi
fi

# If port wasn't found, try common defaults
if [[ "${SERVER_PORT}" == "${LOCAL_PORT}" ]]; then
    SERVER_PORT="8080"
fi

echo "=============================================="
echo "Port Forwarding Setup"
echo "=============================================="
echo "Job ID: ${JOB_ID}"
echo "Worker Node: ${NODE_NAME}"
echo "Server Port (on worker): ${SERVER_PORT}"
echo "Local Port (on login node): ${LOCAL_PORT}"
echo "=============================================="
echo ""

# Check if job is running
JOB_STATE=$(squeue -j "${JOB_ID}" -h -o "%T" 2>/dev/null || echo "NOT_FOUND")
if [[ "${JOB_STATE}" == "NOT_FOUND" ]] || [[ -z "${JOB_STATE}" ]]; then
    echo "WARNING: Job ${JOB_ID} not found in queue. It may have completed or not started yet."
    echo ""
fi

case "${ACTION}" in
    --check)
        # Check if port forwarding is already running
        if pgrep -f "ssh.*-L.*${LOCAL_PORT}:localhost:${SERVER_PORT}.*${NODE_NAME}" > /dev/null; then
            echo "✓ Port forwarding is ACTIVE"
            echo ""
            echo "Active forwarding processes:"
            ps aux | grep -E "ssh.*-L.*${LOCAL_PORT}:localhost:${SERVER_PORT}.*${NODE_NAME}" | grep -v grep || true
        else
            echo "✗ Port forwarding is NOT active"
            echo ""
            echo "To start forwarding, run:"
            echo "  $0 ${JOB_ID} ${LOCAL_PORT}"
        fi
        ;;
    
    --kill)
        # Kill existing port forwarding
        PIDS=$(pgrep -f "ssh.*-L.*${LOCAL_PORT}:localhost:${SERVER_PORT}.*${NODE_NAME}" || true)
        if [[ -n "${PIDS}" ]]; then
            echo "Killing port forwarding processes: ${PIDS}"
            echo "${PIDS}" | xargs kill 2>/dev/null || true
            echo "✓ Port forwarding stopped"
        else
            echo "No active port forwarding found"
        fi
        ;;
    
    forward)
        # Check if forwarding already exists
        if pgrep -f "ssh.*-L.*${LOCAL_PORT}:localhost:${SERVER_PORT}.*${NODE_NAME}" > /dev/null; then
            echo "WARNING: Port forwarding already appears to be active!"
            echo ""
            echo "Active processes:"
            ps aux | grep -E "ssh.*-L.*${LOCAL_PORT}:localhost:${SERVER_PORT}.*${NODE_NAME}" | grep -v grep || true
            echo ""
            echo "To kill existing forwarding: $0 ${JOB_ID} ${LOCAL_PORT} --kill"
            echo "To check status: $0 ${JOB_ID} ${LOCAL_PORT} --check"
            exit 1
        fi
        
        # Start port forwarding in background
        echo "Starting SSH port forwarding..."
        echo "Command: ssh -L ${LOCAL_PORT}:localhost:${SERVER_PORT} ${NODE_NAME} -N -f"
        echo ""
        
        # Use -N (no remote command), -f (background), and -o ExitOnForwardFailure=yes
        # Forward localhost:${LOCAL_PORT} (on login node) -> localhost:${SERVER_PORT} (on worker node)
        if ssh -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=no \
             -L "${LOCAL_PORT}:localhost:${SERVER_PORT}" \
             "${NODE_NAME}" -N -f 2>&1; then
            echo "✓ Port forwarding started successfully!"
            echo ""
            echo "Forwarding: localhost:${LOCAL_PORT} -> ${NODE_NAME}:${SERVER_PORT}"
            echo ""
            echo "Test the connection:"
            echo "  curl http://localhost:${LOCAL_PORT}/ping"
            echo ""
            echo "To check status: $0 ${JOB_ID} ${LOCAL_PORT} --check"
            echo "To stop forwarding: $0 ${JOB_ID} ${LOCAL_PORT} --kill"
            echo ""
            echo "=============================================="
            echo "Chaining from Local Desktop"
            echo "=============================================="
            echo "To forward from your local desktop to login node, run on your desktop:"
            echo ""
            echo "  ssh -L ${LOCAL_PORT}:localhost:${LOCAL_PORT} <login_node_hostname> -N"
            echo ""
            echo "Then access the server at: http://localhost:${LOCAL_PORT}"
            echo ""
        else
            echo "✗ Failed to start port forwarding"
            echo ""
            echo "Possible reasons:"
            echo "  1. Job may not be running yet (check with: squeue -j ${JOB_ID})"
            echo "  2. Server may not be listening on port ${SERVER_PORT}"
            echo "  3. SSH connection to ${NODE_NAME} failed"
            echo ""
            echo "Check job logs:"
            JOB_OUTPUT=$(scontrol show job "${JOB_ID}" | grep -oP "StdOut=\K[^\s]+" || echo "")
            if [[ -n "${JOB_OUTPUT}" ]] && [[ -f "${JOB_OUTPUT}" ]]; then
                echo "  tail -f ${JOB_OUTPUT}"
            fi
            exit 1
        fi
        ;;
    
    *)
        echo "ERROR: Unknown action: ${ACTION}"
        exit 1
        ;;
esac

