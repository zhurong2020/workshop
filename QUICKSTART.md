# 有心工坊 - 快速开始指南

> 一键发布文章到 WordPress + GitHub Pages + 微信公众号

## 🚀 快速启动

### 第一次使用

1. **安装依赖**（仅需一次）
   ```bash
   cd /home/wuxia/projects/workshop
   venv/bin/pip install -r requirements.txt
   ```

2. **重新加载终端配置**（仅需一次）
   ```bash
   source ~/.bashrc
   ```

### 日常使用

**只需一条命令：**
```bash
workshop
```

系统会自动：
1. 显示主菜单
2. 让你选择要发布的草稿
3. 选择发布平台
4. 自动发布到所有平台

## 📝 创作流程

### 1. 创建草稿

```bash
cd /home/wuxia/projects/workshop
vim _drafts/my-article.md
```

**Front Matter 模板**：
```yaml
---
title: "文章标题"
date: 2026-01-12
author: "Rong Zhu"
categories: ["技术赋能"]
tags: ["标签1", "标签2", "标签3"]
excerpt: "文章摘要，60-120字，用于SEO和预览"
layout: post
header:
  teaser: "https://图片链接.jpg"
---

文章开头...

<!-- more -->

文章主体内容...
```

### 2. 运行发布系统

**最简单的方式**：
```bash
workshop
```

**其他方式**：
```bash
# 使用启动脚本
./workshop.sh

# 直接使用虚拟环境
venv/bin/python3 run.py

# VS Code 快捷键
# 按 Ctrl+Shift+B
```

### 3. 选择发布平台

系统会提示选择：
- ☑ **WordPress** (arong.eu.org) - 完整文章
- ☑ **GitHub Pages** - 摘要+引流
- ☑ **微信公众号** - 发布指南

### 4. 确认发布

发布完成后，系统会显示：
- ✅ WordPress 文章 ID 和 URL
- ✅ GitHub Pages 文件位置
- ✅ 微信发布指南路径

## 📚 三平台策略

| 平台 | 内容 | 目的 |
|------|------|------|
| **WordPress** | 完整文章 | 主站内容，SEO优化 |
| **GitHub Pages** | 摘要+链接 | 引流到WordPress |
| **微信公众号** | 格式化指南 | 手动发布到微信 |

## 🔧 常用命令

```bash
# 启动有心工坊
workshop

# 查看帮助
workshop --help

# 查看草稿列表
ls -lh _drafts/*.md

# 查看已发布文章
ls -lh _posts/*.md

# 编辑草稿
vim _drafts/my-article.md
```

## ⚠️ 注意事项

1. **不要使用 `python run.py`**
   - ❌ 错误：`python run.py` 或 `python3 run.py`
   - ✅ 正确：`workshop` 或 `./workshop.sh` 或 `venv/bin/python3 run.py`

2. **图片处理**
   - 本地图片需先上传到 OneDrive 图床
   - 使用相对路径：`assets/images/posts/2026/01/image.png`
   - 系统会自动替换为 CDN 链接

3. **默认发布状态**
   - WordPress 默认发布为**草稿**
   - 需要在后台审核后再发布
   - 修改配置：`config/app.yml` → `platforms.wordpress.publish_status: publish`

4. **数学公式支持**
   - 使用 LaTeX 语法：`$$公式$$` 或 `$公式$`
   - 确保 WordPress 已安装 MathJax 插件

## 🐛 常见问题

### Q: 提示"找不到命令 workshop"
**A**: 重新加载终端配置
```bash
source ~/.bashrc
```

### Q: 提示"ModuleNotFoundError"
**A**: 安装依赖
```bash
cd /home/wuxia/projects/workshop
venv/bin/pip install -r requirements.txt
```

### Q: WordPress 发布失败
**A**: 检查以下几点
1. `.env` 文件中的 WordPress 配置是否正确
2. 应用专用密码是否有效
3. 网络连接是否正常
4. 查看日志：`logs/`

### Q: 如何查看已发布的文章
**A**: 登录 WordPress 后台
```
https://www.arong.eu.org/youxin-admin/
文章 → 所有文章
```

## 📖 详细文档

### 核心文档
- **完整使用指南**: `docs/WORDPRESS_PUBLISHING_GUIDE.md`
- **文档导航地图**: `DOCS_MAP.md` ⭐ (推荐收藏)
- **故障排查指南**: `TROUBLESHOOTING.md`
- **项目文档**: `CLAUDE.md`

### 配置相关
- **主配置文件**: `config/app.yml`
- **环境变量**: `.env`
- **配置验证**: `python scripts/tools/validate_config.py`
- **配置检查**: `python scripts/tools/config_standardization.py`

### 环境迁移
- **迁移总览**: `README_MIGRATION.md`
- **快速参考**: `docs/QUICK_MIGRATION_REFERENCE.md`
- **完整指南**: `docs/MIGRATION_GUIDE.md`
- **迁移准备**: `bash scripts/tools/prepare_migration.sh`

## 🎉 开始创作

现在你可以开始创作了！

```bash
# 1. 创建草稿
vim _drafts/my-first-article.md

# 2. 运行发布系统
workshop

# 3. 享受自动化发布！
```

---

**最后更新**: 2026-01-12
**维护者**: zhurong + Claude Sonnet 4.5
