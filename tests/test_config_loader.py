"""
配置加载器自动化测试
验证配置管理系统的完整性和兼容性
"""

import sys
import pytest
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.config_loader import ConfigLoader, get_config, load_config


class TestConfigLoader:
    """配置加载器测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前重置单例"""
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_singleton_pattern(self):
        """测试单例模式"""
        loader1 = ConfigLoader()
        loader2 = ConfigLoader()
        assert loader1 is loader2, "ConfigLoader 应该是单例"

    def test_project_root_detection(self):
        """测试项目根目录检测"""
        config = get_config()
        assert config.project_root.exists(), "项目根目录应该存在"
        assert (config.project_root / "config").exists(), "config 目录应该存在"
        assert (config.project_root / "scripts").exists(), "scripts 目录应该存在"

    def test_config_dir(self):
        """测试配置目录"""
        config = get_config()
        assert config.config_dir.exists(), "配置目录应该存在"
        assert (config.config_dir / "app.yml").exists(), "app.yml 应该存在"


class TestPathsConfig:
    """路径配置测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_paths_exist(self):
        """测试路径配置存在"""
        config = get_config()
        paths = config.get("paths")
        assert paths is not None, "paths 配置应该存在"
        assert "drafts" in paths, "drafts 路径应该配置"
        assert "posts" in paths, "posts 路径应该配置"

    def test_get_path(self):
        """测试获取路径方法"""
        config = get_config()
        drafts = config.get_path("drafts")
        posts = config.get_path("posts")

        assert drafts.name == "_drafts", "drafts 路径应该是 _drafts"
        assert posts.name == "_posts", "posts 路径应该是 _posts"

    def test_path_resolution(self):
        """测试路径解析"""
        config = get_config()
        drafts = config.get_path("drafts")

        # 路径应该是绝对路径
        assert drafts.is_absolute(), "返回的路径应该是绝对路径"


class TestAIConfig:
    """AI 配置测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_gemini_config(self):
        """测试 Gemini 配置"""
        config = get_config()
        ai_config = config.get_ai_config()

        assert ai_config is not None, "AI 配置应该存在"
        assert "model" in ai_config, "model 应该配置"

    def test_gemini_model_value(self):
        """测试 Gemini 模型值"""
        config = get_config()
        ai_config = config.get_ai_config()

        model = ai_config.get("model", "")
        assert "gemini" in model.lower(), "模型应该是 Gemini 系列"


class TestPlatformConfig:
    """平台配置测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_platforms_exist(self):
        """测试平台配置存在"""
        config = get_config()

        for platform in ["github_pages", "wordpress", "wechat"]:
            p = config.get_platform(platform)
            assert p is not None, f"{platform} 配置应该存在"

    def test_platform_enabled(self):
        """测试平台启用状态"""
        config = get_config()

        github = config.get_platform("github_pages")
        assert github.get("enabled") is True, "github_pages 应该启用"

        wordpress = config.get_platform("wordpress")
        assert wordpress.get("enabled") is True, "wordpress 应该启用"

    def test_platform_features(self):
        """测试平台功能配置"""
        config = get_config()

        wordpress = config.get_platform("wordpress")
        features = wordpress.get("features", {})

        assert "analyze_content" in features, "应该有 analyze_content 配置"
        assert "replace_images" in features, "应该有 replace_images 配置"


class TestWordPressConfig:
    """WordPress 配置测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_wordpress_config_exists(self):
        """测试 WordPress 配置存在"""
        config = get_config()
        wp = config.get_wordpress_config()

        assert wp is not None, "WordPress 配置应该存在"
        assert "url" in wp, "应该有 url"
        assert "username" in wp, "应该有 username"
        assert "password" in wp, "应该有 password"

    def test_wordpress_url_format(self):
        """测试 WordPress URL 格式"""
        config = get_config()
        wp = config.get_wordpress_config()

        url = wp.get("url", "")
        if url:  # 只有配置了才测试
            assert url.startswith("https://"), "URL 应该使用 HTTPS"

    def test_wordpress_env_compatibility(self):
        """测试 WordPress 环境变量兼容性"""
        # 测试新旧环境变量名都能工作
        config = get_config()
        wp = config.get_wordpress_config()

        # 应该能获取到配置（来自 WORDPRESS_* 或 WP_*）
        assert wp.get("url") or wp.get("username"), "应该能从环境变量获取 WordPress 配置"


class TestCategoriesConfig:
    """分类配置测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_categories_exist(self):
        """测试分类配置存在"""
        config = get_config()
        categories = config.get_categories()

        assert categories is not None, "分类配置应该存在"
        assert len(categories) > 0, "应该有分类"

    def test_core_categories(self):
        """测试核心分类"""
        config = get_config()
        categories = config.get_categories()

        expected = ["认知升级", "技术赋能", "全球视野", "投资理财"]
        for cat in expected:
            assert cat in categories, f"应该有 {cat} 分类"


class TestLoadConfigFunction:
    """load_config 便捷函数测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_dot_notation(self):
        """测试点号表示法"""
        model = load_config("ai.gemini.model")
        assert model is not None, "应该能用点号获取嵌套配置"

    def test_default_value(self):
        """测试默认值"""
        value = load_config("non.existent.key", "default")
        assert value == "default", "不存在的键应该返回默认值"

    def test_full_config(self):
        """测试获取完整配置"""
        config = load_config()
        assert isinstance(config, dict), "无参数时应该返回完整配置字典"


class TestConfigCompatibility:
    """配置兼容性测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        ConfigLoader._instance = None
        ConfigLoader._config = None
        yield

    def test_legacy_paths_structure(self):
        """测试旧版路径结构兼容"""
        config = get_config()

        # 旧版 pipeline_config.yml 结构
        paths = config.get("paths", {})
        assert "drafts" in paths
        assert "posts" in paths
        assert "images" in paths

    def test_legacy_logging_structure(self):
        """测试旧版日志结构兼容"""
        config = get_config()

        logging = config.get("logging", {})
        assert "level" in logging
        assert "format" in logging

    def test_legacy_content_processing(self):
        """测试旧版内容处理配置兼容"""
        config = get_config()

        # 可能在 ai.gemini 或 content_processing.gemini
        ai_config = config.get_ai_config()
        assert ai_config is not None, "应该能获取 AI 配置（新旧格式）"


class TestConfigFiles:
    """配置文件完整性测试"""

    def test_app_yml_exists(self):
        """测试 app.yml 存在"""
        config = get_config()
        app_yml = config.config_dir / "app.yml"
        assert app_yml.exists(), "app.yml 应该存在"

    def test_pipeline_config_exists(self):
        """测试 pipeline_config.yml 存在（兼容性）"""
        config = get_config()
        pipeline_config = config.config_dir / "pipeline_config.yml"
        assert pipeline_config.exists(), "pipeline_config.yml 应该存在（兼容性）"

    def test_platforms_yml_exists(self):
        """测试 platforms.yml 存在"""
        config = get_config()
        platforms_yml = config.config_dir / "platforms.yml"
        assert platforms_yml.exists(), "platforms.yml 应该存在"

    def test_archived_directory(self):
        """测试归档目录存在"""
        config = get_config()
        archived = config.config_dir / "archived"
        assert archived.exists(), "archived 目录应该存在"
        assert archived.is_dir(), "archived 应该是目录"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
