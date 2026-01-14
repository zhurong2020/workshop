#!/usr/bin/env python3
"""
验证Gemini模型配置和可用性
使用新版 google-genai SDK
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 使用新版 google-genai SDK
from google import genai

def main():
    """验证Gemini 2.5模型配置"""
    # 加载环境变量
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("未找到GEMINI_API_KEY环境变量")
        return False

    try:
        # 创建客户端
        client = genai.Client(api_key=api_key)

        # 获取可用模型列表
        print("正在获取可用模型列表...")
        models_response = client.models.list()
        model_names = [model.name for model in models_response]

        print(f"共找到 {len(model_names)} 个可用模型:")
        for name in sorted(model_names):
            if 'gemini' in name.lower():
                print(f"  {name}")

        # 检查Gemini 2.5模型可用性
        target_models = ['gemini-2.5-flash', 'gemini-2.5-pro']
        available_target_models = []

        for target in target_models:
            matching = [name for name in model_names if target in name]
            if matching:
                available_target_models.append(matching[0])
                print(f"[OK] {target} - 可用")
            else:
                print(f"[X] {target} - 不可用")

        if available_target_models:
            # 测试第一个可用的2.5模型
            test_model = available_target_models[0]
            print(f"\n测试模型: {test_model}")

            # 使用新 SDK 的 generate_content 方法
            response = client.models.generate_content(
                model=test_model,
                contents="简单介绍一下Gemini AI模型"
            )

            if response.text:
                print(f"[OK] 模型测试成功")
                print(f"响应长度: {len(response.text)} 字符")
                print(f"响应片段: {response.text[:100]}...")
                return True
            else:
                print("[X] 模型响应为空")
                return False
        else:
            print("[X] 没有找到可用的Gemini 2.5模型")
            return False

    except Exception as e:
        print(f"[X] 验证过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)