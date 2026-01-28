# Workshop 项目待办清单

**最后更新**: 2026-01-28
**项目状态**: 维护模式（内容创作已迁移至 WordPress）+ 项目规范化整改中
**负责人**: zhurong

---

## 优先级说明
- P0: 紧急/安全相关
- P1: 本周完成
- P2: 本月完成
- P3: 可选/低优先级

---

## 待办事项

### P0 - 项目规范化整改（进行中）

- [x] **第一阶段：快速胜利** ✅ 已完成（2026-01-28）
  - [x] 批量添加LICENSE（10个项目）
  - [x] 批量创建.env.example（17个项目）
  - [x] 处理git遗留问题
  - 成效：LICENSE覆盖率100%，.env.example覆盖率100%
  - 详见：`docs/PHASE1_FINAL_STATUS_REPORT.md`

- [ ] **第二阶段：关键改进**（待开始，8-12小时）
  - 描述：为关键项目添加CI/CD和测试框架
  - 优先级：smartnews-lite（最高） > Tier 1核心研究 > 其他Tier 2
  - 预期：CI/CD覆盖率60%，测试框架65%，平均评分80+
  - 详见：`docs/PHASE2_TASKS_TODO.md`

- [ ] **第三阶段：批量完善**（待开始，5-8小时）
  - 描述：批量添加CONTRIBUTING.md，优化文档结构
  - 详见：`docs/GLOBAL_PROJECTS_SUMMARY_AND_REMEDIATION.md`

### P1 - 本周任务

- [ ] **AI 主题生成功能增强**
  - 描述: 添加保存功能、批量处理、质量评估
  - 参考: `docs/NEXT_PHASE_DEVELOPMENT_PLAN.md`

- [ ] **OneDrive 图床 API 激活**
  - 描述: 配置 Microsoft Graph API 凭证
  - 具体步骤:
    1. [ ] 获取 Azure AD 应用凭证
    2. [ ] 配置 OAuth 认证流程
    3. [ ] 测试图片上传功能

### P2 - 本月任务

- [ ] **AdSense 审核跟进**
  - arong.eu.org: 正在准备中
  - 审核通过后:
    1. [ ] 创建广告单元 (arong-in-article, arong-sidebar, arong-footer)
    2. [ ] 配置 Ad Inserter 插件
  - 参考: `docs/ADSENSE_PENDING_TASKS.md`

### P3 - 可选任务

- [ ] **喜马拉雅 API 集成**
  - 描述: 国内用户音频分发渠道
  - 参考: `docs/audio-platform-integration-plan.md`

- [ ] **混合 TTS 架构实施**
  - 描述: 成本优化，Azure vs ElevenLabs

---

## 内容创作任务（迁移至 WordPress 发布）

### 待兑现预告文章（5篇）

| 优先级 | 文章标题 | 来源 | 状态 |
|--------|---------|------|------|
| P1 | 小资金大收益：Poor Man's Covered Call 完全指南 | 期权解套文章预告 | 待创作 |
| P1 | 30+ 回购分红标的深度分析 | 期权解套文章预告 | 素材已有 |
| P2 | 量化策略组合：如何同时运行多个自动交易系统 | 期权解套文章预告 | 待创作 |
| P2 | VS Code 配合 AI 插件进行策略改造 | 开源定投文章预告 | 待创作 |
| P3 | 使用本地模型避免高额 LLM 费用 | 开源定投文章预告 | 待创作 |

### 近期可发布内容（素材已完成）

| 文件 | 主题 | 字数 | 发布平台 |
|------|------|------|---------|
| 03-stock-buyback-dividend-full.md | 回购分红 30+ 标的 | 37K | WordPress + 知乎 + 雪球 |
| DCA-05-7layer-system.md | 7 层回撤系统 | - | WordPress + 公众号 |
| 05-ib-level3-guide.md | IB 期权指南 | - | WordPress |

### 发布平台清单

- **WordPress** (www.arong.eu.org): 完整版归档
- **知乎**: 教程类内容
- **雪球**: 数据分析和策略
- **公众号**: 深度内容和会员服务
- **微信群**: 读者交流

---

## 已完成任务

### 2026-01
- [x] 21个项目配置管理评估（3批次）
- [x] 第一阶段规范化整改（LICENSE + .env.example）
- [x] 项目演进发现（cnnvideo-timer → smartnews-lite）
- [x] 生成9份详细评估和整改文档

### 2025-12
- [x] WordPress 迁移工具开发
- [x] AdSense 集成配置
- [x] pyobfus 博文发布

### 2025-09
- [x] TQQQ 定投系列 3 篇
- [x] 期权解套完全指南

---

## 相关文档

- 项目路线图: `docs/PROJECT_ROADMAP.md`
- 开发计划: `docs/NEXT_PHASE_DEVELOPMENT_PLAN.md`
- 内容发布路线图: `_drafts/todos/00-CONTENT-PUBLISHING-ROADMAP.md`
- 预告追踪: `_drafts/todos/00-CONTENT-PROMISES-TRACKER.md`
