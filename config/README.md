# 配置文件说明

本目录包含有心工坊的所有配置文件。

## 配置结构

```
config/
├── app.yml                    # 主配置文件（核心）
├── post_templates.yml         # 文章模板配置
├── inspiration_domains.yml    # 领域知识库
├── vip_content_config.yml     # VIP 内容配置
├── youtube_podcast_config.yml # YouTube 播客配置
├── elevenlabs_voices.yml      # ElevenLabs 语音配置
├── onedrive_config.json       # OneDrive 配置
├── youtube_oauth_*.json       # YouTube OAuth 凭据
├── function_*.json            # 功能映射（内部使用）
└── README.md                  # 本文件
```

## 核心配置文件

### app.yml (主配置)

整合了核心运行配置，包括：

| 配置项 | 说明 |
|--------|------|
| `paths` | 项目路径配置 |
| `logging` | 日志配置 |
| `ai.gemini` | Gemini AI 配置 |
| `platforms` | 发布平台配置 |
| `categories` | 文章分类体系 |
| `templates` | 文章模板配置 |

### .env (环境变量)

敏感信息配置，包括：

| 变量 | 说明 |
|------|------|
| `GEMINI_API_KEY` | Google Gemini API 密钥 |
| `WORDPRESS_*` | WordPress 配置 |
| `WECHAT_*` | 微信公众号配置 |
| `GITHUB_*` | GitHub 配置 |
| `ONEDRIVE_*` | OneDrive 配置 |
| `ELEVENLABS_API_KEY` | ElevenLabs API 密钥 |

## 配置加载

使用统一的配置加载器：

```python
from scripts.utils.config_loader import get_config, load_config

# 获取完整配置
config = get_config()

# 获取特定配置项
model = load_config("ai.gemini.model", "gemini-2.5-flash")

# 获取路径
drafts_path = config.get_path("drafts")

# 获取平台配置
wp_config = config.get_platform("wordpress")

# 获取 WordPress 配置（支持多种环境变量名）
wp = config.get_wordpress_config()
```

## 配置优先级

1. 环境变量 (`.env`)
2. 主配置文件 (`app.yml`)
3. 导入的配置文件
4. 旧版配置文件（向后兼容）

## 敏感文件

以下文件包含敏感信息，已在 `.gitignore` 中排除：

- `.env` - 环境变量
- `config/onedrive_tokens.json` - OneDrive OAuth tokens
- `config/youtube_oauth_token.json` - YouTube OAuth token
- `config/onedrive_config.json` - OneDrive 配置（如包含密钥）

## 迁移说明

### 从旧版配置迁移

旧版配置文件（`pipeline_config.yml`, `gemini_config.yml` 等）仍然支持，但建议迁移到新的 `app.yml`。

配置加载器会自动合并新旧配置，新配置优先。

### WordPress 配置统一

旧版存在多套 WordPress 配置变量：
- `WP_*`
- `WORDPRESS_*`

现已统一为 `WORDPRESS_*`，旧变量名仍然兼容。
