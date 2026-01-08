# mu-plugins 已迁移通知

**迁移日期**: 2026-01-08
**清理日期**: 2026-01-08

## 迁移说明

此目录中的 mu-plugins 已统一迁移到 `vpsserver` 仓库进行管理：

**新位置**: `vpsserver/wordpress/mu-plugins/`

## 迁移原因

1. **安全性**: vpsserver 是 private 仓库，更适合存储服务器配置
2. **统一管理**: 所有 WordPress 相关配置集中在一处
3. **避免重复**: 消除 workshop 和 vpsserver 之间的文件冗余

## 清理记录

以下文件已迁移并从此目录删除：

| 文件 | 状态 |
|------|------|
| `adsense-verification.php` | ✅ 已迁移并删除 |
| `custom-functions.php` | ✅ 已迁移并删除 |
| `footer-policy-links.php` | ✅ 已迁移并删除 |
| `mathjax-support.php` | ✅ 已迁移并删除 |
| `pagination-scroll-fix.php` | ✅ 已迁移并删除 |
| `security-enhancements.php` | ✅ 已迁移并删除 |
| `sidebar-for-posts.php` | ✅ 已迁移并删除 |

## 当前状态

此目录仅保留本迁移通知文件，所有 mu-plugins 源码已移至 vpsserver。

**所有更新应在 vpsserver 仓库中进行**

## 相关文档

- 新位置文档: `vpsserver/wordpress/mu-plugins/README.md`
- VPS 部署指南: `vpsserver/DEPLOYMENT.md`
