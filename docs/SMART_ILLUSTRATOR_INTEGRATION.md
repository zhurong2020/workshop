# smart-illustrator 集成方案

**调研日期**: 2026-02-26
**实施日期**: 2026-02-26
**状态**: ✅ Phase 1 已完成 | Phase 2 计划中（2026-03-01 规划）
**优先级**: Phase 2 下一步

---

## 一、项目背景

### 解决的痛点

| 当前痛点 | smart-illustrator 的解决方案 |
|---------|--------------------------|
| 每篇文章需要手动找/制作配图 | 自动分析文章结构，生成上下文相关配图 |
| Header image 需要手动设计 | Cover 生成模式，多平台尺寸预设 |
| 金融/投资类文章需要流程图、对比图 | Mermaid 生成结构图，Excalidraw 生成对比图 |
| 认知类文章需要概念可视化 | Gemini 生成隐喻图，Excalidraw 生成思维导图 |

### 项目信息

- **仓库**: https://github.com/axtonliu/smart-illustrator
- **类型**: Claude Code Skill（TypeScript/Bun）
- **Stars**: 330（活跃维护，2026年2月）
- **文档**: 有 `README.zh-CN.md` 中文文档

---

## 二、技术架构

### 三引擎系统

```
文章内容
    ↓ 分析
[引擎选择逻辑]
    ├── Gemini API (Priority 1)
    │   → 创意视觉图、隐喻图、封面图、信息图
    │   → 分辨率: 2K (2816×1536)
    │
    ├── Excalidraw (Priority 2) [可选]
    │   → 手绘风格概念图、关系图、对比图
    │   → 需要 Playwright + Firefox
    │
    └── Mermaid CLI (Priority 3)
        → 结构化流程图、时序图、架构图、思维导图
        → 纯本地，无需 API
```

### 输出规格

- **格式**: PNG
- **文件命名**: `{prefix}-01.png`, `{prefix}-02.png`, ...
- **输出目录**: 可配置（需与 workshop 路径约定对齐）

---

## 三、API Key 调研结论

### 现有 Key 可直接复用 ✅

Workshop 已配置 `GEMINI_API_KEY`（用于 `gemini-2.5-flash` 文本生成）。

**关键结论**：同一个 Google AI Studio API Key 同时支持：
- 文本生成：`gemini-2.5-flash` ← 已在使用
- 图像生成：`gemini-3.1-flash-image-preview`（Nano Banana 2）← **无需额外申请，换模型名即可**

smart-illustrator 读取的环境变量也是 `GEMINI_API_KEY`，**完全匹配，零额外配置**。

**Google billing 状态**：✅ 已开启（2026-03-01 确认）

### 推荐模型：Nano Banana 2（2026-02-26 发布）

| 属性 | 说明 |
|------|------|
| 模型 ID | `gemini-3.1-flash-image-preview` |
| 前代 | Nano Banana Pro（`gemini-3-pro-image`，Phase 1 使用） |
| 优势 | Pro 级质量 + Flash 速度，支持 4K |
| API | 无免费层，需 billing |

> Phase 1 使用的 `gemini-3-pro-image` 建议升级为 `gemini-3.1-flash-image-preview`

### 费用参考（Nano Banana 2 实际定价）

| 分辨率 | 单价 | 批量（5折） | 适用场景 |
|--------|------|------------|---------|
| 512px | $0.045/张 | $0.022/张 | 快速草图 |
| 1K (1024px) | $0.067/张 | $0.034/张 | 博客/周报封面 ← 推荐 |
| 2K | $0.101/张 | $0.050/张 | 高质量公众号封面 |
| 4K | $0.151/张 | $0.076/张 | 专业商业用途 |

**月费估算**（典型场景）：4篇公众号(×2图) + 4篇周报(×1图) = 12张/月 → 约 **$0.80/月**

### 图片策略（成本与质量平衡）

| 使用场景 | 推荐方案 | 费用 |
|---------|---------|------|
| 公众号/WordPress 封面图 | Nano Banana 2（1K-2K） | $0.067-0.101/张 |
| 博客文章内嵌配图 | Pollinations（免费无限） | 免费 |
| 流程图/架构图 | Mermaid CLI（本地） | 免费 |
| 论文周报 WordPress 封面 | Nano Banana 2 批量模式 | ~$0.034/张 |

---

## 四、本地化安装难度评估

| 环节 | 难度 | 说明 |
|------|------|------|
| 安装 Skill | ⭐ 极简 | 一行 `git clone` 到 `~/.claude/skills/` |
| Bun 运行时 | ⭐⭐ 简单 | `npx -y bun` 可自动获取，无需手动安装 |
| Mermaid CLI | ⭐⭐ 简单 | `npm install -g @mermaid-js/mermaid-cli` |
| Playwright/Firefox | ⭐⭐⭐ 中等 | **可选**，仅 Excalidraw 引擎需要，约 200MB，Phase 2 再装 |
| 配置输出目录 | ⭐⭐ 简单 | 配置 `~/.smart-illustrator/config.json` |

**总评**: 安装简单，Phase 1 当天可完成。

---

## 五、与 Workshop 现有管道的整合

### 完整工作流

