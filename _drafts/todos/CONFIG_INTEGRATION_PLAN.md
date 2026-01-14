# 配置文件完整整合计划

> 创建时间: 2026-01-14
> 完成时间: 2026-01-14
> 状态: 已完成

## 整合目标

将分散的配置文件整合为清晰的两层结构：
- `config/app.yml` - 主配置（非敏感信息）
- `.env` - 敏感信息（API密钥、密码、Token）

## 任务清单

### 阶段一：config/ 目录整合

- [x] 1.1 分析配置文件现状
- [x] 1.2 将 `post_templates.yml` 的 footer 配置合并到 `app.yml`
- [x] 1.3 补全 `app.yml` 中的 platforms 配置（添加 URL 端点）
- [x] 1.4 删除 `platforms.yml`（已整合到 app.yml）
- [x] 1.5 删除 `pipeline_config.yml`（已整合到 app.yml）
- [x] 1.6 删除 `post_templates.yml`（已整合到 app.yml）
- [x] 1.7 删除 `config/archived/` 目录

### 阶段二：.env 精简

- [x] 2.1 将 URL 端点移到 `app.yml`
  - WORDPRESS_URL, WORDPRESS_API_URL, WORDPRESS_JWT_URL
  - WECHAT_API_BASE_URL
  - SMTP_SERVER, SMTP_PORT
- [x] 2.2 将非敏感配置移到 `app.yml`
  - GITHUB_USERNAME, GITHUB_REPO
  - ONEDRIVE_REDIRECT_URI
- [x] 2.3 清理废弃配置
  - 删除百度网盘注释
  - 删除 Cloudflare 注释
- [x] 2.4 精简 .env 文件 (84行 → 60行)

### 阶段三：同步与更新

- [x] 3.1 更新 `.env.example` 与 `.env` 同步
- [x] 3.2 更新 `config_loader.py` 移除旧文件引用，添加新方法
- [x] 3.3 更新 `config/README.md` 文档
- [x] 3.4 运行测试验证配置加载

### 阶段四：验证与提交

- [x] 4.1 运行 `python run.py` 验证主程序
- [x] 4.2 运行配置测试 `pytest tests/test_config_loader.py` (26 passed)
- [x] 4.3 提交所有更改

## 文件变更清单

### 删除的文件
```
config/platforms.yml
config/pipeline_config.yml
config/post_templates.yml
config/archived/elevenlabs_voices_pro.yml
config/archived/elevenlabs_voices_template.yml
config/archived/gemini_config.yml
config/archived/test_config.yml
```

### 修改的文件
```
config/app.yml          - 整合所有配置
.env                    - 精简为仅敏感信息
.env.example            - 同步更新
scripts/utils/config_loader.py - 移除旧文件引用
config/README.md        - 更新文档
```

### 保留的文件
```
config/elevenlabs_voices.yml
config/youtube_podcast_config.yml
config/vip_content_config.yml
config/inspiration_domains.yml
config/function_baseline.json
config/function_mapping.json
config/onedrive_config.json
config/onedrive_config.example.json
config/onedrive_tokens.json
config/youtube_oauth_credentials.json
config/youtube_oauth_token.json
config/templates/
```

## 目标结构

```
项目根目录/
├── .env                    # 仅敏感信息 (~20 变量)
├── .env.example            # 模板文件
│
└── config/
    ├── app.yml             # 主配置 (~250 行)
    ├── elevenlabs_voices.yml
    ├── youtube_podcast_config.yml
    ├── vip_content_config.yml
    ├── inspiration_domains.yml
    ├── function_*.json
    ├── onedrive_*.json
    ├── youtube_oauth_*.json
    ├── templates/
    └── README.md
```

## 进度记录

| 日期 | 完成项 | 备注 |
|------|--------|------|
| 2026-01-14 | 1.1-1.7 | 完成 config/ 目录整合 |
| 2026-01-14 | 2.1-2.4 | 完成 .env 精简 (84行→60行) |
| 2026-01-14 | 3.1-3.4 | 完成同步与更新 |
| 2026-01-14 | 4.1-4.3 | 完成验证与提交 |

---
*此文件用于跟踪配置整合进度，确保工作可以在对话中断后继续*
