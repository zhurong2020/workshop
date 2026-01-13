#!/bin/bash
# 有心工坊 - 便捷启动脚本
# 使用虚拟环境运行 run.py

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# 激活虚拟环境并运行
"$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/run.py" "$@"
