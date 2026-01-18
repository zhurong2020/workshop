"""
Gemini AI 客户端封装
使用新版 google-genai SDK，提供向后兼容的接口
"""
import os
import logging
from typing import Optional, Dict, Any, Union
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 尝试导入新版 SDK
try:
    from google import genai
    from google.genai import types
    NEW_SDK_AVAILABLE = True
except ImportError:
    NEW_SDK_AVAILABLE = False
    genai = None
    types = None


class GeminiClient:
    """Gemini AI 客户端封装类"""

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        """
        初始化 Gemini 客户端

        Args:
            api_key: API密钥，如果不提供则从环境变量读取
            model_name: 模型名称
        """
        if GeminiClient._initialized:
            return

        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.client = None
        self.api_available = False

        if not NEW_SDK_AVAILABLE:
            self.logger.error("google-genai SDK 未安装，请运行: pip install google-genai")
            return

        # 获取 API 密钥
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self.logger.warning("未找到 GEMINI_API_KEY 环境变量")
            return

        try:
            # 创建客户端实例
            self.client = genai.Client(api_key=self.api_key)
            self.api_available = True
            self.logger.debug(f"Gemini 客户端初始化成功，使用模型: {model_name}")
            GeminiClient._initialized = True
        except Exception as e:
            self.logger.error(f"Gemini 客户端初始化失败: {e}")

    def generate_content(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
        top_p: float = 0.95,
        model: Optional[str] = None
    ) -> Optional[str]:
        """
        生成内容

        Args:
            prompt: 提示词
            temperature: 温度参数
            max_output_tokens: 最大输出 token 数
            top_p: top_p 参数
            model: 可选的模型名称覆盖

        Returns:
            生成的文本内容，失败时返回 None
        """
        if not self.api_available or not self.client:
            self.logger.warning("API 不可用")
            return None

        try:
            # 构建配置
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p
            )

            # 调用 API
            response = self.client.models.generate_content(
                model=model or self.model_name,
                contents=prompt,
                config=config
            )

            if response and response.text:
                return response.text
            return None

        except Exception as e:
            self.logger.error(f"生成内容失败: {e}")
            return None

    def test_connection(self) -> bool:
        """
        测试 API 连接

        Returns:
            连接是否成功
        """
        if not self.api_available:
            return False

        try:
            result = self.generate_content(
                "Test connection",
                temperature=0.1,
                max_output_tokens=10
            )
            return result is not None
        except Exception as e:
            self.logger.error(f"连接测试失败: {e}")
            return False


class GenerativeModelCompat:
    """
    兼容层：模拟旧版 GenerativeModel 接口
    便于渐进式迁移
    """

    def __init__(self, model_name: str, client: Optional[GeminiClient] = None):
        """
        初始化兼容模型

        Args:
            model_name: 模型名称
            client: GeminiClient 实例
        """
        self.model_name = model_name
        self._client = client or GeminiClient(model_name=model_name)

    def generate_content(
        self,
        prompt: str,
        generation_config: Union[Dict[str, Any], "GenerationConfigCompat", None] = None,
        safety_settings: Optional[Any] = None
    ):
        """
        生成内容（兼容旧接口）

        Args:
            prompt: 提示词
            generation_config: 生成配置（字典或 GenerationConfigCompat）
            safety_settings: 安全设置（已弃用，新版SDK自动处理）

        Returns:
            ResponseCompat 对象
        """
        # safety_settings 在新版 SDK 中已弃用，但保留参数以兼容旧代码
        if safety_settings:
            logging.getLogger(__name__).debug("safety_settings 参数已弃用，将被忽略")
        # 解析配置
        temp = 0.7
        max_tokens = 8192
        top_p = 0.95

        if generation_config:
            if isinstance(generation_config, dict):
                temp = generation_config.get('temperature', temp)
                max_tokens = generation_config.get('max_output_tokens', max_tokens)
                top_p = generation_config.get('top_p', top_p)
            elif hasattr(generation_config, 'temperature'):
                temp = getattr(generation_config, 'temperature', temp)
                max_tokens = getattr(generation_config, 'max_output_tokens', max_tokens)
                top_p = getattr(generation_config, 'top_p', top_p)

        text = self._client.generate_content(
            prompt=prompt,
            temperature=temp,
            max_output_tokens=max_tokens,
            top_p=top_p
        )

        return ResponseCompat(text)


class ResponseCompat:
    """响应兼容类"""

    def __init__(self, text: Optional[str]):
        self.text = text

    def __bool__(self):
        return self.text is not None


class GenerationConfigCompat:
    """GenerationConfig 兼容类"""

    def __init__(
        self,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
        top_p: float = 0.95,
        **kwargs
    ):
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        # 存储其他参数以便未来扩展
        for key, value in kwargs.items():
            setattr(self, key, value)


# 便捷函数：配置 API（兼容旧代码）
def configure(api_key: str):
    """
    配置 API 密钥（兼容旧接口）

    Args:
        api_key: API 密钥
    """
    # 设置环境变量供后续使用
    os.environ["GEMINI_API_KEY"] = api_key
    # 重置单例以便重新初始化
    GeminiClient._instance = None
    GeminiClient._initialized = False


# 导出兼容类型
GenerativeModel = GenerativeModelCompat
GenerationConfig = GenerationConfigCompat
