# 有心工坊环境迁移指南

本指南适用于将开发环境从一台机器迁移到另一台机器（特别是Windows 11 + WSL2环境）。

## 📋 迁移前检查

### 1. 验证当前环境配置

在旧机器上运行验证工具：

```bash
cd ~/projects/workshop
source venv/bin/activate
python scripts/tools/validate_config.py
```

✅ 确保所有必需配置项都通过验证

### 2. 运行配置标准化检查

```bash
python scripts/tools/config_standardization.py
```

按照建议完成必要的配置改造（如有）

## 📦 准备迁移包

### 一键打包脚本

在旧机器上执行：

```bash
cd ~
# 创建迁移目录
mkdir -p ~/migration-package

# 1. 打包workshop项目敏感配置
cd ~/projects/workshop
tar -czf ~/migration-package/workshop-secrets.tar.gz \
    .env \
    config/onedrive_tokens.json \
    config/youtube_oauth_credentials.json \
    config/youtube_oauth_token.json

# 2. 打包系统级配置
cd ~
tar -czf ~/migration-package/system-configs.tar.gz \
    .cloudflare/ \
    .ssh/ \
    .config/gh/ \
    .gitconfig

# 3. 打包Claude配置（仅凭据）
tar -czf ~/migration-package/claude-config.tar.gz \
    .claude/.credentials.json

# 4. 导出Python依赖（可选，作为参考）
source ~/projects/workshop/venv/bin/activate
pip freeze > ~/migration-package/workshop-requirements.txt
deactivate

# 5. 如果有cardiac项目
if [ -d ~/projects/cardiac-ml-research ]; then
    cd ~/projects/cardiac-ml-research
    tar -czf ~/migration-package/cardiac-configs.tar.gz \
        config/licenses/ \
        config/*.yaml \
        config/*.json

    source .venv/bin/activate
    pip freeze > ~/migration-package/cardiac-requirements.txt
    deactivate
fi

# 6. 创建迁移清单
cat > ~/migration-package/MIGRATION_CHECKLIST.md << 'EOF'
# 迁移清单

## 已打包内容

- [x] workshop-secrets.tar.gz - Workshop项目敏感配置
- [x] system-configs.tar.gz - 系统级配置（SSH, Git, Cloudflare等）
- [x] claude-config.tar.gz - Claude Code认证
- [x] workshop-requirements.txt - Python依赖列表
- [ ] cardiac-configs.tar.gz - Cardiac项目配置（如适用）
- [ ] cardiac-requirements.txt - Cardiac Python依赖（如适用）

## 需要手动迁移的内容

- [ ] VPS服务器密钥（jdcloud.pem）已在system-configs.tar.gz中
- [ ] GitHub SSH密钥（id_ed25519）已在system-configs.tar.gz中
- [ ] Cloudflare配置已在system-configs.tar.gz中

## 迁移后需要验证

- [ ] SSH连接到GitHub: ssh -T git@github.com
- [ ] SSH连接到VPS: ssh arong-vps
- [ ] GitHub CLI认证: gh auth status
- [ ] Claude Code认证: claude --version
- [ ] Workshop配置: python scripts/tools/validate_config.py

## 注意事项

1. 传输方式建议：
   - U盘（最安全）
   - 加密压缩包通过网络传输
   - **不要**通过未加密的方式传输

2. 在新机器验证成功前，不要删除旧机器上的配置

3. 某些token可能需要重新认证（如OneDrive、YouTube）
EOF

echo "✅ 迁移包准备完成！"
echo "📂 位置: ~/migration-package/"
ls -lh ~/migration-package/
```

## 🚀 新机器设置

### 阶段1：基础环境

#### 1.1 安装WSL2（如果是Windows）

```powershell
# 以管理员权限运行PowerShell
wsl --install -d Ubuntu-22.04
```

#### 1.2 安装基础工具

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必需工具
sudo apt install -y \
    git \
    python3.12 \
    python3.12-venv \
    python3-pip \
    build-essential \
    curl \
    wget

# 安装GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# 安装Claude Code CLI
# 访问 https://docs.anthropic.com/claude/docs/claude-code 获取最新安装方法
```

#### 1.3 安装Ruby和Jekyll（可选，用于本地预览）

```bash
# 在Windows端安装Ruby
# 下载：https://rubyinstaller.org/downloads/
# 选择：Ruby 3.3.7 with DevKit

# 安装完成后，在WSL中：
gem install jekyll bundler
```

### 阶段2：恢复配置

#### 2.1 传输并解压迁移包

```bash
# 假设已将migration-package复制到新机器的 ~/Downloads/

cd ~
# 解压系统配置
tar -xzf ~/Downloads/migration-package/system-configs.tar.gz

# 解压Claude配置
tar -xzf ~/Downloads/migration-package/claude-config.tar.gz

# 设置正确的权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/jdcloud.pem
chmod 644 ~/.ssh/id_ed25519.pub ~/.ssh/config
chmod 600 ~/.gitconfig
chmod 600 ~/.claude/.credentials.json
```

#### 2.2 验证SSH和Git

```bash
# 测试GitHub SSH连接
ssh -T git@github.com
# 应该看到：Hi username! You've successfully authenticated...

# 测试VPS连接
ssh arong-vps "echo 'SSH connection successful'"

# 验证Git配置
git config --global --list
```

#### 2.3 认证GitHub CLI

```bash
gh auth login
# 选择：GitHub.com
# 选择：SSH
# 选择：使用现有SSH密钥（~/.ssh/id_ed25519）

# 验证
gh auth status
```

### 阶段3：克隆项目

#### 3.1 Workshop项目

```bash
# 创建项目目录
mkdir -p ~/projects
cd ~/projects

