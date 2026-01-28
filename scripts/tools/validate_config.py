#!/usr/bin/env python3
"""
配置验证工具
用于验证环境配置是否完整，特别适用于新环境迁移后的检查
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv


class ConfigValidator:
    """配置验证器"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.env_file = self.project_root / ".env"

        # 加载环境变量
        load_dotenv(self.env_file)

        self.validation_results = {
            'env_vars': [],
            'config_files': [],
            'system_configs': [],
            'tools': [],
        }

    def run_validation(self) -> bool:
        """运行完整验证"""
        print("🔍 开始环境配置验证...")
        print("=" * 60)

        all_passed = True

        # 1. 验证环境变量
        all_passed &= self.validate_env_vars()

        # 2. 验证配置文件
        all_passed &= self.validate_config_files()

        # 3. 验证系统级配置
        all_passed &= self.validate_system_configs()

        # 4. 验证工具链
        all_passed &= self.validate_tools()

        # 5. 生成报告
        self.generate_report()

        return all_passed

    def validate_env_vars(self) -> bool:
        """验证环境变量"""
        print("\n📝 检查环境变量...")

        # 定义必需和可选的环境变量
        required_vars = {
            'GEMINI_API_KEY': 'Google Gemini API密钥',
            'ONEDRIVE_TENANT_ID': 'OneDrive租户ID',
            'ONEDRIVE_CLIENT_ID': 'OneDrive客户端ID',
            'ONEDRIVE_CLIENT_SECRET': 'OneDrive客户端密钥',
        }

        optional_vars = {
            'ELEVENLABS_API_KEY': 'ElevenLabs TTS API密钥',
            'YOUTUBE_API_KEY': 'YouTube Data API密钥',
            'WORDPRESS_USERNAME': 'WordPress用户名',
            'WORDPRESS_APP_PASSWORD': 'WordPress应用专用密码',
            'GITHUB_TOKEN': 'GitHub Personal Access Token',
            'WECHAT_APPID': '微信公众号AppID',
            'WECHAT_APPSECRET': '微信公众号AppSecret',
        }

        all_passed = True

        # 检查必需变量
        for var, description in required_vars.items():
            value = os.getenv(var)
            if value:
                print(f"  ✅ {var}: {description}")
                self.validation_results['env_vars'].append({
                    'var': var,
                    'status': 'ok',
                    'required': True
                })
            else:
                print(f"  ❌ {var}: {description} (缺失)")
                self.validation_results['env_vars'].append({
                    'var': var,
                    'status': 'missing',
                    'required': True
                })
                all_passed = False

        # 检查可选变量
        print("\n  可选配置：")
        for var, description in optional_vars.items():
            value = os.getenv(var)
            if value:
                print(f"  ✅ {var}: {description}")
                self.validation_results['env_vars'].append({
                    'var': var,
                    'status': 'ok',
                    'required': False
                })
            else:
                print(f"  ⚠️  {var}: {description} (未配置)")
                self.validation_results['env_vars'].append({
                    'var': var,
                    'status': 'missing',
                    'required': False
                })

        return all_passed

    def validate_config_files(self) -> bool:
        """验证配置文件"""
        print("\n📁 检查配置文件...")

        required_files = [
            ('config/app.yml', '主配置文件', True),
            ('config/onedrive_tokens.json', 'OneDrive认证Token', False),
            ('config/youtube_oauth_credentials.json', 'YouTube OAuth凭据', False),
            ('config/youtube_oauth_token.json', 'YouTube OAuth Token', False),
        ]

        all_passed = True

        for filepath, description, required in required_files:
            full_path = self.project_root / filepath
            exists = full_path.exists()

            if exists:
                print(f"  ✅ {filepath}: {description}")
                self.validation_results['config_files'].append({
                    'file': filepath,
                    'status': 'ok',
                    'required': required
                })
            else:
                if required:
                    print(f"  ❌ {filepath}: {description} (缺失)")
                    all_passed = False
                else:
                    print(f"  ⚠️  {filepath}: {description} (未配置，某些功能可能不可用)")

                self.validation_results['config_files'].append({
                    'file': filepath,
                    'status': 'missing',
                    'required': required
                })

        return all_passed

    def validate_system_configs(self) -> bool:
        """验证系统级配置"""
        print("\n🔧 检查系统级配置...")

        system_configs = [
            (Path.home() / '.cloudflare' / 'config', 'Cloudflare配置', False),
            (Path.home() / '.ssh' / 'config', 'SSH配置', True),
            (Path.home() / '.ssh' / 'id_ed25519', 'SSH私钥', True),
            (Path.home() / '.gitconfig', 'Git全局配置', True),
            (Path.home() / '.config' / 'gh' / 'hosts.yml', 'GitHub CLI认证', False),
            (Path.home() / '.claude' / '.credentials.json', 'Claude Code认证', False),
        ]

        all_passed = True

        for filepath, description, required in system_configs:
            exists = filepath.exists()

            if exists:
                print(f"  ✅ {description}: {filepath}")
                self.validation_results['system_configs'].append({
                    'file': str(filepath),
                    'status': 'ok',
                    'required': required
                })
            else:
                if required:
                    print(f"  ❌ {description}: {filepath} (缺失)")
                    all_passed = False
                else:
                    print(f"  ⚠️  {description}: {filepath} (未配置)")

                self.validation_results['system_configs'].append({
                    'file': str(filepath),
                    'status': 'missing',
                    'required': required
                })

        return all_passed

    def validate_tools(self) -> bool:
        """验证工具链"""
        print("\n🛠️  检查工具链...")

        tools = [
            ('python3', 'Python 3.12+', True),
            ('git', 'Git版本控制', True),
            ('gh', 'GitHub CLI', False),
            ('claude', 'Claude Code CLI', False),
            ('ruby', 'Ruby (Jekyll依赖)', False),
            ('jekyll', 'Jekyll静态站点生成器', False),
        ]

        all_passed = True

        for tool, description, required in tools:
            # 检查工具是否存在
            import shutil
            tool_path = shutil.which(tool)

            if tool_path:
                # 尝试获取版本
                import subprocess
                try:
                    result = subprocess.run(
                        [tool, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    version = result.stdout.split('\n')[0][:50]
                    print(f"  ✅ {description}: {version}")
                    self.validation_results['tools'].append({
                        'tool': tool,
                        'status': 'ok',
                        'version': version,
                        'required': required
                    })
                except Exception as e:
                    print(f"  ✅ {description}: 已安装 (无法获取版本)")
                    self.validation_results['tools'].append({
                        'tool': tool,
                        'status': 'ok',
                        'version': 'unknown',
                        'required': required
                    })
            else:
                if required:
                    print(f"  ❌ {description}: 未安装")
                    all_passed = False
                else:
                    print(f"  ⚠️  {description}: 未安装 (某些功能可能不可用)")

                self.validation_results['tools'].append({
                    'tool': tool,
                    'status': 'missing',
                    'required': required
                })

        return all_passed

    def generate_report(self):
        """生成验证报告"""
        print("\n" + "=" * 60)
        print("📊 验证报告汇总")
        print("=" * 60)

        # 统计
        total_checks = 0
        passed_checks = 0
        failed_checks = 0
        warnings = 0

        for category in self.validation_results.values():
            for item in category:
                total_checks += 1
                if item['status'] == 'ok':
                    passed_checks += 1
                elif item['status'] == 'missing':
                    if item.get('required', False):
                        failed_checks += 1
                    else:
                        warnings += 1

        print(f"\n总计检查项: {total_checks}")
        print(f"✅ 通过: {passed_checks}")
        print(f"❌ 失败: {failed_checks}")
        print(f"⚠️  警告: {warnings}")

        if failed_checks == 0:
            print("\n🎉 所有必需配置已就绪！")
            if warnings > 0:
                print(f"💡 {warnings}个可选配置未设置，某些功能可能不可用")
        else:
            print(f"\n⚠️  发现 {failed_checks} 个必需配置缺失，请完成配置后重试")

        # 生成JSON报告
        report_file = self.project_root / "config" / "validation_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 详细报告已保存到: {report_file}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='配置验证工具 - 验证环境配置完整性'
    )
    parser.add_argument(
        '--exit-code',
        action='store_true',
        help='失败时返回非零退出码（用于CI/CD）'
    )

    args = parser.parse_args()

    validator = ConfigValidator()
    all_passed = validator.run_validation()

    if args.exit_code and not all_passed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
