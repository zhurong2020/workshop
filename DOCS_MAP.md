# 📚 有心工坊 - 文档导航地图

> **快速找到你需要的文档** - 分类清晰的文档索引

**最后更新**: 2026-01-28

---

## 🎯 快速导航

### 刚开始？从这里开始

| 文档 | 适用场景 | 预计阅读时间 |
|------|----------|--------------|
| **[QUICKSTART.md](QUICKSTART.md)** | 第一次使用系统 | 5分钟 |
| **[README.md](README.md)** | 了解项目功能和架构 | 10分钟 |
| **[CLAUDE.md](CLAUDE.md)** | 开始开发和贡献 | 15分钟 |

### 遇到问题？查看故障排查

| 文档 | 问题类型 | 预计解决时间 |
|------|----------|--------------|
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | 常见问题快速索引 | 2-5分钟 |
| **[QUICKSTART.md#常见问题](QUICKSTART.md#-常见问题)** | 启动和发布问题 | 2-5分钟 |
| **[配置验证工具](scripts/tools/validate_config.py)** | 配置问题诊断 | 1分钟 |

### 需要迁移环境？

| 文档 | 适用场景 | 预计时间 |
|------|----------|----------|
| **[QUICK_MIGRATION_REFERENCE.md](docs/QUICK_MIGRATION_REFERENCE.md)** | 快速迁移速查 | 15分钟 |
| **[MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)** | 详细迁移步骤 | 30分钟 |
| **[README_MIGRATION.md](README_MIGRATION.md)** | 迁移准备总览 | 5分钟 |

### 想要贡献代码？

| 文档 | 内容 | 必读性 |
|------|------|--------|
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | 贡献指南和开发规范 | ⭐⭐⭐ |
| **[CLAUDE.md](CLAUDE.md)** | 开发约定和最佳实践 | ⭐⭐⭐ |
| **[SECURITY.md](SECURITY.md)** | 安全最佳实践 | ⭐⭐ |

---

## 📖 完整文档分类

### 🚀 入门文档

| 文档 | 描述 | 难度 |
|------|------|------|
| [README.md](README.md) | 项目总览和功能介绍 | ⭐ |
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速开始指南 | ⭐ |
| [CLAUDE.md](CLAUDE.md) | 开发约定和规范 | ⭐⭐ |
| [TODO.md](TODO.md) | 待办事项和路线图 | ⭐ |

### 🔧 配置与安装

| 文档 | 描述 | 何时查看 |
|------|------|----------|
| [.env.example](.env.example) | 环境变量配置模板 | 首次安装 |
| [requirements.txt](requirements.txt) | Python依赖列表 | 首次安装 |
| [docs/setup/youtube_podcast_setup.md](docs/setup/youtube_podcast_setup.md) | YouTube播客配置 | 使用播客功能时 |
| [docs/setup/tts_comprehensive_setup.md](docs/setup/tts_comprehensive_setup.md) | 语音系统配置 | 使用TTS时 |
| [docs/setup/YOUTUBE_OAUTH_SETUP.md](docs/setup/YOUTUBE_OAUTH_SETUP.md) | YouTube上传OAuth2配置 | 上传视频时 |

### 🛠️ 配置管理工具（2026-01-28新增）

| 工具/文档 | 功能 | 使用场景 |
|-----------|------|----------|
| [scripts/tools/validate_config.py](scripts/tools/validate_config.py) | 验证27项配置完整性 | 启动前、迁移后 |
| [scripts/tools/config_standardization.py](scripts/tools/config_standardization.py) | 检查配置问题和改进建议 | 配置优化 |
| [scripts/tools/prepare_migration.sh](scripts/tools/prepare_migration.sh) | 一键生成完整迁移包 | 环境迁移前 |
| [docs/CONFIG_STANDARDIZATION_SUMMARY.md](docs/CONFIG_STANDARDIZATION_SUMMARY.md) | 配置标准化总结 | 了解配置管理 |

### 🔄 环境迁移

| 文档 | 内容 | 适用对象 |
|------|------|----------|
| [README_MIGRATION.md](README_MIGRATION.md) | 迁移准备总览 | 需要迁移的用户 |
| [docs/QUICK_MIGRATION_REFERENCE.md](docs/QUICK_MIGRATION_REFERENCE.md) | 快速迁移速查表（一页纸） | 快速迁移 |
| [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) | 完整迁移指南（含故障排查） | 首次迁移 |
| [docs/CHANGELOG_2026-01-28_CONFIG_MIGRATION.md](docs/CHANGELOG_2026-01-28_CONFIG_MIGRATION.md) | 配置管理修订记录 | 了解技术细节 |
| [docs/GIT_COMMITS_SUMMARY_2026-01-28.md](docs/GIT_COMMITS_SUMMARY_2026-01-28.md) | Git提交总结 | 查看提交历史 |

### 🏗️ 技术架构

| 文档 | 描述 | 目标读者 |
|------|------|----------|
| [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md) | v2.0技术架构和设计决策 | 开发者 |
| [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | 重构后的目录结构说明 | 开发者 |
| [docs/SYSTEM_MENU_ARCHITECTURE.md](docs/SYSTEM_MENU_ARCHITECTURE.md) | 菜单系统架构设计 | 开发者 |
| [docs/PROJECT_SOFTWARE_ENGINEERING_FINAL_AUDIT.md](docs/PROJECT_SOFTWARE_ENGINEERING_FINAL_AUDIT.md) | A-级别软件工程审计报告 | 技术决策者 |

### 📝 功能指南

| 文档 | 功能 | 何时查看 |
|------|------|----------|
| [docs/WORDPRESS_PUBLISHING_GUIDE.md](docs/WORDPRESS_PUBLISHING_GUIDE.md) | WordPress多平台发布系统 | 发布文章时 |
| [docs/IMAGE_MANAGEMENT_WORKFLOW.md](docs/IMAGE_MANAGEMENT_WORKFLOW.md) | OneDrive图片管理工作流 | 处理图片时 |
| [docs/AUDIO_RESOURCE_MANAGEMENT.md](docs/AUDIO_RESOURCE_MANAGEMENT.md) | 音频资源管理系统 | 处理音频时 |
| [docs/guides/YOUTUBE_COMPLETE_GUIDE.md](docs/guides/YOUTUBE_COMPLETE_GUIDE.md) | YouTube功能完整指南 | 使用YouTube功能时 |
| [docs/USER_GUIDE_NEW_MENU.md](docs/USER_GUIDE_NEW_MENU.md) | 菜单系统使用指南 | 不熟悉菜单时 |

### 💎 会员内容管理

| 文档 | 内容 | 目标读者 |
|------|------|----------|
| [docs/MEMBER_CONTENT_RULES_AND_STANDARDS.md](docs/MEMBER_CONTENT_RULES_AND_STANDARDS.md) | VIP内容创作和管理标准 | 内容创作者 |
| [docs/VIP_CONTENT_CREATION_GUIDE.md](docs/VIP_CONTENT_CREATION_GUIDE.md) | VIP内容创作指南 | 内容创作者 |
| [docs/MEMBER_CONTENT_MANAGEMENT_SYSTEM.md](docs/MEMBER_CONTENT_MANAGEMENT_SYSTEM.md) | 访问控制和版本管理系统 | 开发者 |
| [docs/CONTENT_SERIES_INTEGRATION_STRATEGY.md](docs/CONTENT_SERIES_INTEGRATION_STRATEGY.md) | 四大系列有机关联设计 | 内容规划者 |
| [docs/member-system-guide.md](docs/member-system-guide.md) | 会员管理、配置和运营指南 | 管理员 |
| [docs/member-access-user-guide.md](docs/member-access-user-guide.md) | 会员验证系统使用指南 | 会员用户 |

### 🔒 安全与维护

| 文档 | 内容 | 重要性 |
|------|------|--------|
| [SECURITY.md](SECURITY.md) | 安全最佳实践 | ⭐⭐⭐ |
| [docs/API_KEYS_REGISTRY.md](docs/API_KEYS_REGISTRY.md) | API密钥注册表和配额管理 | ⭐⭐⭐ |
| [docs/FUNCTION_REGRESSION_PREVENTION.md](docs/FUNCTION_REGRESSION_PREVENTION.md) | 功能退化防控系统 | ⭐⭐ |

### 📊 项目历史与更新

| 文档 | 内容 | 适用场景 |
|------|------|----------|
| [docs/CHANGELOG_DETAILED.md](docs/CHANGELOG_DETAILED.md) | v2.0详细功能实现历史 | 了解项目演进 |
| [docs/REFACTORING_PROGRESS.md](docs/REFACTORING_PROGRESS.md) | 完整的重构历程和成果 | 了解重构过程 |
| [docs/ARCHAEOLOGY_DISCOVERY_ROUND2.md](docs/ARCHAEOLOGY_DISCOVERY_ROUND2.md) | 功能考古发现记录 | 技术研究 |

### 🎬 音视频系统

| 文档 | 内容 | 相关功能 |
|------|------|----------|
| [docs/audio-platform-integration-plan.md](docs/audio-platform-integration-plan.md) | 多平台音频系统架构 | 音频发布 |
| [docs/ximalaya-developer-requirements.md](docs/ximalaya-developer-requirements.md) | 第三方平台集成准备 | 喜马拉雅集成 |

### 🚀 规划与路线图

| 文档 | 内容 | 目标读者 |
|------|------|----------|
| [docs/AZURE_INTEGRATION_ROADMAP.md](docs/AZURE_INTEGRATION_ROADMAP.md) | Azure生态系统集成规划 | 技术规划者 |
| [TODO.md](TODO.md) | 待办事项和短期路线图 | 所有人 |

---

## 🔍 按使用场景查找

### 我想...

| 场景 | 推荐文档 |
|------|----------|
| **快速开始使用系统** | [QUICKSTART.md](QUICKSTART.md) |
| **了解项目全貌** | [README.md](README.md) |
| **发布第一篇文章** | [QUICKSTART.md](QUICKSTART.md) → [docs/WORDPRESS_PUBLISHING_GUIDE.md](docs/WORDPRESS_PUBLISHING_GUIDE.md) |
| **配置新功能** | [.env.example](.env.example) → 对应setup文档 |
| **解决配置问题** | [scripts/tools/validate_config.py](scripts/tools/validate_config.py) → [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **迁移到新环境** | [README_MIGRATION.md](README_MIGRATION.md) → [docs/QUICK_MIGRATION_REFERENCE.md](docs/QUICK_MIGRATION_REFERENCE.md) |
| **深入了解技术** | [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md) |
| **贡献代码** | [CONTRIBUTING.md](CONTRIBUTING.md) → [CLAUDE.md](CLAUDE.md) |
| **管理会员内容** | [docs/MEMBER_CONTENT_RULES_AND_STANDARDS.md](docs/MEMBER_CONTENT_RULES_AND_STANDARDS.md) |
| **处理图片** | [docs/IMAGE_MANAGEMENT_WORKFLOW.md](docs/IMAGE_MANAGEMENT_WORKFLOW.md) |
| **排查故障** | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |

---

## 📱 文档更新历史

| 日期 | 更新内容 |
|------|----------|
| 2026-01-28 | 新增配置管理工具文档和迁移文档体系 |
| 2025-08-20 | 新增会员内容管理文档 |
| 2025-08-15 | 重构后v2.0文档更新 |

---

## 💡 使用提示

1. **收藏本页**: 这是查找所有文档的最快方式
2. **善用搜索**: 在项目根目录运行 `grep -r "关键词" docs/`
3. **从简单开始**: 新手建议从 QUICKSTART.md 开始
4. **遇到问题先查**: TROUBLESHOOTING.md 包含95%的常见问题
5. **保持文档同步**: 修改功能时同步更新相关文档

---

## 🤝 文档贡献

发现文档问题或有改进建议？

1. 提交Issue: [GitHub Issues](https://github.com/zhurong2020/workshop/issues)
2. 直接PR: 参考 [CONTRIBUTING.md](CONTRIBUTING.md)
3. 联系维护者: 查看 [CLAUDE.md](CLAUDE.md)

---

**维护者**: Rong Zhu + Claude Code
**文档版本**: v2.0
**最后更新**: 2026-01-28
