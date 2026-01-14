"""
统一配置加载器
支持新旧配置格式的兼容加载
"""

import os
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigLoader:
    """统一配置加载器"""

    _instance = None
    _config = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if ConfigLoader._config is not None:
            return

        self.logger = logging.getLogger(__name__)
        self.project_root = self._find_project_root()
        self.config_dir = self.project_root / "config"

        # 加载环境变量
        load_dotenv(self.project_root / ".env", override=True)

        # 加载配置
        ConfigLoader._config = self._load_all_configs()

    def _find_project_root(self) -> Path:
        """查找项目根目录"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "config").exists() and (parent / "scripts").exists():
                return parent
        return Path.cwd()

    def _load_all_configs(self) -> Dict[str, Any]:
        """加载所有配置"""
        config = {}

        # 1. 优先加载新版主配置 (app.yml)
        app_config = self._load_yaml("app.yml")
        if app_config:
            config.update(app_config)
            self.logger.debug("Loaded config/app.yml")

        # 2. 加载旧版配置作为后备（向后兼容）
        legacy_configs = [
            ("pipeline_config.yml", ["paths", "logging", "content_processing"]),
            ("gemini_config.yml", ["content_processing"]),
            ("platforms.yml", ["platforms"]),
            ("post_templates.yml", ["front_matter", "categories", "footer"]),
        ]

        for filename, keys in legacy_configs:
            legacy = self._load_yaml(filename)
            if legacy:
                for key in keys:
                    if key in legacy and key not in config:
                        config[key] = legacy[key]

        # 3. 处理导入的配置文件
        if "imports" in config:
            for import_file in config["imports"]:
                imported = self._load_yaml(import_file)
                if imported:
                    # 合并导入的配置，不覆盖已有配置
                    for key, value in imported.items():
                        if key not in config:
                            config[key] = value

        # 4. 环境变量覆盖
        config = self._apply_env_overrides(config)

        return config

    def _load_yaml(self, filename: str) -> Optional[Dict[str, Any]]:
        """加载 YAML 配置文件"""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            self.logger.warning(f"Failed to load {filename}: {e}")
            return None

    def _load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        """加载 JSON 配置文件"""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load {filename}: {e}")
            return None

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """应用环境变量覆盖"""
        # 路径配置
        env_paths = {
            "DRAFTS_DIR": "drafts",
            "POSTS_DIR": "posts",
            "IMAGES_DIR": "images",
            "OUTPUT_DIR": "output",
            "ARCHIVE_DIR": "archive",
            "LOGS_DIR": "logs",
            "DATA_DIR": "data",
        }

        if "paths" not in config:
            config["paths"] = {}

        for env_key, config_key in env_paths.items():
            env_value = os.getenv(env_key)
            if env_value:
                config["paths"][config_key] = env_value

        # 日志级别
        log_level = os.getenv("LOG_LEVEL")
        if log_level and "logging" in config:
            config["logging"]["level"] = log_level

        return config

    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return ConfigLoader._config or {}

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_path(self, key: str) -> Path:
        """获取路径配置"""
        path_str = self.get(f"paths.{key}", "")
        if path_str:
            return self.project_root / path_str
        return self.project_root

    def get_platform(self, platform: str) -> Dict[str, Any]:
        """获取平台配置"""
        return self.get(f"platforms.{platform}", {})

    def get_ai_config(self) -> Dict[str, Any]:
        """获取 AI 配置"""
        # 支持新旧两种配置格式
        ai_config = self.get("ai.gemini") or self.get("content_processing.gemini", {})
        return ai_config

    def get_categories(self) -> Dict[str, list]:
        """获取分类配置"""
        return self.get("categories", {})

    def get_templates(self) -> Dict[str, Any]:
        """获取模板配置"""
        return self.get("templates", {}) or self.get("front_matter", {})

    # WordPress 配置兼容方法
    def get_wordpress_config(self) -> Dict[str, str]:
        """获取 WordPress 配置（支持多种环境变量名）"""
        return {
            "url": os.getenv("WORDPRESS_URL") or os.getenv("WP_URL", ""),
            "username": os.getenv("WORDPRESS_USERNAME") or os.getenv("WP_USERNAME", ""),
            "password": os.getenv("WORDPRESS_APP_PASSWORD") or os.getenv("WP_APP_PASSWORD") or os.getenv("WP_PASSWORD", ""),
            "api_url": os.getenv("WORDPRESS_API_URL") or os.getenv("WP_API_URL", ""),
        }


# 便捷函数
def get_config() -> ConfigLoader:
    """获取配置加载器实例"""
    return ConfigLoader()


def load_config(key: str = None, default: Any = None) -> Any:
    """加载配置项"""
    loader = ConfigLoader()
    if key:
        return loader.get(key, default)
    return loader.config
