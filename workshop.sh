#!/bin/bash
#
# 有心工坊启动脚本
# 快速启动发布系统，包含配置检查和环境验证
#

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"

# 打印信息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查虚拟环境
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        print_error "虚拟环境不存在: $VENV_PATH"
        print_info "运行: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
}

# 检查Python版本
check_python_version() {
    PYTHON="$VENV_PATH/bin/python3"
    if [ ! -f "$PYTHON" ]; then
        PYTHON="$VENV_PATH/bin/python"
    fi

    if [ ! -f "$PYTHON" ]; then
        print_error "找不到Python: $PYTHON"
        exit 1
    fi

    # 检查Python版本（需要3.8+）
    VERSION=$("$PYTHON" -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    print_success "Python版本: $VERSION"
}

# 快速配置检查（可选，不阻塞启动）
quick_config_check() {
    # 检查.env文件
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        print_warning ".env文件不存在"
        print_info "建议运行: cp .env.example .env"
        echo
    fi

    # 检查关键配置文件
    if [ ! -f "$PROJECT_ROOT/config/app.yml" ]; then
        print_warning "主配置文件缺失: config/app.yml"
        echo
    fi
}

# 显示帮助信息
show_help() {
    cat << 'EOF'
有心工坊 - 一键发布系统

使用:
  workshop              # 启动发布系统
  workshop --help       # 显示帮助
  workshop --check      # 完整配置检查
  workshop --version    # 显示版本信息

快速链接:
  文档导航: DOCS_MAP.md
  快速开始: QUICKSTART.md
  故障排查: TROUBLESHOOTING.md

配置工具:
  python scripts/tools/validate_config.py          # 验证配置
  python scripts/tools/config_standardization.py   # 配置检查
  bash scripts/tools/prepare_migration.sh          # 准备迁移

EOF
}

# 完整配置检查
full_config_check() {
    print_info "运行完整配置检查..."
    echo

    cd "$PROJECT_ROOT"
    source "$VENV_PATH/bin/activate"

    if python scripts/tools/validate_config.py; then
        echo
        print_success "配置检查通过！"
    else
        echo
        print_warning "配置检查发现问题，请根据提示修复"
        print_info "详细信息: TROUBLESHOOTING.md"
        exit 1
    fi
}

# 显示版本信息
show_version() {
    cat << 'EOF'
有心工坊 (YouXin Workshop) v2.0
- 基于Jekyll的自动化博客发布系统
- 多平台内容分发 + 图片管理 + 会员服务

项目地址: https://github.com/zhurong2020/workshop
文档: README.md | DOCS_MAP.md
EOF
}

# 主函数
main() {
    # 处理参数
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --check|-c)
            check_venv
            check_python_version
            full_config_check
            exit 0
            ;;
        --version|-v)
            show_version
            exit 0
            ;;
        "")
            # 正常启动
            ;;
        *)
            print_error "未知参数: $1"
            echo
            show_help
            exit 1
            ;;
    esac

    # 启动系统
    print_info "启动有心工坊..."
    echo

    # 基本检查
    check_venv
    check_python_version
    quick_config_check

    # 进入项目目录
    cd "$PROJECT_ROOT"

    # 激活虚拟环境并运行
    source "$VENV_PATH/bin/activate"

    # 运行主程序
    python run.py "$@"
}

# 执行主函数
main "$@"
