#!/bin/bash
# VS Code terminal auto-activation script for workshop venv

# Source the default bashrc first
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Get the workspace folder (parent of .vscode)
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Activate the virtual environment
if [ -f "$WORKSPACE_DIR/venv/bin/activate" ]; then
    source "$WORKSPACE_DIR/venv/bin/activate"
    echo "Virtual environment activated: $WORKSPACE_DIR/venv"
fi

# Change to workspace directory
cd "$WORKSPACE_DIR"
