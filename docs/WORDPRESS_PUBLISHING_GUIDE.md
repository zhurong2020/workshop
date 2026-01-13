# WordPress 多平台发布指南

> 通过"有心工坊"一键发布文章到 WordPress + GitHub Pages + 微信公众号

---

## 📋 目录

1. [系统架构](#系统架构)
2. [快速开始](#快速开始)
3. [配置说明](#配置说明)
4. [发布流程](#发布流程)
5. [VS Code 快捷键](#vs-code-快捷键)
6. [常见问题](#常见问题)

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│              内容创作中心 (workshop)                         │
│                                                             │
│  workshop/_drafts/                                          │
│  └── blog-trilium-notes.md ← 在这里创作草稿                 │
│                                                             │
│  工具: "有心工坊" (run.py)                                   │
│  └── 智能内容发布系统                                        │
│       ├── 质量检查                                           │
│       ├── 平台选择                                           │
│       └── 多平台发布                                         │
│            ├─→ WordPress (arong.eu.org) [完整内容]          │
│            ├─→ GitHub Pages (workshop) [摘要+引流]          │
│            └─→ 微信公众号 [发布指南]                        │
│                                                             │
│  发布后:                                                    │
│  └── workshop/_posts/2026-01-12-blog-trilium-notes.md      │
└─────────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 第一步：配置环境变量

1. 在 workshop 项目根目录，复制 `.env.example` 为 `.env`：
   ```bash
   cd /home/wuxia/projects/workshop
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，配置 WordPress 认证信息：
   ```bash
   # WordPress 配置
   WORDPRESS_URL=https://www.arong.eu.org
   WORDPRESS_USERNAME=你的用户名
   WORDPRESS_PASSWORD=你的应用专用密码
   ```

3. **获取 WordPress 应用专用密码**：
   - 登录 WordPress 后台：https://www.arong.eu.org/youxin-admin/
   - 进入：用户 → 个人资料 → 应用密码
   - 创建新应用密码（名称：workshop-publisher）
   - 复制生成的密码到 `.env` 文件

### 第二步：移动草稿文件

将你的 Markdown 草稿移动到 workshop 项目的 `_drafts/` 目录：

```bash
# 从 vpsserver 移动到 workshop
mv /home/wuxia/projects/vpsserver/wordpress/content/blog-trilium-notes.md \
   /home/wuxia/projects/workshop/_drafts/
```

### 第三步：运行发布流程

在 VS Code 中打开 workshop 项目，使用以下任一方式发布：

**方式 1：快捷键（推荐）**
- 按 `Ctrl+Shift+B` → 自动运行"有心工坊 - 智能发布"

**方式 2：命令面板**
- 按 `Ctrl+Shift+P`
- 输入 `Tasks: Run Task`
- 选择 `📝 有心工坊 - 智能发布`

**方式 3：终端命令**
```bash
# 方式 3a: 使用快捷命令（推荐）
workshop

# 方式 3b: 使用启动脚本
cd /home/wuxia/projects/workshop
./workshop.sh

# 方式 3c: 直接使用虚拟环境
cd /home/wuxia/projects/workshop
venv/bin/python3 run.py
```

**注意**: 不要直接使用 `python run.py`，必须使用虚拟环境中的Python。

---

## 配置说明

### platforms.yml 配置详解

配置文件：`workshop/config/platforms.yml`

```yaml
platforms:
  # GitHub Pages - 摘要 + 引流
  github_pages:
    enabled: true
    excerpt_mode: true    # 启用摘要模式（引流到 WordPress）

  # 微信公众号 - 发布指南
  wechat:
    enabled: true
    publish_mode: guide   # guide 模式（生成发布指南）

  # WordPress - 完整内容
  wordpress:
    enabled: true
    publish_status: draft # 默认发布为草稿（可改为 publish）
```

### 发布模式说明

| 平台 | 模式 | 说明 |
|------|------|------|
| **WordPress** | 完整内容 | 发布完整文章到 arong.eu.org |
| **GitHub Pages** | 摘要 + 引流 | 发布前 300 字摘要，附"阅读完整文章"链接 |
| **微信公众号** | 发布指南 | 生成发布指南文档，手动复制粘贴到微信后台 |

---

## 发布流程

### 完整发布流程

```
1. 创作草稿
   └─ 在 _drafts/ 中编辑 Markdown 文件

2. 运行"有心工坊"
   └─ python run.py 或按 Ctrl+Shift+B

3. 选择草稿
   └─ 从列表中选择要发布的草稿

4. 质量检查
   ├─ 自动检查 Front Matter
   ├─ 验证图片路径
   ├─ 检查摘要长度
   └─ 自动修复缺失的 excerpt

5. 选择平台
   ├─ ☑ WordPress (完整文章)
   ├─ ☑ GitHub Pages (摘要引流)
   └─ ☑ 微信公众号 (发布指南)

6. 选择会员分级
   └─ free (所有人可见)

7. 执行发布
   ├─ WordPress → 调用 REST API 发布
   ├─ GitHub Pages → 生成摘要版本
   └─ 微信公众号 → 生成发布指南

8. 完成
   ├─ 文件移至 _posts/
   ├─ 更新发布状态
   └─ 显示发布结果
```

### Front Matter 格式

确保你的 Markdown 文件包含正确的 Front Matter：

```yaml
---
title: "完全免费的笔记神器：Trilium Notes"
date: 2026-01-12
author: "Rong Zhu"
categories: ["开源应用"]
tags: ["笔记", "开源", "自托管"]
excerpt: "Notion 要订阅、印象笔记要会员、Obsidian 同步要付费……有没有一款笔记软件，功能强大又完全免费？"
layout: post
header:
  teaser: "https://onedrive-url/image.jpg"
---

文章开头内容...

<!-- more -->

文章后续内容...
```

**必需字段**：
- `title`: 文章标题
- `date`: 发布日期
- `excerpt`: 摘要（50-160 字，用于 SEO 和引流）
- `categories`: 分类（建议 1-2 个）
- `tags`: 标签（建议 3-5 个）

---

## VS Code 快捷键

### 可用任务

| 任务 | 快捷键 | 说明 |
|------|--------|------|
| 📝 有心工坊 - 智能发布 | `Ctrl+Shift+B` | 运行完整发布流程（默认） |
| 🚀 快速发布当前草稿 | 手动选择 | 直接发布当前打开的文件 |
| 📊 检查草稿质量 | 手动选择 | 检查所有草稿的质量问题 |
| 🔄 处理 OneDrive 图片 | 手动选择 | 上传本地图片到 OneDrive 图床 |

**使用方式**：
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 `Tasks: Run Task`
3. 选择相应任务

---

## 常见问题

### Q1: WordPress 发布失败，提示认证错误

**A:** 检查以下几点：
1. `.env` 文件中的 `WORDPRESS_URL` 是否正确（https://www.arong.eu.org）
2. `WORDPRESS_USERNAME` 是否正确
3. `WORDPRESS_PASSWORD` 是否是应用专用密码（不是登录密码）
4. 应用专用密码是否已过期（重新生成即可）

### Q2: GitHub Pages 没有生成引流链接

**A:** 确保 `platforms.yml` 中：
```yaml
github_pages:
  enabled: true
  excerpt_mode: true  # 必须为 true
```

### Q3: 微信公众号指南在哪里？

**A:** 发布完成后，指南文件位于：
```
workshop/微信发布指南/[文章标题].md
```
打开后复制内容，粘贴到微信公众平台后台。

### Q4: 如何修改 WordPress 发布状态（草稿 vs 直接发布）

**A:** 修改 `config/platforms.yml`：
```yaml
wordpress:
  publish_status: draft   # 草稿
  # 或
  publish_status: publish # 直接发布
```

### Q5: 文章包含数学公式，WordPress 显示不正常

**A:** 确保 WordPress 已安装并激活 MathJax 插件（已在 mu-plugins 中配置）。
发布时系统会自动提示是否包含数学公式。

### Q6: 图片路径是本地的，如何处理？

**A:** 两种方式：
1. **自动**：运行"🔄 处理 OneDrive 图片"任务，自动上传并替换链接
2. **手动**：在发布前手动上传图片到 OneDrive 或 WordPress 媒体库

### Q7: 如何只发布到 WordPress，不发布到其他平台？

**A:** 在"选择平台"步骤时，只勾选 WordPress 即可。

### Q8: 发布后想修改文章怎么办？

**A:** 两种方式：
1. **WordPress 后台**：直接在后台编辑
2. **重新发布**：修改 `_posts/` 中的文件，运行发布流程（需要指定 post_id）

### Q9: 如何查看发布状态？

**A:** 发布状态记录在：
```
workshop/.publishing/[文章名].yml
```

---

## 技术细节

### Markdown → Gutenberg 转换

系统自动处理以下转换：

- **标题** → `<!-- wp:heading -->`
- **段落** → `<!-- wp:paragraph -->`
- **代码块** → `<!-- wp:code {"language":"python"} -->`
- **表格** → `<!-- wp:table -->`
- **图片** → `<!-- wp:image -->`
- **LaTeX 公式** → 保留原样（需 MathJax 插件）
- **ASCII Art** → 特殊样式处理

### 分类和标签处理

- 自动查找或创建 WordPress 分类/标签
- 保持与 Jekyll Front Matter 一致
- 支持中文分类和标签

### 图片处理

- 自动替换 OneDrive 图片链接
- 保持图片的 alt 属性
- 自动添加响应式样式

---

## 下一步

### 推荐工作流

1. **内容创作** → 在 `_drafts/` 中创作
2. **质量检查** → 运行"📊 检查草稿质量"
3. **图片处理** → 运行"🔄 处理 OneDrive 图片"
4. **发布** → 按 `Ctrl+Shift+B` 一键发布
5. **验证** → 访问 arong.eu.org 检查文章

### 高级功能

- **批量发布**：修改 `run.py` 支持批处理
- **定时发布**：配合 cron 实现定时发布
- **自动引流**：GitHub Pages 自动生成引流链接

---

## 支持

遇到问题？

1. 查看日志：`workshop/logs/`
2. 查看发布状态：`workshop/.publishing/`
3. 参考文档：`workshop/docs/`

---

**最后更新**: 2026-01-12
**维护者**: zhurong + Claude Sonnet 4.5
**版本**: v2.0
