#!/bin/bash
# ALIAS Universal Launch Script

echo "🤖 ALIAS - Advanced Learning Intelligence Assistant System"
echo "=========================================================="
echo

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python detected"

# Install minimal requirements if needed
if ! $PYTHON_CMD -c "import requests" &> /dev/null; then
    echo "📦 Installing minimal requirements..."
    pip install requests
fi

echo "🚀 Starting ALIAS..."
echo
echo "Features: Voice • 7 AI Modes • 50+ Tools • 100% FREE"
echo "Keyboard: Ctrl+Enter (send) | Ctrl+L (voice) | Ctrl+M (mode) | F1 (help)"
echo

$PYTHON_CMD alias.py
