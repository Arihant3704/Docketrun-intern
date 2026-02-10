#!/bin/bash

# Navigate to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if a virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating venv..."
    source venv/bin/activate
elif [ -d "env" ]; then
    echo "Activating env..."
    source env/bin/activate
fi

# Run the Python script
echo "Running run_prompt_inference.py..."
python run_prompt_inference.py

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
    echo "Deactivated virtual environment."
fi
