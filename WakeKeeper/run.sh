#!/bin/bash
# WakeKeeper 启动脚本
# 用法：bash run.sh
set -e
cd "$(dirname "$0")"

# 确保 uv 在 PATH 中
export PATH="$HOME/.local/bin:$PATH"

uv run python main.py