# 克隆项目
git clone git@github.com:zhurong2020/workshop.git
cd workshop

# 解压敏感配置
tar -xzf ~/Downloads/migration-package/workshop-secrets.tar.gz

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 验证配置
python scripts/tools/validate_config.py
```

#### 3.2 Cardiac项目（如需要）

```bash
cd ~/projects

# 克隆项目（替换为实际的仓库地址）
git clone git@github.com:your-username/cardiac-ml-research.git
cd cardiac-ml-research

# 解压配置
tar -xzf ~/Downloads/migration-package/cardiac-configs.tar.gz

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3.3 VPSServer项目（如需要）

```bash
cd ~/projects
git clone git@github.com:your-username/vpsserver.git
```

### 阶段4：工具链设置

#### 4.1 Claude Code认证

```bash
# Claude配置已在阶段2.1中恢复
# 验证
claude --version

# 如果需要重新登录
claude login
```

#### 4.2 设置Bash别名

```bash
# 添加到 ~/.bashrc
echo "alias workshop='/home/wuxia/projects/workshop/workshop.sh'" >> ~/.bashrc
source ~/.bashrc
```

#### 4.3 OneDrive重新认证（如token过期）

```bash
cd ~/projects/workshop
source venv/bin/activate
python scripts/tools/onedrive_auth.py
# 按照提示完成OAuth认证
```

#### 4.4 YouTube OAuth重新认证（如token过期）

```bash
# YouTube OAuth token可能需要重新生成
# 在Google Cloud Console中生成新的OAuth凭据
# 更新 config/youtube_oauth_credentials.json
```

## ✅ 迁移验证清单

运行以下命令验证迁移是否成功：

### Workshop项目
```bash
cd ~/projects/workshop
source venv/bin/activate

# 1. 配置验证
python scripts/tools/validate_config.py

# 2. 测试运行主程序
python run.py

# 3. 测试Git操作
git status
git log -1

# 4. 测试SSH连接
ssh arong-vps "echo 'VPS connection OK'"

# 5. 测试GitHub CLI
gh repo view

# 6. 测试Cloudflare API（如配置）
python -c "from pathlib import Path; import configparser; cf=Path.home()/'.cloudflare'/'config'; print('✅ Cloudflare配置存在' if cf.exists() else '❌ Cloudflare配置缺失')"
```

### Cardiac项目
```bash
cd ~/projects/cardiac-ml-research
source .venv/bin/activate

# 1. 检查License文件
ls -la config/licenses/

# 2. 验证配置文件
ls -la config/*.yaml config/*.json

# 3. 测试Python环境
python -c "import torch; print(f'PyTorch {torch.__version__}')"
```

### 系统工具
```bash
# Claude Code
claude --version

# GitHub CLI
gh auth status

# Git
git config --global --list

# SSH
ssh -T git@github.com
ssh arong-vps "hostname"

# Ruby & Jekyll
ruby --version
jekyll --version
```

## 🔧 故障排查

### SSH密钥权限问题

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/jdcloud.pem
chmod 644 ~/.ssh/id_ed25519.pub ~/.ssh/config
```

### Python虚拟环境问题

```bash
# 删除并重建虚拟环境
cd ~/projects/workshop
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### OneDrive Token过期

```bash
cd ~/projects/workshop
source venv/bin/activate
python scripts/tools/onedrive_auth.py
# 完成OAuth认证流程
```

### Cloudflare配置问题

```bash
# 检查配置文件
cat ~/.cloudflare/config

# 如果缺失，从旧机器复制或重新创建
mkdir -p ~/.cloudflare
# 复制 config 文件内容
```

### Git凭据问题

```bash
# 重新配置Git
git config --global user.name "your-name"
git config --global user.email "your-email@example.com"

# 重新设置GitHub CLI凭据辅助
git config --global credential.helper ""
git config --global credential.helper "!/usr/bin/gh auth git-credential"
```

## 📝 迁移后清理

**在新环境完全验证成功后**，在旧机器上：

```bash
# 安全删除迁移包
cd ~/migration-package
shred -u *.tar.gz  # 安全删除（多次覆写）

# 或者直接删除
rm -rf ~/migration-package
```

**不要删除旧机器上的原始配置文件**，建议保留作为备份。

## 🔐 安全提示

1. **传输安全**：
   - 使用U盘物理传输最安全
   - 如通过网络传输，使用加密压缩包：
     ```bash
     # 加密
     tar -czf - migration-package/ | openssl enc -aes-256-cbc -e > migration.tar.gz.enc

     # 解密
     openssl enc -aes-256-cbc -d -in migration.tar.gz.enc | tar -xz
     ```

2. **密钥管理**：
   - SSH私钥应始终保持600权限
   - .env文件应始终保持600权限
   - 不要将迁移包上传到云存储

3. **Token刷新**：
   - OAuth token（OneDrive、YouTube）可能需要重新认证
   - API密钥应定期轮换
   - 完成迁移后建议更新所有重要密钥

## 📚 相关文档

- [技术架构文档](./TECHNICAL_ARCHITECTURE.md)
- [API密钥注册表](./API_KEYS_REGISTRY.md)
- [图片管理工作流程](./IMAGE_MANAGEMENT_WORKFLOW.md)
- [WordPress发布指南](./WORDPRESS_PUBLISHING_GUIDE.md)

## 🆘 获取帮助

如遇到问题：
1. 查看本文档的"故障排查"部分
2. 运行配置验证工具：`python scripts/tools/validate_config.py`
3. 检查项目的GitHub Issues
4. 查看相关日志文件：`logs/`目录

---

**最后更新**: 2026-01-28
**适用版本**: Workshop v2.0+
**维护者**: Rong Zhu