```
[写完博文 Markdown]
        ↓
[/smart-illustrator] ← 新增 (Claude Code Skill)
  - 分析文章结构，识别最佳配图位置
  - Gemini → 创意图 / 封面图
  - Mermaid → 流程图 / 架构图
  - 输出 PNG 到 assets/images/posts/YYYY/MM/
        ↓
[mixed_image_manager.py] ← 现有管道，无需改动
  上传 OneDrive → 替换为 CDN 链接
        ↓
[run.py 发布流程] ← 现有管道，无需改动
  WordPress + Jekyll + WeChat
```

### 路径约定对齐

Workshop 图片路径规范：
```
assets/images/posts/YYYY/MM/filename.png
```

需在 `~/.smart-illustrator/config.json` 中配置：
```json
{
  "outputDir": "assets/images/posts/{YYYY}/{MM}",
  "prefix": "post-{slug}"
}
```

---

## 六、分阶段实施计划

### Phase 1：基础安装与测试 ✅ 已完成（2026-02-26）

```bash
# Step 1: 安装 Skill ✅
git clone https://github.com/axtonliu/smart-illustrator.git ~/.claude/skills/smart-illustrator

# Step 2: 安装 Mermaid CLI ✅
npm install -g @mermaid-js/mermaid-cli  # v11.12.0

# Step 3: 创建配置文件 ✅
mkdir -p ~/.smart-illustrator
# ~/.smart-illustrator/config.json = { "references": [] }
# 注意：config.json 只支持 references 字段，无 outputDir

# Step 4: GEMINI_API_KEY 配置 ✅
# workshop/.env 中设置真实 Key
# ~/.bashrc 自动读取 .env 导出到 shell 环境

# Step 5: 测试验证 ✅
# 测试文章: _posts/2025-12-06-dca-math-principle-why-profit-in-falling-market.md
# 生成结果:
#   assets/images/posts/2025/12/dca-cover.png (399KB)
#   assets/images/posts/2025/12/dca-harmonic-vs-arithmetic.png (667KB)
#   assets/images/posts/2025/12/dca-5strategy-portfolio.png (404KB)
#   _posts/2025-12-06-dca-math-principle-why-profit-in-falling-market-image.md
```

**已知问题**：
- **Mermaid PNG 导出**需要 Chromium 系统依赖（WSL 中），运行前先执行：
  ```bash
  sudo apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
  ```
  临时方案：在 -image.md 中使用 Mermaid 代码块内嵌（非 PNG）。
- **Gemini 模型**：`gemini-3-pro-image-preview` 需付费；`gemini-2.0-flash-exp-image-generation` 可用但不支持自定义宽高比。
- **图像生成需要开启 Google billing**（文本生成免费，图像生成收费）。
- **调用方式**：`/smart-illustrator` Skill 在 Claude Code 中不能通过 Skill tool 自动加载，需手动执行 SKILL.md 流程。

**验收结论**: ✅ 能对文章生成 3 张配图，输出到正确路径 `assets/images/posts/YYYY/MM/`。

### Phase 2：嵌入发布流程（2026-03-01 规划，下一步实施）

**范围扩展**：不仅限于 workshop 文章，还包括论文周报封面（跨 workspace 集成）。

#### Phase 2-A：workshop run.py 半自动集成
在 `run.py` 菜单新增"为文章生成封面图"选项：
- 读取文章标题/标签，构建 Prompt
- 调用 Nano Banana 2（`gemini-3.1-flash-image-preview`）生成封面
- 输出到 `assets/images/posts/YYYY/MM/` 标准路径
- 后续由 `mixed_image_manager.py` 上传 OneDrive → CDN 链接

#### Phase 2-B：全自动集成（Phase 2-A 验证后）
在发布流程中自动触发，无需人工干预。

#### Phase 2-C：论文周报封面图（跨 workspace）
在 `weekly_paper_search.py` 发布到 WordPress 后，自动调用 Nano Banana 2：
- Prompt 模板：`学术医学研究封面图，主题：{research_topic}，风格：干净专业的学术期刊风格，16:9`
- 使用批量模式（50% 折扣），每周约 $0.034/张
- **注意**：需在 VPS 环境中配置 `GEMINI_API_KEY`

#### model 升级（Phase 2 开始前先做）
将 smart-illustrator 配置从 `gemini-3-pro-image` 改为 `gemini-3.1-flash-image-preview`（Nano Banana 2），性能更好，API 成本更低。

### Phase 3：Excalidraw 支持（可选）

```bash
cd ~/.claude/skills/smart-illustrator/scripts
npm install
npx playwright install firefox
```

适用场景：认知类文章的手绘风格概念图。

---

## 七、注意事项

1. **图片文件名**：smart-illustrator 默认命名需检查是否符合 workshop 的英文纯字母规范（禁止中文）
2. **封面图尺寸**：WordPress 封面图建议 1200×628，需确认 smart-illustrator 的 Cover 模式输出尺寸
3. **API 配额**：免费额度每天约 1500 张，日常博文创作完全够用；如需批量处理历史文章，可用 Batch 模式（5折）
4. **WSL 环境**：项目运行在 WSL2，Playwright/Firefox 安装需确认 Linux 系统依赖（通常自动处理）

---

## 八、相关文档

- [IMAGE_MANAGEMENT_WORKFLOW.md](IMAGE_MANAGEMENT_WORKFLOW.md) - OneDrive 图片管理流程
- [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) - v2.0 架构详情
- [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) - 项目整体规划
- smart-illustrator 中文文档: `~/.claude/skills/smart-illustrator/README.zh-CN.md`（安装后可读）
