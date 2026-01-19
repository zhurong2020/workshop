# Arong-Unified Workspace 命名规范

本文档定义项目、文件和代码的统一命名规范，便于长期开发维护。

## 一、目录/项目命名规范

### 1.1 规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 全小写 | 统一使用小写字母 | `workshop`, `docuforge` |
| 连字符分隔 | 多个单词用 `-` 连接 | `smart-news`, `vps-server` |
| 禁止空格 | 绝不使用空格 | ❌ `my project` → ✅ `my-project` |
| 纯英文 | 不使用中文或特殊字符 | ❌ `商户分析` → ✅ `bizassist` |
| 简洁明了 | 2-3个单词，表达核心功能 | `paper-toolkit`, `cardiac-ml` |

### 1.2 当前项目重命名对照表

| 当前名称 | 建议名称 | 说明 |
|----------|----------|------|
| `workshop` | `workshop` | ✅ 已符合 |
| `vpsserver` | `vps-server` | 添加连字符增强可读性 |
| `docuforge` | `docuforge` | ✅ 已符合 |
| `bizassist` | `bizassist` | ✅ 已符合 |
| `smartnews-lite` | `smartnews-lite` | ✅ 已符合 |
| `home` | `home-manager` | 增加描述性后缀 |
| `moomoo_custom_strategies` | `moomoo-strategies` | 下划线改连字符，简化 |
| `zhurong2020.github.io` | `gridea-archive` | 描述性命名 (注: GitHub Pages 要求特定名称) |

---

## 二、VS Code Workspace 文件夹命名

### 2.1 规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 纯英文 | 显示名也用英文 | ❌ `(商户分析)` → ✅ `(Merchant)` |
| 简短标签 | 括号内1-2个单词说明用途 | `Workshop (Blog)` |
| 可选省略 | 名称自解释时可不加括号 | `docuforge` |

### 2.2 建议的 Workspace 文件夹配置

```json
{
  "folders": [
    { "name": "workshop", "path": "./workshop" },
    { "name": "gridea-archive", "path": "./zhurong2020.github.io" },
    { "name": "vps-server", "path": "./vpsserver" },
    { "name": "bizassist", "path": "./bizassist" },
    { "name": "smartnews-lite", "path": "./smartnews-lite" },
    { "name": "docuforge", "path": "./docuforge" },
    { "name": "home-manager", "path": "./home" },
    { "name": "moomoo-strategies", "path": "./moomoo_custom_strategies" }
  ]
}
```

---

## 三、文件命名规范

### 3.1 代码文件

| 类型 | 规则 | 示例 |
|------|------|------|
| Python | snake_case | `content_pipeline.py`, `wordpress_publisher.py` |
| JavaScript/TypeScript | camelCase 或 kebab-case | `contentService.ts`, `api-client.js` |
| Shell 脚本 | kebab-case | `deploy-config.sh`, `backup-db.sh` |
| 配置文件 | kebab-case | `app-config.yml`, `docker-compose.yml` |

### 3.2 文档文件

| 规则 | 说明 | 示例 |
|------|------|------|
| 大写+下划线 | Markdown 文档 | `CHANGELOG_DETAILED.md`, `API_KEYS_REGISTRY.md` |
| 英文优先 | 文件名用英文 | ❌ `使用指南.md` → ✅ `USER_GUIDE.md` |
| 前缀分类 | 可选：用前缀分组 | `00-CONTENT-HOOKS-SOP.md` |

### 3.3 资源文件

| 类型 | 规则 | 示例 |
|------|------|------|
| 图片 | kebab-case, 日期前缀可选 | `hero-banner.png`, `2025-01-chart.png` |
| 数据文件 | snake_case | `user_data.json`, `config_backup.yml` |

---

## 四、Git 分支命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 主分支 | `main` | `main` |
| 功能分支 | `feature/<描述>` | `feature/add-podcast-generator` |
| 修复分支 | `fix/<描述>` | `fix/pylance-type-errors` |
| 发布分支 | `release/<版本>` | `release/v2.0.0` |

---

## 五、Git Commit 消息规范

### 5.1 格式

```
<type>(<scope>): <简短描述>

[可选正文]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### 5.2 Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(publisher): 添加微信发布适配器` |
| `fix` | Bug 修复 | `fix(api): 修复 Gemini 配额检测` |
| `docs` | 文档更新 | `docs: 更新 CHANGELOG` |
| `refactor` | 重构 | `refactor(core): 模块化菜单系统` |
| `test` | 测试 | `test: 添加 API 单元测试` |
| `chore` | 杂项 | `chore: 更新依赖版本` |
| `style` | 格式 | `style: 修复代码缩进` |
| `perf` | 性能 | `perf: 优化图片加载速度` |

### 5.3 Scope 范围 (可选)

按模块或功能区分：`core`, `cli`, `api`, `test`, `docs`, `config`, `publisher`, `podcast` 等

---

## 六、CLAUDE.md 文件规范

### 6.1 层级结构

```
/home/wuxia/projects/
├── ARONG_UNIFIED_CLAUDE.md    # Workspace 级别约定 (跨项目通用)
├── workshop/
│   └── CLAUDE.md              # 项目级别约定
├── docuforge/
│   └── CLAUDE.md              # 项目级别约定
└── ...
```

### 6.2 内容规范

| 层级 | 内容 |
|------|------|
| Workspace | 共享资源、项目关系、通用约定 |
| Project | 项目概述、技术架构、开发约定、文件路径 |

---

## 七、环境变量命名

| 规则 | 说明 | 示例 |
|------|------|------|
| 全大写 | 环境变量统一大写 | `API_KEY`, `DB_HOST` |
| 下划线分隔 | 多个单词用 `_` 连接 | `WORDPRESS_API_URL` |
| 前缀分组 | 同类变量用前缀 | `GEMINI_API_KEY`, `CLAUDE_API_KEY` |

---

## 八、实施计划

### Phase 1: 低风险调整 (立即)
- [x] 更新 workspace 文件夹显示名称 (不影响实际路径)
- [x] 新建文件遵循命名规范

### Phase 2: 渐进式重命名 (按需)
- [ ] `moomoo_custom_strategies` → `moomoo-strategies`
- [ ] `vpsserver` → `vps-server`
- [ ] `home` → `home-manager`

### Phase 3: 文档标准化 (持续)
- [ ] 中文文件名改为英文
- [ ] 统一 README 和 CLAUDE.md 结构

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-01-19 | 初始版本，定义命名规范 |
