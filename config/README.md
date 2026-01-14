# 配置文件说明

本目录包含有心工坊的所有配置文件。

## 配置架构

```
┌─────────────────────────────────────────────────────────────┐
│                    配置管理架构                              │
├─────────────────────────────────────────────────────────────┤
│  app.yml (主配置)              │  .env (敏感信息)            │
│  ├─ paths       路径配置       │  ├─ API 密钥               │
│  ├─ logging     日志配置       │  ├─ 密码/Token             │
│  ├─ ai          AI 配置        │  └─ OAuth 凭据             │
│  ├─ platforms   平台配置       │                            │
│  ├─ github      GitHub 配置    │                            │
│  ├─ onedrive    OneDrive 配置  │                            │
│  ├─ email       邮件配置       │                            │
│  ├─ categories  分类体系       │                            │
│  ├─ templates   文章模板       │                            │
│  └─ footer      页脚配置       │                            │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
config/
├── app.yml                    # 主配置文件（核心）
├── elevenlabs_voices.yml      # ElevenLabs 语音配置
├── youtube_podcast_config.yml # YouTube 播客配置
├── vip_content_config.yml     # VIP 内容配置
├── inspiration_domains.yml    # 领域知识库
├── function_baseline.json     # 功能回归基线
├── function_mapping.json      # 功能映射
├── onedrive_config.json       # OneDrive 配置
├── onedrive_config.example.json
├── onedrive_tokens.json       # OAuth 令牌（敏感）
├── youtube_oauth_*.json       # YouTube OAuth 凭据（敏感）
├── templates/                 # HTML 模板
└── README.md                  # 本文件
```

## 配置加载

使用统一的配置加载器：

```python
from scripts.utils.config_loader import get_config, load_config

# 获取配置加载器实例
config = get_config()

# 获取特定配置项（点号表示法）
model = load_config("ai.gemini.model", "gemini-2.5-flash")

# 获取路径
drafts_path = config.get_path("drafts")

# 获取平台配置
wp_config = config.get_platform("wordpress")

# 获取服务配置（整合 app.yml 和 .env）
wp = config.get_wordpress_config()      # WordPress
wechat = config.get_wechat_config()     # 微信公众号
github = config.get_github_config()     # GitHub
onedrive = config.get_onedrive_config() # OneDrive
email = config.get_email_config()       # 邮件
```

## 配置优先级

1. 环境变量 (`.env`)
2. 主配置文件 (`app.yml`)
3. 导入的配置文件 (`imports`)

## 敏感文件

以下文件包含敏感信息，已在 `.gitignore` 中排除：

- `.env` - 环境变量（API密钥、密码）
- `config/onedrive_tokens.json` - OneDrive OAuth tokens
- `config/youtube_oauth_token.json` - YouTube OAuth token

## 配置说明

### app.yml 主要配置项

| 配置项 | 说明 |
|--------|------|
| `paths` | 项目路径配置 |
| `logging` | 日志配置 |
| `ai.gemini` | Gemini AI 配置 |
| `platforms` | 发布平台配置（GitHub Pages、WordPress、微信） |
| `github` | GitHub 用户名和仓库 |
| `onedrive` | OneDrive redirect_uri |
| `email` | SMTP 服务器配置 |
| `categories` | 文章分类体系 |
| `templates` | 文章模板 front matter |
| `footer` | 页脚配置（投资声明、打赏等） |

### .env 敏感信息

| 变量 | 说明 |
|------|------|
| `GEMINI_API_KEY` | Google Gemini API 密钥 |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS API 密钥 |
| `YOUTUBE_API_KEY` | YouTube Data API 密钥 |
| `WORDPRESS_USERNAME/APP_PASSWORD` | WordPress 凭据 |
| `WECHAT_APPID/APPSECRET` | 微信公众号凭据 |
| `GITHUB_TOKEN` | GitHub Personal Access Token |
| `ONEDRIVE_*` | OneDrive OAuth 凭据 |
| `GMAIL_USER/APP_PASSWORD` | Gmail SMTP 凭据 |

## 功能模块配置

独立功能模块保持单独的配置文件，便于维护：

- `elevenlabs_voices.yml` - TTS 语音组合配置
- `youtube_podcast_config.yml` - 播客生成参数
- `vip_content_config.yml` - VIP 等级和内容标准
- `inspiration_domains.yml` - 领域知识和搜索参数
