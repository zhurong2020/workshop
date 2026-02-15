# 快速迁移参考卡片

> 📌 **一页纸搞定环境迁移** - 常用命令速查表

## 🚀 旧机器：准备迁移包（3分钟）

```bash
# 1. 进入项目目录
cd ~/projects/personal/websites/workshop

# 2. 验证配置完整性（可选）
source venv/bin/activate
python scripts/tools/validate_config.py

# 3. 生成迁移包（一键完成）
bash scripts/tools/prepare_migration.sh

# 4. 记录迁移包位置
# 输出中会显示：迁移包位置: /home/wuxia/migration-package-YYYYMMDD-HHMMSS

# 5. 传输到新机器（使用U盘最安全）
```

## 💻 新机器：环境恢复（10分钟）

### 基础环境（3分钟）
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具（一行命令）
sudo apt install -y git python3.12 python3.12-venv python3-pip gh build-essential curl wget

# 安装Claude Code CLI（访问官网）
# https://docs.anthropic.com/claude/docs/claude-code
```

### 恢复配置（2分钟）
```bash
# 假设迁移包在 ~/Downloads/migration-package-YYYYMMDD-HHMMSS/

# 解压系统配置
cd ~
tar -xzf ~/Downloads/migration-package-*/system-configs.tar.gz
tar -xzf ~/Downloads/migration-package-*/claude-config.tar.gz

# 设置权限（重要！）
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/*.pem
chmod 644 ~/.ssh/id_ed25519.pub ~/.ssh/config
```

### Workshop项目（5分钟）
```bash
# 克隆项目
mkdir -p ~/projects && cd ~/projects
git clone git@github.com:zhurong2020/workshop.git
cd workshop

# 恢复敏感配置
tar -xzf ~/Downloads/migration-package-*/workshop-secrets.tar.gz

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 验证配置
python scripts/tools/validate_config.py
```

## ✅ 验证清单（2分钟）

```bash
# 1. SSH连接
ssh -T git@github.com                      # 应显示：Hi username! You've successfully authenticated
ssh arong-vps "echo 'OK'"                  # 应显示：OK

# 2. Git和GitHub
git config --global --list                 # 检查用户名和邮箱
gh auth status                             # 应显示：Logged in

# 3. Claude和工具
claude --version                           # 应显示：2.1.x
python run.py                              # 应正常启动

# 4. 完整验证
cd ~/projects/personal/websites/workshop && source venv/bin/activate
python scripts/tools/validate_config.py    # 应显示：🎉 所有必需配置已就绪！
```

## 🔧 常见问题速查

### SSH权限问题
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/*.pem
chmod 644 ~/.ssh/id_ed25519.pub ~/.ssh/config
```

### GitHub认证问题
```bash
gh auth login
# 选择：GitHub.com → SSH → 使用现有密钥
```

### Python虚拟环境问题
```bash
cd ~/projects/personal/websites/workshop
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### OneDrive Token过期
```bash
cd ~/projects/personal/websites/workshop && source venv/bin/activate
python scripts/tools/onedrive_auth.py
# 按提示完成OAuth认证
```

## 📦 迁移包内容清单

| 文件 | 内容 | 大小 |
|------|------|------|
| `workshop-secrets.tar.gz` | .env, OAuth tokens | ~5KB |
| `system-configs.tar.gz` | SSH, Git, Cloudflare, GH CLI | ~6KB |
| `claude-config.tar.gz` | Claude认证 | ~1KB |
| `cardiac-configs.tar.gz` | Cardiac配置和License | ~23KB |
| `workshop-requirements.txt` | Python依赖列表 | ~2KB |
| `MIGRATION_CHECKLIST.md` | 详细清单 | ~2KB |

**总大小**: ~40-60KB（不含cardiac则~15KB）

## 📞 获取帮助

- **详细指南**: `docs/MIGRATION_GUIDE.md`
- **配置验证**: `python scripts/tools/validate_config.py`
- **标准化检查**: `python scripts/tools/config_standardization.py`
- **问题排查**: 见 `MIGRATION_GUIDE.md` 第9节

---

**💡 提示**: 保存此页面为PDF，打印后放在手边，迁移时更方便！
