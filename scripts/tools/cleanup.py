#!/usr/bin/env python3
"""
项目清理工具
清理临时文件、缓存和日志，保持项目整洁
"""

import os
import shutil
import argparse
from pathlib import Path


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent.parent


def clean_python_cache(project_root: Path, dry_run: bool = False) -> int:
    """清理 Python 缓存文件"""
    count = 0
    patterns = ['__pycache__', '*.pyc', '*.pyo', '*.pyd']

    # 清理 __pycache__ 目录
    for pycache in project_root.rglob('__pycache__'):
        if 'venv' in str(pycache) or '.venv' in str(pycache):
            continue
        if dry_run:
            print(f"  [DRY] Would remove: {pycache}")
        else:
            shutil.rmtree(pycache, ignore_errors=True)
        count += 1

    # 清理 .pyc 等文件
    for pattern in ['*.pyc', '*.pyo', '*.pyd']:
        for file in project_root.rglob(pattern):
            if 'venv' in str(file) or '.venv' in str(file):
                continue
            if dry_run:
                print(f"  [DRY] Would remove: {file}")
            else:
                file.unlink(missing_ok=True)
            count += 1

    return count


def clean_test_cache(project_root: Path, dry_run: bool = False) -> int:
    """清理测试缓存"""
    count = 0
    cache_dirs = ['.pytest_cache', '.mypy_cache', '.tox', '.nox', 'htmlcov']

    for cache_name in cache_dirs:
        cache_path = project_root / cache_name
        if cache_path.exists():
            if dry_run:
                print(f"  [DRY] Would remove: {cache_path}")
            else:
                shutil.rmtree(cache_path, ignore_errors=True)
            count += 1

    # 清理 .build 下的缓存
    build_htmlcov = project_root / '.build' / 'htmlcov'
    if build_htmlcov.exists():
        if dry_run:
            print(f"  [DRY] Would remove: {build_htmlcov}")
        else:
            shutil.rmtree(build_htmlcov, ignore_errors=True)
        count += 1

    return count


def clean_logs(project_root: Path, dry_run: bool = False) -> int:
    """清理日志文件"""
    count = 0
    log_dirs = ['logs', '.build/logs']

    for log_dir in log_dirs:
        log_path = project_root / log_dir
        if log_path.exists():
            for log_file in log_path.glob('*.log'):
                if dry_run:
                    print(f"  [DRY] Would remove: {log_file}")
                else:
                    log_file.unlink(missing_ok=True)
                count += 1

    return count


def clean_temp_files(project_root: Path, dry_run: bool = False) -> int:
    """清理临时文件"""
    count = 0

    # 清理 .tmp/cache
    tmp_cache = project_root / '.tmp' / 'cache'
    if tmp_cache.exists():
        for item in tmp_cache.iterdir():
            if item.name == '.gitkeep':
                continue
            if dry_run:
                print(f"  [DRY] Would remove: {item}")
            else:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
            count += 1

    # 清理编辑器临时文件
    for pattern in ['*.swp', '*~', '*.bak', '.DS_Store', 'Thumbs.db']:
        for file in project_root.rglob(pattern):
            if 'venv' in str(file) or '.venv' in str(file) or '.git' in str(file):
                continue
            if dry_run:
                print(f"  [DRY] Would remove: {file}")
            else:
                file.unlink(missing_ok=True)
            count += 1

    return count


def clean_jekyll_cache(project_root: Path, dry_run: bool = False) -> int:
    """清理 Jekyll 构建缓存"""
    count = 0
    jekyll_dirs = ['_site', '.sass-cache', '.jekyll-cache', '.jekyll-metadata']

    for cache_name in jekyll_dirs:
        cache_path = project_root / cache_name
        if cache_path.exists():
            if dry_run:
                print(f"  [DRY] Would remove: {cache_path}")
            else:
                if cache_path.is_dir():
                    shutil.rmtree(cache_path, ignore_errors=True)
                else:
                    cache_path.unlink(missing_ok=True)
            count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description='清理项目临时文件和缓存')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='只显示要删除的内容，不实际删除')
    parser.add_argument('--all', '-a', action='store_true',
                        help='清理所有类型的临时文件')
    parser.add_argument('--python', '-p', action='store_true',
                        help='清理 Python 缓存 (__pycache__, *.pyc)')
    parser.add_argument('--test', '-t', action='store_true',
                        help='清理测试缓存 (.pytest_cache, htmlcov)')
    parser.add_argument('--logs', '-l', action='store_true',
                        help='清理日志文件 (*.log)')
    parser.add_argument('--temp', action='store_true',
                        help='清理临时文件 (.tmp, editor backups)')
    parser.add_argument('--jekyll', '-j', action='store_true',
                        help='清理 Jekyll 构建缓存 (_site, .sass-cache)')

    args = parser.parse_args()

    # 如果没有指定任何选项，显示帮助
    if not any([args.all, args.python, args.test, args.logs, args.temp, args.jekyll]):
        parser.print_help()
        print("\n使用 --all 清理所有类型，或指定特定类型")
        return

    project_root = get_project_root()
    total_count = 0

    if args.dry_run:
        print("=== 试运行模式 (不会实际删除) ===\n")

    # 执行清理
    if args.all or args.python:
        print("清理 Python 缓存...")
        count = clean_python_cache(project_root, args.dry_run)
        print(f"  已清理 {count} 个项目")
        total_count += count

    if args.all or args.test:
        print("清理测试缓存...")
        count = clean_test_cache(project_root, args.dry_run)
        print(f"  已清理 {count} 个项目")
        total_count += count

    if args.all or args.logs:
        print("清理日志文件...")
        count = clean_logs(project_root, args.dry_run)
        print(f"  已清理 {count} 个项目")
        total_count += count

    if args.all or args.temp:
        print("清理临时文件...")
        count = clean_temp_files(project_root, args.dry_run)
        print(f"  已清理 {count} 个项目")
        total_count += count

    if args.all or args.jekyll:
        print("清理 Jekyll 缓存...")
        count = clean_jekyll_cache(project_root, args.dry_run)
        print(f"  已清理 {count} 个项目")
        total_count += count

    print(f"\n总计清理 {total_count} 个项目")


if __name__ == '__main__':
    main()
