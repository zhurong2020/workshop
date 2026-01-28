#!/usr/bin/env python3
"""
配置标准化工具
用于在迁移前统一配置管理，实现最佳实践
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any


class ConfigStandardizer:
    """配置标准化工具"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.env_file = self.project_root / ".env"
        self.backup_dir = self.project_root / "config" / "backup"

    def run_standardization(self):
        """执行完整的标准化流程"""
        print("🚀 开始配置标准化...")
        print("=" * 60)

        # 1. 创建备份
        self.create_backup()

        # 2. 检查敏感配置
        issues = self.check_sensitive_configs()

        # 3. 报告问题
        self.report_issues(issues)

        # 4. 提供改造建议
        self.provide_recommendations(issues)

        print("\n✅ 配置标准化检查完成！")

    def create_backup(self):
        """创建配置备份"""
        print("\n📦 创建配置备份...")

        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)

        # 备份关键配置文件
        files_to_backup = [
            "onedrive_config.json",
            "onedrive_tokens.json",
            "youtube_oauth_credentials.json",
            "youtube_oauth_token.json",
        ]

        for filename in files_to_backup:
            src = self.config_dir / filename
            if src.exists():
                dst = self.backup_dir / f"{filename}.backup"
                shutil.copy2(src, dst)
                print(f"  ✓ 已备份: {filename}")

    def check_sensitive_configs(self) -> Dict[str, Any]:
        """检查敏感配置"""
        print("\n🔍 检查敏感配置...")

        issues = {
            "git_tracked_sensitive": [],
            "duplicate_configs": [],
            "missing_examples": [],
            "env_issues": [],
        }

        # 1. 检查被git追踪的敏感文件
        onedrive_config = self.config_dir / "onedrive_config.json"
        if onedrive_config.exists():
            # 检查是否包含真实凭据
            with open(onedrive_config, 'r') as f:
                config = json.load(f)
                auth = config.get('auth', {})
                if not auth.get('tenant_id', '').startswith('YOUR_'):
                    issues['git_tracked_sensitive'].append({
                        'file': 'config/onedrive_config.json',
                        'issue': '包含真实凭据但被git追踪',
                        'severity': 'HIGH'
                    })

        # 2. 检查配置重复
        env_vars = self._read_env_file()
        if 'ONEDRIVE_TENANT_ID' in env_vars and onedrive_config.exists():
            issues['duplicate_configs'].append({
                'config': 'OneDrive认证',
                'locations': ['.env', 'config/onedrive_config.json'],
                'recommendation': '应该只在.env中存储'
            })

        # 3. 检查示例文件
        sensitive_files = [
            'onedrive_config.json',
            'youtube_oauth_credentials.json',
        ]

        for filename in sensitive_files:
            example_file = self.config_dir / f"{filename.replace('.json', '.example.json')}"
            if not example_file.exists():
                issues['missing_examples'].append({
                    'file': filename,
                    'example': example_file.name
                })

        # 4. 检查.env必需变量
        required_vars = [
            'GEMINI_API_KEY',
            'ONEDRIVE_TENANT_ID',
            'ONEDRIVE_CLIENT_ID',
            'ONEDRIVE_CLIENT_SECRET',
            'WORDPRESS_USERNAME',
            'WORDPRESS_APP_PASSWORD',
        ]

        missing_vars = [var for var in required_vars if var not in env_vars]
        if missing_vars:
            issues['env_issues'].append({
                'type': 'missing_required',
                'vars': missing_vars
            })

        return issues

    def _read_env_file(self) -> Dict[str, str]:
        """读取.env文件"""
        env_vars = {}
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _ = line.split('=', 1)
                        env_vars[key] = 'exists'
        return env_vars

    def report_issues(self, issues: Dict[str, Any]):
        """报告发现的问题"""
        print("\n📊 问题报告：")
        print("-" * 60)

        total_issues = sum(len(v) for v in issues.values())

        if total_issues == 0:
            print("  ✅ 未发现配置问题，配置管理符合最佳实践！")
            return

        # 报告git追踪的敏感文件
        if issues['git_tracked_sensitive']:
            print("\n⚠️  【高危】被Git追踪的敏感文件：")
            for item in issues['git_tracked_sensitive']:
                print(f"  - {item['file']}: {item['issue']}")

        # 报告重复配置
        if issues['duplicate_configs']:
            print("\n⚠️  配置重复：")
            for item in issues['duplicate_configs']:
                print(f"  - {item['config']}")
                print(f"    位置: {', '.join(item['locations'])}")
                print(f"    建议: {item['recommendation']}")

        # 报告缺失示例
        if issues['missing_examples']:
            print("\n⚠️  缺少示例文件：")
            for item in issues['missing_examples']:
                print(f"  - {item['file']} -> 建议创建 {item['example']}")

        # 报告环境变量问题
        if issues['env_issues']:
            print("\n⚠️  环境变量问题：")
            for item in issues['env_issues']:
                if item['type'] == 'missing_required':
                    print(f"  - 缺少必需变量: {', '.join(item['vars'])}")

    def provide_recommendations(self, issues: Dict[str, Any]):
        """提供改造建议"""
        print("\n💡 改造建议：")
        print("-" * 60)

        recommendations = []

        # 1. Git追踪问题
        if issues['git_tracked_sensitive']:
            recommendations.append({
                'priority': 1,
                'title': '移除git追踪的敏感文件',
                'steps': [
                    'git rm --cached config/onedrive_config.json',
                    '将真实凭据移到.env中',
                    '在.gitignore中添加 config/onedrive_config.json',
                    '保留 config/onedrive_config.example.json 作为模板'
                ]
            })

        # 2. 配置整合
        if issues['duplicate_configs']:
            recommendations.append({
                'priority': 2,
                'title': '整合重复配置',
                'steps': [
                    '将所有敏感信息集中到.env文件',
                    '修改ConfigLoader支持从环境变量读取OneDrive配置',
                    '配置文件只保留非敏感的功能性配置'
                ]
            })

        # 3. 创建示例文件
        if issues['missing_examples']:
            recommendations.append({
                'priority': 3,
                'title': '创建配置模板',
                'steps': [
                    f'为每个敏感配置文件创建.example版本',
                    '在示例文件中使用占位符（YOUR_XXX）',
                    '在README中说明如何配置'
                ]
            })

        # 4. 虚拟环境统一
        recommendations.append({
            'priority': 4,
            'title': '统一虚拟环境命名',
            'steps': [
                '将当前的 venv/ 重命名为 .venv/',
                '更新相关脚本和文档',
                '在.gitignore中确保两种命名都被排除'
            ]
        })

        # 5. 创建配置验证脚本
        recommendations.append({
            'priority': 5,
            'title': '创建配置验证工具',
            'steps': [
                '创建 scripts/tools/validate_config.py',
                '检查所有必需的配置项',
                '在迁移文档中使用'
            ]
        })

        # 按优先级排序并输出
        recommendations.sort(key=lambda x: x['priority'])

        for rec in recommendations:
            print(f"\n【优先级 {rec['priority']}】{rec['title']}")
            for i, step in enumerate(rec['steps'], 1):
                print(f"  {i}. {step}")

    def apply_fixes(self, auto_fix: bool = False):
        """应用修复（可选）"""
        if not auto_fix:
            print("\n❓ 提示：运行 --apply-fixes 参数可以自动应用部分修复")
            return

        print("\n🔧 应用自动修复...")

        # TODO: 实现自动修复逻辑
        # 1. 创建示例文件
        # 2. 更新.gitignore
        # 3. 重命名虚拟环境

        print("  ⚠️  自动修复功能开发中，请手动执行建议的步骤")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='配置标准化工具 - 在迁移前统一配置管理'
    )
    parser.add_argument(
        '--apply-fixes',
        action='store_true',
        help='自动应用部分修复（谨慎使用）'
    )

    args = parser.parse_args()

    standardizer = ConfigStandardizer()
    standardizer.run_standardization()

    if args.apply_fixes:
        standardizer.apply_fixes(auto_fix=True)


if __name__ == "__main__":
    main()
