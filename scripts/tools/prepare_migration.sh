#!/bin/bash
#
# 一键迁移准备脚本
# 自动打包所有必要的配置文件，准备迁移到新机器
#

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印信息
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

# 函数：检查文件是否存在
check_file() {
    local file=$1
    local description=$2

    if [ -f "$file" ]; then
        print_success "$description: $file"
        return 0
    else
        print_warning "$description 不存在: $file"
        return 1
    fi
}

# 主函数
main() {
    echo "======================================================================"
    echo "🚀 有心工坊 - 环境迁移准备工具"
    echo "======================================================================"
    echo ""

    # 1. 确定项目根目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

    print_info "项目根目录: $PROJECT_ROOT"

    # 2. 创建迁移目录
    MIGRATION_DIR="$HOME/migration-package-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$MIGRATION_DIR"
    print_success "创建迁移目录: $MIGRATION_DIR"

    echo ""
    echo "----------------------------------------------------------------------"
    echo "📦 阶段1：打包Workshop项目敏感配置"
    echo "----------------------------------------------------------------------"

    cd "$PROJECT_ROOT"

    # 检查必需文件
    files_exist=true

    if ! check_file ".env" ".env配置文件"; then
        files_exist=false
    fi

    # 打包workshop配置
    if [ "$files_exist" = true ]; then
        print_info "正在打包workshop敏感配置..."

        tar -czf "$MIGRATION_DIR/workshop-secrets.tar.gz" \
            .env \
            $([ -f config/onedrive_tokens.json ] && echo "config/onedrive_tokens.json" || echo "") \
            $([ -f config/youtube_oauth_credentials.json ] && echo "config/youtube_oauth_credentials.json" || echo "") \
            $([ -f config/youtube_oauth_token.json ] && echo "config/youtube_oauth_token.json" || echo "") \
            2>/dev/null || true

        print_success "Workshop配置已打包"
    else
        print_error "缺少必需文件，跳过workshop配置打包"
    fi

    echo ""
    echo "----------------------------------------------------------------------"
    echo "🔧 阶段2：打包系统级配置"
    echo "----------------------------------------------------------------------"

    cd "$HOME"

    # 检查系统配置
    system_files=()

    if [ -d ".cloudflare" ]; then
        system_files+=(".cloudflare")
        print_success "找到Cloudflare配置"
    fi

    if [ -d ".ssh" ]; then
        system_files+=(".ssh")
        print_success "找到SSH配置"
    fi

    if [ -d ".config/gh" ]; then
        system_files+=(".config/gh")
        print_success "找到GitHub CLI配置"
    fi

    if [ -f ".gitconfig" ]; then
        system_files+=(".gitconfig")
        print_success "找到Git配置"
    fi

    if [ ${#system_files[@]} -gt 0 ]; then
        print_info "正在打包系统配置..."
        tar -czf "$MIGRATION_DIR/system-configs.tar.gz" "${system_files[@]}"
        print_success "系统配置已打包"
    else
        print_warning "未找到系统配置文件"
    fi

    echo ""
    echo "----------------------------------------------------------------------"
    echo "🤖 阶段3：打包Claude配置"
    echo "----------------------------------------------------------------------"

    if [ -f "$HOME/.claude/.credentials.json" ]; then
        print_info "正在打包Claude配置..."
        tar -czf "$MIGRATION_DIR/claude-config.tar.gz" \
            -C "$HOME" \
            .claude/.credentials.json
        print_success "Claude配置已打包"
    else
        print_warning "未找到Claude配置"
    fi

    echo ""
    echo "----------------------------------------------------------------------"
    echo "📋 阶段4：导出Python依赖"
    echo "----------------------------------------------------------------------"

    # Workshop依赖
    if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
        print_info "导出workshop Python依赖..."
        source "$PROJECT_ROOT/venv/bin/activate"
        pip freeze > "$MIGRATION_DIR/workshop-requirements.txt"
        deactivate
        print_success "Workshop依赖已导出"
    else
        print_warning "未找到workshop虚拟环境"
    fi

    # Cardiac依赖（如果存在）
    CARDIAC_DIR="$HOME/projects/cardiac-ml-research"
    if [ -d "$CARDIAC_DIR" ]; then
        echo ""
        print_info "检测到cardiac-ml-research项目..."

        # 打包cardiac配置
        if [ -d "$CARDIAC_DIR/config" ]; then
            print_info "正在打包cardiac配置..."
            cd "$CARDIAC_DIR"
            tar -czf "$MIGRATION_DIR/cardiac-configs.tar.gz" \
                config/ \
                2>/dev/null || true
            print_success "Cardiac配置已打包"
        fi

        # 导出cardiac依赖
        if [ -f "$CARDIAC_DIR/.venv/bin/activate" ]; then
            print_info "导出cardiac Python依赖..."
            source "$CARDIAC_DIR/.venv/bin/activate"
            pip freeze > "$MIGRATION_DIR/cardiac-requirements.txt"
            deactivate
            print_success "Cardiac依赖已导出"
        fi
    fi

    echo ""
    echo "----------------------------------------------------------------------"
    echo "📝 阶段5：生成迁移清单"
    echo "----------------------------------------------------------------------"

    # 创建迁移清单
    cat > "$MIGRATION_DIR/MIGRATION_CHECKLIST.md" << 'EOF'
# 迁移清单

## 📦 已打包内容

### Workshop项目
- [ ] workshop-secrets.tar.gz - 敏感配置（.env, OAuth tokens等）
- [ ] workshop-requirements.txt - Python依赖列表

### Cardiac项目（如适用）
- [ ] cardiac-configs.tar.gz - 配置文件和License
- [ ] cardiac-requirements.txt - Python依赖列表

### 系统配置
- [ ] system-configs.tar.gz - SSH, Git, Cloudflare, GitHub CLI配置
- [ ] claude-config.tar.gz - Claude Code认证

## 🔍 迁移前验证

在旧机器上运行以下命令验证配置完整性：

```bash
cd ~/projects/personal/websites/workshop
source venv/bin/activate
python scripts/tools/validate_config.py
```

## 📋 迁移到新机器的步骤

### 1. 传输迁移包
将整个 migration-package 目录传输到新机器（建议使用U盘）

### 2. 新机器基础环境设置
```bash
# 安装基础工具
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3.12 python3.12-venv python3-pip gh

# 安装Claude Code CLI（访问官网获取最新安装方法）
```

### 3. 恢复系统配置
```bash
cd ~
tar -xzf ~/migration-package-*/system-configs.tar.gz
tar -xzf ~/migration-package-*/claude-config.tar.gz

# 设置权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/*.pem
chmod 644 ~/.ssh/id_ed25519.pub ~/.ssh/config
```

### 4. 克隆并配置Workshop项目
```bash
mkdir -p ~/projects
cd ~/projects
git clone git@github.com:zhurong2020/workshop.git
cd workshop

# 恢复敏感配置
tar -xzf ~/migration-package-*/workshop-secrets.tar.gz

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 验证配置
python scripts/tools/validate_config.py
```

### 5. 验证核心功能
```bash
# SSH连接
ssh -T git@github.com
ssh arong-vps "echo 'OK'"

# Git配置
git config --global --list

# GitHub CLI
gh auth status

# Claude Code
claude --version
```

## ⚠️ 注意事项

1. **传输安全**：使用U盘物理传输最安全
2. **权限设置**：SSH密钥必须是600权限
3. **Token刷新**：某些OAuth token可能需要重新认证
4. **备份保留**：在新环境验证成功前，保留旧机器配置

## 📚 详细文档

参见: docs/MIGRATION_GUIDE.md

---

生成时间: $(date)
来源机器: $(hostname)
EOF

    print_success "迁移清单已创建"

    echo ""
    echo "----------------------------------------------------------------------"
    echo "📊 打包汇总"
    echo "----------------------------------------------------------------------"

    echo ""
    print_info "迁移包内容："
    ls -lh "$MIGRATION_DIR/"

    echo ""
    total_size=$(du -sh "$MIGRATION_DIR" | cut -f1)
    print_success "迁移包总大小: $total_size"
    print_success "迁移包位置: $MIGRATION_DIR"

    echo ""
    echo "======================================================================"
    echo "✅ 迁移准备完成！"
    echo "======================================================================"
    echo ""
    print_info "下一步操作："
    echo "  1. 查看迁移包: cd $MIGRATION_DIR"
    echo "  2. 查看迁移清单: cat $MIGRATION_DIR/MIGRATION_CHECKLIST.md"
    echo "  3. 传输到新机器（建议使用U盘）"
    echo "  4. 在新机器上按照 docs/MIGRATION_GUIDE.md 操作"
    echo ""
    print_warning "重要：在新环境验证成功前，不要删除旧机器上的配置！"
    echo ""
}

# 执行主函数
main "$@"
