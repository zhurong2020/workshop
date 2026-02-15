# 🔧 故障排查指南

> **快速解决常见问题** - 95%的问题都在这里有答案

**最后更新**: 2026-01-28

---

## 🚀 快速诊断

**遇到问题？先运行配置验证工具：**

```bash
cd ~/projects/personal/websites/workshop
source venv/bin/activate
python scripts/tools/validate_config.py
```

这会自动检查27项配置，快速定位问题。

---

## 📋 问题分类索引

### 🔴 紧急问题（影响使用）

| 问题 | 跳转 |
|------|------|
| 系统完全无法启动 | [→ 启动问题](#-启动问题) |
| 找不到命令/模块 | [→ 环境问题](#-python环境问题) |
| 配置文件缺失 | [→ 配置问题](#-配置问题) |
| 发布失败 | [→ 发布问题](#-发布问题) |

### 🟡 一般问题（功能异常）

| 问题 | 跳转 |
|------|------|
| 图片无法上传 | [→ OneDrive问题](#-onedrive图床问题) |
| 权限错误 | [→ 权限问题](#-权限问题) |
| API配额超限 | [→ API问题](#-api配额问题) |
| 性能缓慢 | [→ 性能问题](#-性能问题) |

### 🟢 配置问题（需要调整）

| 问题 | 跳转 |
|------|------|
| 如何配置新功能 | [→ 配置问题](#-配置问题) |
| Token过期 | [→ 认证问题](#-oauth认证问题) |
| 环境变量设置 | [→ 环境变量](#环境变量问题) |

---

## 🔴 启动问题

### ❌ 问题：提示"找不到命令 workshop"

**症状**:
```bash
$ workshop
bash: workshop: 未找到命令
```

**原因**: bash别名未生效

**解决方案**:
```bash
# 方案1: 重新加载配置（推荐）
source ~/.bashrc

# 方案2: 使用完整路径
cd ~/projects/personal/websites/workshop
./workshop.sh

# 方案3: 使用虚拟环境直接运行
venv/bin/python3 run.py

# 验证别名
type workshop
```

**预防措施**:
- 修改 `.bashrc` 后总是运行 `source ~/.bashrc`
- 在新终端窗口测试

---

### ❌ 问题：提示"Permission denied"

**症状**:
```bash
$ workshop
bash: ./workshop.sh: Permission denied
```

**原因**: 脚本没有执行权限

**解决方案**:
```bash
# 添加执行权限
chmod +x workshop.sh

# 或直接用bash运行
bash workshop.sh
```

---

### ❌ 问题：Python脚本启动后立即退出

**症状**: 运行后没有菜单显示，直接返回命令行

**排查步骤**:
```bash
# 1. 查看错误日志
cat logs/pipeline.log | tail -50

# 2. 直接运行看详细错误
source venv/bin/activate
python run.py

# 3. 检查配置完整性
python scripts/tools/validate_config.py

# 4. 查看Python版本
python --version  # 需要 3.8+
```

**常见原因**:
- 缺少必需的环境变量
- Python版本过低
- 依赖包未安装

---

## 🐍 Python环境问题

### ❌ 问题：ModuleNotFoundError

**症状**:
```python
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'yaml'
```

**原因**: 依赖包未安装或使用了系统Python

**解决方案**:
```bash
# 1. 确保使用虚拟环境
cd ~/projects/personal/websites/workshop
source venv/bin/activate  # 命令行前应显示 (venv)

# 2. 重新安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 3. 验证安装
pip list | grep <包名>

# 4. 如果虚拟环境损坏，重建
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**验证虚拟环境**:
```bash
# 检查Python路径（应该指向venv目录）
which python
# 应该输出: /home/wuxia/projects/personal/websites/workshop/venv/bin/python
```

---

### ❌ 问题：ImportError: cannot import name

**症状**:
```python
ImportError: cannot import name 'ConfigLoader' from 'scripts.utils.config_loader'
```

**原因**: 代码结构变更或缓存问题

**解决方案**:
```bash
# 1. 清理Python缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 2. 重新安装包（如果是editable install）
pip install -e .

# 3. 检查import路径
python -c "from scripts.utils.config_loader import ConfigLoader; print('OK')"
```

---

## ⚙️ 配置问题

### ❌ 问题：.env文件缺失

**症状**:
```
FileNotFoundError: .env file not found
或配置验证显示缺少环境变量
```

**解决方案**:
```bash
# 1. 检查.env是否存在
ls -la .env

# 2. 如果不存在，从示例复制
cp .env.example .env

# 3. 编辑.env填入真实值
vim .env
# 或
nano .env

# 4. 验证必需变量
python scripts/tools/validate_config.py
```

**必需的环境变量**:
```bash
GEMINI_API_KEY=your-key          # 必需
ONEDRIVE_TENANT_ID=your-id       # 必需
ONEDRIVE_CLIENT_ID=your-id       # 必需
ONEDRIVE_CLIENT_SECRET=your-secret  # 必需
```

---

### 环境变量问题

**Q**: 如何检查环境变量是否生效？

```bash
# 方法1: 在Python中检查
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GEMINI_API_KEY:', os.getenv('GEMINI_API_KEY')[:10]+'...')"

# 方法2: 使用配置验证工具
python scripts/tools/validate_config.py
```

**Q**: .env文件已配置但仍然提示缺失？

**原因**: 可能在使用系统Python而不是虚拟环境

```bash
# 确保激活虚拟环境
source venv/bin/activate

# 检查Python路径
which python  # 应该指向venv/bin/python
```

---

## 📤 发布问题

### ❌ 问题：WordPress发布失败

**症状**:
```
Error: Authentication failed
或 ConnectionError
```

**排查清单**:
```bash
# 1. 检查WordPress配置
grep WORDPRESS .env

# 2. 验证网络连接
ping www.arong.eu.org

# 3. 测试API端点
curl -I https://www.arong.eu.org/wp-json/

# 4. 验证应用密码
# 登录 WordPress 后台 → 用户 → 个人资料 → 应用密码

# 5. 查看详细错误日志
cat logs/pipeline.log | grep -A 5 "WordPress"
```

**常见原因**:
1. **应用密码错误**: 重新生成应用密码（不是账号密码）
2. **网络问题**: 检查VPN或防火墙设置
3. **API端点错误**: 确认 `config/app.yml` 中URL正确
4. **权限不足**: 确认WordPress用户有发布权限

**应用密码设置**:
```
1. 登录 https://www.arong.eu.org/youxin-admin/
2. 用户 → 个人资料
3. 滚动到底部 → 应用密码
4. 输入名称（如"Workshop") → 添加新应用密码
5. 复制生成的密码（格式: xxxx xxxx xxxx xxxx）
6. 在.env中设置: WORDPRESS_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

---

### ❌ 问题：GitHub Pages发布失败

**症状**:
```
git push failed
或 Permission denied (publickey)
```

**解决方案**:
```bash
# 1. 检查SSH密钥
ssh -T git@github.com
# 应该显示: Hi username! You've successfully authenticated

# 2. 如果失败，检查SSH配置
cat ~/.ssh/config
ls -la ~/.ssh/id_ed25519

# 3. 测试Git配置
git config --global --list

# 4. 检查远程仓库
git remote -v
```

**SSH密钥问题**: 参见 [SSH问题](#-ssh和git问题)

---

## 🖼️ OneDrive图床问题

### ❌ 问题：OAuth Token过期

**症状**:
```
Error: invalid_grant
或 Token has expired
```

**解决方案**:
```bash
# 重新认证
cd ~/projects/personal/websites/workshop
source venv/bin/activate
python scripts/tools/onedrive_auth.py

# 按照提示：
# 1. 浏览器会打开认证页面
# 2. 登录OneDrive账户
# 3. 授权应用
# 4. 复制返回的Token
# 5. Token会自动保存到 config/onedrive_tokens.json
```

**预防措施**:
- OneDrive Token有效期通常为90天
- 在迁移时记得复制 `config/onedrive_tokens.json`

---

### ❌ 问题：图片上传失败

**症状**:
```
Failed to upload image to OneDrive
或 File not found
```

**排查步骤**:
```bash
# 1. 检查图片文件是否存在
ls -la assets/images/posts/2026/01/

# 2. 检查文件权限
ls -l <图片文件>

# 3. 检查OneDrive配置
cat config/onedrive_config.json

# 4. 测试OneDrive连接
python -c "from scripts.tools.onedrive_blog_images import OneDriveBlogImages; obj = OneDriveBlogImages(); print('Token valid' if obj.is_token_valid() else 'Token invalid')"
```

**常见原因**:
1. Token过期 → 重新认证
2. 文件路径错误 → 使用相对路径
3. 文件太大 → 检查大小限制（32MB）
4. 网络问题 → 检查网络连接

---

## 🔐 OAuth认证问题

### ❌ 问题：YouTube OAuth认证失败

**症状**:
```
Error: invalid_client
或 redirect_uri_mismatch
```

**解决方案**:
```bash
# 1. 检查OAuth凭据文件
cat config/youtube_oauth_credentials.json

# 2. 验证redirect_uri
# 应该是: http://localhost:8080/

# 3. 重新获取凭据
# Google Cloud Console → APIs & Services → Credentials
# 创建OAuth 2.0客户端ID
# 应用类型：桌面应用
# 下载JSON文件，保存为 youtube_oauth_credentials.json

# 4. 重新认证
rm config/youtube_oauth_token.json
# 重新运行需要YouTube的功能，会自动触发认证
```

**详细配置**: 参见 [docs/setup/YOUTUBE_OAUTH_SETUP.md](docs/setup/YOUTUBE_OAUTH_SETUP.md)

---

## 📊 API配额问题

### ❌ 问题：Gemini API配额耗尽

**症状**:
```
429 Resource has been exhausted
或 Quota exceeded
```

**解决方案**:
```bash
# 1. 检查配额状态
# 访问: https://aistudio.google.com/app/apikey

# 2. 等待配额重置（太平洋时间午夜）

# 3. 临时使用Claude（如配置）
# 系统会自动切换，或手动指定

# 4. 考虑升级到付费层级
# 绑定信用卡到Google Cloud
# 免费额度：$300
```

**配额限制**（Free Tier）:
- 50次/天
- 5 RPM (gemini-2.5-pro)
- 125,000 TPM

**详细信息**: 参见 [docs/API_KEYS_REGISTRY.md](docs/API_KEYS_REGISTRY.md)

---

## 🔑 权限问题

### ❌ 问题：SSH密钥权限错误

**症状**:
```
Permissions 0644 for '/home/wuxia/.ssh/id_ed25519' are too open
```

**解决方案**:
```bash
# 修复SSH密钥权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 644 ~/.ssh/config

# 验证
ls -la ~/.ssh/
```

**正确的权限设置**:
```
drwx------  ~/.ssh/                 (700)
-rw-------  ~/.ssh/id_ed25519       (600)
-rw-r--r--  ~/.ssh/id_ed25519.pub   (644)
-rw-r--r--  ~/.ssh/config           (644)
```

---

### ❌ 问题：文件写入权限被拒绝

**症状**:
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**:
```bash
# 1. 检查文件所有者
ls -la <文件路径>

# 2. 如果所有者不是当前用户
sudo chown -R $(whoami):$(whoami) ~/projects/personal/websites/workshop

# 3. 检查目录权限
chmod 755 ~/projects/personal/websites/workshop
chmod 755 ~/projects/personal/websites/workshop/_posts
chmod 755 ~/projects/personal/websites/workshop/_drafts
```

---

## 🔌 SSH和Git问题

### ❌ 问题：SSH连接GitHub失败

**症状**:
```
Permission denied (publickey)
```

**排查步骤**:
```bash
# 1. 测试SSH连接
ssh -T git@github.com

# 2. 检查SSH密钥
ls -la ~/.ssh/id_ed25519*

# 3. 如果没有密钥，生成新密钥
ssh-keygen -t ed25519 -C "your-email@example.com"

# 4. 将公钥添加到GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出，添加到：https://github.com/settings/keys

# 5. 验证连接
ssh -T git@github.com
```

**详细指南**: [GitHub SSH文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

### ❌ 问题：Git push被拒绝

**症状**:
```
! [rejected] main -> main (fetch first)
或 ! [remote rejected] main -> main (pre-receive hook declined)
```

**解决方案**:
```bash
# 情况1: 远程有新提交
git pull --rebase origin main
git push origin main

# 情况2: 历史冲突
git status
# 解决冲突后
git add .
git rebase --continue
git push origin main

# 情况3: 分支保护（通常不适用个人项目）
# 检查 GitHub → Settings → Branches
```

---

## ⚡ 性能问题

### ❌ 问题：运行缓慢

**排查清单**:
```bash
# 1. 检查系统资源
top
df -h

# 2. 清理Python缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 3. 清理日志文件
ls -lh logs/
# 如果日志太大
> logs/pipeline.log  # 清空日志

# 4. 优化图片处理
# 减小图片尺寸或数量

# 5. 检查网络连接
ping -c 3 www.arong.eu.org
ping -c 3 api.openai.com
```

---

## 🧪 配置验证命令

### 完整的系统健康检查

```bash
cd ~/projects/personal/websites/workshop
source venv/bin/activate

# 1. 配置验证（推荐首先运行）
python scripts/tools/validate_config.py

# 2. 配置标准化检查
python scripts/tools/config_standardization.py

# 3. 检查Python环境
python --version
pip list | grep -E "requests|yaml|google"

# 4. 检查SSH配置
ssh -T git@github.com
ssh arong-vps "echo 'VPS OK'"

# 5. 检查Git状态
git status
git log --oneline -3

# 6. 查看日志
tail -50 logs/pipeline.log
```

---

## 📚 更多帮助

### 还是无法解决？

1. **查看详细日志**:
   ```bash
   cat logs/pipeline.log | less
   ```

2. **运行诊断工具**:
   ```bash
   python scripts/tools/validate_config.py
   python scripts/tools/config_standardization.py
   ```

3. **查看完整文档**:
   - [DOCS_MAP.md](DOCS_MAP.md) - 文档导航
   - [README.md](README.md) - 项目总览
   - [CLAUDE.md](CLAUDE.md) - 开发约定

4. **提交Issue**:
   - [GitHub Issues](https://github.com/zhurong2020/workshop/issues)
   - 包含错误信息和系统环境

5. **查看相关文档**:
   - 配置问题: [docs/CONFIG_STANDARDIZATION_SUMMARY.md](docs/CONFIG_STANDARDIZATION_SUMMARY.md)
   - 迁移问题: [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)
   - WordPress问题: [docs/WORDPRESS_PUBLISHING_GUIDE.md](docs/WORDPRESS_PUBLISHING_GUIDE.md)

---

## 🔄 文档更新

本文档持续更新，记录新发现的问题和解决方案。

**贡献问题解决方案**: 如果你遇到并解决了新问题，欢迎提交PR更新本文档！

---

**维护者**: Rong Zhu + Claude Code
**最后更新**: 2026-01-28
**文档版本**: v1.0
