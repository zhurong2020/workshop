"""
WordPress 发布器
负责将 Markdown 内容发布到 WordPress，支持 Gutenberg 格式
"""
import os
import sys
import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
import markdown
import frontmatter

# 添加 wordpress_migration 工具路径
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "wordpress_migration"))

try:
    from gutenberg_converter import convert_html_to_gutenberg_with_stats, ConversionOptions  # pyright: ignore[reportMissingImports]
except ImportError:
    # 如果导入失败，定义一个简单的转换函数
    def convert_html_to_gutenberg_with_stats(html: str, options: Any = None) -> Tuple[str, Dict]:
        return html, {}

    class ConversionOptions:
        def __init__(self, **kwargs):
            pass


class WordPressPublisher:
    """WordPress 发布器"""

    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        """
        初始化 WordPress 发布器

        Args:
            config: WordPress 配置字典
            logger: 日志记录器
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)

        # 从环境变量读取认证信息
        self.wp_url = os.getenv('WORDPRESS_URL', config.get('api_endpoint', '').replace('/wp-json/', ''))
        self.wp_user = os.getenv('WORDPRESS_USERNAME', '')
        self.wp_password = os.getenv('WORDPRESS_PASSWORD', '')

        # API 端点
        self.api_base = f"{self.wp_url}/wp-json/wp/v2"

        # 发布状态（draft 或 publish）
        self.publish_status = config.get('publish_status', 'draft')

        # 会话
        self.session = requests.Session()
        if self.wp_user and self.wp_password:
            self.session.auth = HTTPBasicAuth(self.wp_user, self.wp_password)

    def log(self, message: str, level: str = "info", force: bool = False) -> None:
        """记录日志"""
        if self.logger:
            getattr(self.logger, level)(message)
        if force:
            print(f"[{level.upper()}] {message}")

    def convert_markdown_to_gutenberg(self, content: str) -> Tuple[str, Dict[str, int], bool]:
        """
        将 Markdown 转换为 Gutenberg 格式

        Args:
            content: Markdown 内容

        Returns:
            Tuple of (gutenberg_content, stats, has_math)
        """
        # === 预处理：清理 Jekyll/Liquid 特定语法 ===

        # 移除 Liquid 模板块
        content = re.sub(
            r'\{%\s*assign\s+investment_tags.*?\{%\s*endif\s*%\}',
            '', content, flags=re.DOTALL
        )
        content = re.sub(r'\{%\s*assign\s+[^%]*%\}', '', content)
        content = re.sub(r'\{%\s*for\s+[^%]*%\}.*?\{%\s*endfor\s*%\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\{%\s*if\s+[^%]*%\}.*?\{%\s*endif\s*%\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\{%[^%]*%\}', '', content)
        content = re.sub(r'\{\{[^}]*\}\}', '', content)

        # 转换 Kramdown 链接属性
        kramdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)\{:target=["\']_blank["\']\}', content)
        content = re.sub(r'\{:target=["\']_blank["\']\}', '', content)

        # 保护 LaTeX 数学公式
        math_blocks = []
        def save_math(match):
            math_blocks.append(match.group(0))
            return f'%%MATH_BLOCK_{len(math_blocks)-1}%%'

        content = re.sub(r'\$\$[^$]+\$\$', save_math, content, flags=re.DOTALL)
        content = re.sub(r'\$[^$\n]+\$', save_math, content)

        # 保护 ASCII art 块
        ascii_art_blocks = []
        def save_ascii_art(match):
            ascii_art_blocks.append(match.group(0))
            return f'\n%%ASCII_ART_{len(ascii_art_blocks)-1}%%\n'

        content = re.sub(
            r'```[^\n]*\n((?:[^\n]*[├─│└┘┐┌┬┴┼╔╗╚╝║═]+[^\n]*\n)+)```',
            save_ascii_art, content
        )

        # === 转换 Markdown 为 HTML ===
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',  # 保留语言信息
            'toc',
        ])

        html = md.convert(content)

        # === 后处理 ===

        # 恢复 LaTeX 数学块
        for i, math in enumerate(math_blocks):
            html = html.replace(f'%%MATH_BLOCK_{i}%%', math)

        # 恢复 ASCII art 块
        for i, art in enumerate(ascii_art_blocks):
            pre_block = f'''<div class="ascii-art-container" style="overflow-x: auto; background: #f8f9fa; padding: 1.5em; border-radius: 8px; margin: 1em 0; border: 1px solid #e9ecef;">
<pre style="font-family: 'Sarasa Mono SC', 'Noto Sans Mono CJK SC', 'Source Han Mono SC', 'Microsoft YaHei Mono', 'Courier New', monospace; font-size: 14px; line-height: 1.5; white-space: pre; margin: 0; letter-spacing: 0;">{art}</pre>
</div>'''
            html = html.replace(f'<p>%%ASCII_ART_{i}%%</p>', pre_block)
            html = html.replace(f'%%ASCII_ART_{i}%%', pre_block)

        # 修复 more 标签
        html = html.replace('<!-- more -->', '<!--more-->')

        # 为外部链接添加 target="_blank"
        for link_text, link_url in kramdown_links:
            old_link = f'<a href="{link_url}">{link_text}</a>'
            new_link = f'<a href="{link_url}" target="_blank" rel="noopener noreferrer">{link_text}</a>'
            html = html.replace(old_link, new_link)

        # 使图片响应式
        html = re.sub(
            r'<img\s+([^>]*?)(/?)>',
            r'<img \1 style="max-width: 100%; height: auto;" \2>',
            html
        )

        # 清理空段落
        html = re.sub(r'<p>\s*</p>', '', html)

        # 追踪是否有数学内容
        has_math = len(math_blocks) > 0

        # === 转换为 Gutenberg 格式 ===
        options = ConversionOptions(
            preserve_more_tag=True
        )

        try:
            gutenberg_content, stats = convert_html_to_gutenberg_with_stats(html, options)
            return gutenberg_content, stats, has_math
        except Exception as e:
            self.log(f"Gutenberg 转换失败: {e}", level="error")
            # 如果转换失败，返回原始 HTML
            return html, {}, has_math

    def get_or_create_category(self, category_name: str) -> Optional[int]:
        """获取或创建分类"""
        try:
            # 查找现有分类
            response = self.session.get(
                f"{self.api_base}/categories",
                params={'search': category_name, 'per_page': 1}
            )
            response.raise_for_status()

            categories = response.json()
            if categories:
                return categories[0]['id']

            # 创建新分类
            response = self.session.post(
                f"{self.api_base}/categories",
                json={'name': category_name}
            )
            response.raise_for_status()

            return response.json()['id']

        except Exception as e:
            self.log(f"处理分类 '{category_name}' 失败: {e}", level="error")
            return None

    def get_or_create_tag(self, tag_name: str) -> Optional[int]:
        """获取或创建标签"""
        try:
            # 查找现有标签
            response = self.session.get(
                f"{self.api_base}/tags",
                params={'search': tag_name, 'per_page': 1}
            )
            response.raise_for_status()

            tags = response.json()
            if tags:
                return tags[0]['id']

            # 创建新标签
            response = self.session.post(
                f"{self.api_base}/tags",
                json={'name': tag_name}
            )
            response.raise_for_status()

            return response.json()['id']

        except Exception as e:
            self.log(f"处理标签 '{tag_name}' 失败: {e}", level="error")
            return None

    def publish_to_wordpress(
        self,
        content: str,
        metadata: Dict[str, Any],
        post_id: Optional[int] = None
    ) -> Optional[int]:
        """
        发布内容到 WordPress

        Args:
            content: Markdown 内容
            metadata: Front Matter 元数据
            post_id: 如果提供，则更新现有文章；否则创建新文章

        Returns:
            发布后的文章 ID，失败返回 None
        """
        try:
            # 提取标题
            title = metadata.get('title', '无标题')

            # 转换内容为 Gutenberg 格式
            self.log(f"正在转换 Markdown 为 Gutenberg 格式...", level="info", force=True)
            gutenberg_content, stats, has_math = self.convert_markdown_to_gutenberg(content)

            if stats:
                self.log(f"转换统计: {stats}", level="info", force=True)

            # 处理分类
            categories = metadata.get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            category_ids = []
            for cat in categories:
                cat_id = self.get_or_create_category(cat)
                if cat_id:
                    category_ids.append(cat_id)

            # 处理标签
            tags = metadata.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]
            tag_ids = []
            for tag in tags:
                tag_id = self.get_or_create_tag(tag)
                if tag_id:
                    tag_ids.append(tag_id)

            # 准备文章数据
            post_data = {
                'title': title,
                'content': gutenberg_content,
                'status': self.publish_status,
                'categories': category_ids,
                'tags': tag_ids,
            }

            # 添加摘要（如果有）
            excerpt = metadata.get('excerpt', '')
            if excerpt:
                post_data['excerpt'] = excerpt

            # 添加日期（如果有）
            date = metadata.get('date', None)
            if date:
                if isinstance(date, str):
                    post_data['date'] = date
                elif isinstance(date, datetime):
                    post_data['date'] = date.isoformat()

            # 发布或更新文章
            if post_id:
                # 更新现有文章
                self.log(f"正在更新文章 ID {post_id}...", level="info", force=True)
                response = self.session.post(
                    f"{self.api_base}/posts/{post_id}",
                    json=post_data
                )
            else:
                # 创建新文章
                self.log(f"正在创建新文章...", level="info", force=True)
                response = self.session.post(
                    f"{self.api_base}/posts",
                    json=post_data
                )

            response.raise_for_status()
            result = response.json()

            # 记录成功
            post_id_result = result['id']
            post_url = result['link']
            post_status = result['status']

            self.log(
                f"✅ WordPress 文章{'更新' if post_id else '创建'}成功！\n"
                f"   文章 ID: {post_id_result}\n"
                f"   状态: {post_status}\n"
                f"   URL: {post_url}",
                level="info",
                force=True
            )

            if has_math:
                self.log(
                    "⚠️  文章包含数学公式，请确保 WordPress 已安装 MathJax 插件",
                    level="warning",
                    force=True
                )

            return post_id_result

        except requests.exceptions.RequestException as e:
            self.log(f"❌ WordPress API 请求失败: {e}", level="error", force=True)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    self.log(f"错误详情: {error_data}", level="error", force=True)
                except:
                    self.log(f"响应内容: {e.response.text[:500]}", level="error", force=True)
            return None
        except Exception as e:
            self.log(f"❌ 发布失败: {e}", level="error", force=True)
            import traceback
            self.log(traceback.format_exc(), level="error")
            return None
