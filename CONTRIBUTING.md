# 🤝 贡献指南

> 欢迎为有心工坊贡献代码！本指南帮助你快速上手。

**最后更新**: 2026-01-28

---

## 🚀 快速开始

### 前置要求

- Python 3.8+ (推荐 3.12+)
- Git 2.x+
- 基本的Python和命令行知识

### 开发环境设置

```bash
# 1. Fork项目到你的GitHub账号
# 访问: https://github.com/zhurong2020/workshop
# 点击右上角 Fork

# 2. 克隆你的Fork
git clone git@github.com:YOUR_USERNAME/workshop.git
cd workshop

# 3. 添加上游仓库
git remote add upstream git@github.com:zhurong2020/workshop.git

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的配置

# 7. 验证配置
python scripts/tools/validate_config.py

# 8. 运行测试
python -m pytest tests/
```

---

## 📋 贡献流程

### 1. 创建Issue（可选但推荐）

在开始工作前，先创建或查找相关Issue：

- **Bug报告**: 详细描述问题、复现步骤、期望行为
- **功能建议**: 说明需求、使用场景、预期效果
- **文档改进**: 指出不清晰或遗漏的部分

### 2. 创建功能分支

```bash
# 同步主分支
git checkout main
git pull upstream main

# 创建功能分支（命名规范）
git checkout -b feature/your-feature-name   # 新功能
git checkout -b fix/bug-description         # Bug修复
git checkout -b docs/what-to-update         # 文档更新
git checkout -b refactor/what-to-refactor   # 重构
```

### 3. 开发和测试

```bash
# 开发过程中频繁提交
git add .
git commit -m "feat: 添加XXX功能"

# 运行测试确保没有破坏现有功能
python -m pytest tests/

# 如果修改了配置相关代码
python scripts/tools/config_standardization.py
python scripts/tools/validate_config.py
```

### 4. 提交Pull Request

```bash
# 推送到你的Fork
git push origin feature/your-feature-name

# 在GitHub上创建Pull Request
# 访问: https://github.com/YOUR_USERNAME/workshop
# 点击 "Pull Request" → "New Pull Request"
```

**PR标题格式**:
```
<type>: <简短描述>

type可以是:
- feat: 新功能
- fix: Bug修复
- docs: 文档更新
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关
```

**PR描述模板**:
```markdown
## 变更描述
简要说明这个PR做了什么

## 相关Issue
Closes #123 (如果有)

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构
- [ ] 测试

## 测试
说明如何测试这些变更

## 截图（如适用）
添加截图帮助说明

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加/更新测试
- [ ] 已更新相关文档
- [ ] 所有测试通过
- [ ] 无IDE Error级别警告
```

---

## 📐 代码规范

### Python代码风格

**遵循 PEP 8**:
```python
# 好的示例
def process_article(file_path: str, config: Dict[str, Any]) -> bool:
    """
    处理文章文件

    Args:
        file_path: 文章文件路径
        config: 配置字典

    Returns:
        处理是否成功
    """
    if not Path(file_path).exists():
        logger.error(f"File not found: {file_path}")
        return False

    # 处理逻辑
    return True
```

**关键要点**:
- 使用类型注解（Type hints）
- 添加docstring（Google风格）
- 函数名使用snake_case
- 类名使用PascalCase
- 常量使用UPPER_CASE
- 行长度不超过100字符（灵活处理）

### 文件组织

```python
# 文件头部顺序
"""
模块docstring
"""

# 1. 标准库导入
import os
import sys

# 2. 第三方库导入
import yaml
import requests

# 3. 本地导入
from scripts.utils.config_loader import ConfigLoader

# 4. 类型导入（可选）
from typing import Dict, List, Optional

# 5. 常量定义
DEFAULT_TIMEOUT = 30

# 6. 类和函数定义
class MyClass:
    pass

def my_function():
    pass
```

### 错误处理

```python
# 好的错误处理
try:
    result = process_data(data)
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    return None
except ValueError as e:
    logger.warning(f"Invalid data: {e}")
    return None
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise

# 避免裸except
try:
    risky_operation()
except:  # ❌ 不好
    pass

# 使用具体的异常
try:
    risky_operation()
except SpecificError as e:  # ✅ 好
    handle_error(e)
```

---

## 🧪 测试规范

### 编写测试

```python
# tests/test_feature.py
import pytest
from scripts.core.my_module import my_function

def test_my_function_success():
    """测试正常情况"""
    result = my_function("valid_input")
    assert result is not None
    assert result.status == "success"

def test_my_function_with_invalid_input():
    """测试异常输入"""
    with pytest.raises(ValueError):
        my_function("invalid_input")

def test_my_function_with_mock(mocker):
    """测试使用mock"""
    mock_api = mocker.patch('scripts.core.my_module.api_call')
    mock_api.return_value = {"status": "ok"}

    result = my_function("test")
    assert result["status"] == "ok"
    mock_api.assert_called_once()
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_feature.py

# 运行特定测试函数
python -m pytest tests/test_feature.py::test_my_function_success

# 显示详细输出
python -m pytest tests/ -v

# 显示代码覆盖率
python -m pytest tests/ --cov=scripts
```

### 测试要求

- ✅ 核心功能必须有测试覆盖
- ✅ Bug修复要添加回归测试
- ✅ 新功能要有单元测试
- ✅ 测试要能独立运行
- ✅ 测试要有清晰的命名和文档

---

## 📝 文档规范

### 代码文档

```python
def complex_function(param1: str, param2: int, option: bool = False) -> Dict[str, Any]:
    """
    简短的一句话描述

    详细说明可以多行，解释函数的用途、注意事项等。

    Args:
        param1: 参数1的说明
        param2: 参数2的说明
        option: 可选参数的说明（默认值: False）

    Returns:
        返回值的说明，包含数据结构

    Raises:
        ValueError: 当输入无效时
        FileNotFoundError: 当文件不存在时

    Example:
        >>> result = complex_function("test", 42)
        >>> print(result['status'])
        'success'
    """
    pass
```

### Markdown文档

**文档结构**:
```markdown
# 标题（H1，每个文档只有一个）

> 简短的说明或引用

**最后更新**: YYYY-MM-DD

---

## 主要章节（H2）

### 子章节（H3）

内容...

#### 更小的章节（H4，谨慎使用）

---

**维护者**: 姓名
**文档版本**: v1.0
```

**代码块要指定语言**:
```markdown
    ```python
    # Python代码
    ```

    ```bash
    # Shell命令
    ```
```

### 更新现有文档

- 修改功能时同步更新相关文档
- 添加新功能要更新 DOCS_MAP.md
- Bug修复要更新 TROUBLESHOOTING.md（如适用）
- 配置变更要更新 .env.example 和相关文档

---

## 🔧 配置管理最佳实践

### 新增配置项

1. **在 `.env.example` 中添加示例**:
   ```bash
   # 功能描述
   # 获取地址: https://...
   NEW_API_KEY=your-api-key-here
   ```

2. **在 `config/app.yml` 中添加非敏感配置**:
   ```yaml
   new_feature:
     enabled: true
     timeout: 30
   ```

3. **更新 `scripts/utils/config_loader.py`** (如需要)

4. **更新配置验证**:
   ```python
   # 在 scripts/tools/validate_config.py 中添加验证
   required_vars = {
       'NEW_API_KEY': '新功能API密钥',
   }
   ```

5. **更新文档**:
   - `docs/API_KEYS_REGISTRY.md` - 记录API密钥信息
   - 相关的setup文档

### 配置文件命名规范

- 敏感配置: `*.json` 在 `.gitignore` 中排除
- 示例配置: `*.example.json` 进入版本控制
- 非敏感功能配置: `*.yml` 进入版本控制
- Token/密钥: 存储在 `.env`

---

## 🎨 Commit规范

### Commit Message格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `refactor`: 重构（不改变功能）
- `test`: 测试相关
- `chore`: 构建工具、依赖更新等
- `style`: 代码格式（不影响功能）
- `perf`: 性能优化

**示例**:
```bash
# 好的commit
feat(wordpress): 添加Gutenberg自动转换功能
fix(onedrive): 修复token过期导致的上传失败
docs(migration): 更新迁移指南添加故障排查章节
refactor(menu): 简化菜单处理逻辑

# 不好的commit
update code  # ❌ 太模糊
fix bug      # ❌ 没有说明修了什么
```

### Commit要求

- 单个commit做一件事
- Commit message清晰描述变更
- 频繁commit，不要积累太多变更
- 不提交调试代码和临时文件
- 不提交敏感信息（API密钥等）

---

## 🔐 安全要求

### 必须遵守

1. **永远不要提交敏感信息**:
   - API密钥、密码、Token
   - 私钥文件
   - 真实的用户数据

2. **使用 `.gitignore`**:
   - 确保敏感文件被排除
   - 提交前运行 `git status` 检查

3. **配置示例文件**:
   - 使用占位符（`YOUR_KEY_HERE`）
   - 提供获取密钥的链接
   - 注明安全注意事项

4. **代码安全**:
   - 验证用户输入
   - 使用参数化查询（如操作数据库）
   - 避免命令注入、XSS等漏洞

### 安全检查清单

提交前检查：
- [ ] 没有硬编码的API密钥
- [ ] `.env`文件未被追踪
- [ ] 示例配置使用占位符
- [ ] 日志不包含敏感信息
- [ ] 用户输入已验证

---

## 🏗️ 项目结构理解

### 核心模块

```
scripts/
├── core/                    # 核心业务逻辑
│   ├── processors/          # 数据处理器
│   ├── validators/          # 内容验证器
│   ├── workflows/           # 工作流引擎
│   └── managers/            # 管理器模块
├── cli/                     # 命令行界面
├── utils/                   # 通用工具
└── tools/                   # 独立工具
    ├── config_standardization.py    # 配置检查
    ├── validate_config.py           # 配置验证
    └── prepare_migration.sh         # 迁移准备
```

### 添加新功能

**步骤**:
1. 在合适的模块添加代码
2. 添加单元测试
3. 更新相关文档
4. 在菜单系统中添加入口（如需要）
5. 更新 CHANGELOG

**示例：添加新的发布平台**:
```python
# 1. 创建适配器
# scripts/core/processors/platforms/new_platform_adapter.py
class NewPlatformAdapter(PlatformAdapter):
    def publish(self, content: Dict) -> PublishResult:
        # 实现发布逻辑
        pass

# 2. 注册适配器
# scripts/core/content_pipeline.py
PLATFORM_ADAPTERS = {
    'wordpress': WordPressAdapter,
    'github_pages': GitHubPagesAdapter,
    'new_platform': NewPlatformAdapter,  # 添加
}

# 3. 添加配置
# config/app.yml
platforms:
  new_platform:
    enabled: true
    api_endpoint: "..."

# 4. 添加测试
# tests/test_new_platform_adapter.py

# 5. 更新文档
# docs/guides/NEW_PLATFORM_GUIDE.md
```

---

## 📊 代码审查标准

PR会被审查以下方面：

### 功能性
- ✅ 功能按预期工作
- ✅ 没有引入新Bug
- ✅ 边界情况处理正确

### 代码质量
- ✅ 遵循PEP 8
- ✅ 有类型注解
- ✅ 有适当的文档
- ✅ 逻辑清晰易懂
- ✅ 无IDE Error级别警告

### 测试覆盖
- ✅ 核心逻辑有测试
- ✅ 测试覆盖主要路径
- ✅ 所有测试通过

### 文档完整性
- ✅ 代码有docstring
- ✅ 更新了相关文档
- ✅ README/DOCS_MAP更新（如需要）

### 安全性
- ✅ 无敏感信息泄露
- ✅ 输入验证充分
- ✅ 错误处理得当

---

## 🆘 获取帮助

### 开发过程中遇到问题？

1. **查看文档**:
   - [DOCS_MAP.md](DOCS_MAP.md) - 文档导航
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查
   - [CLAUDE.md](CLAUDE.md) - 开发约定

2. **运行诊断工具**:
   ```bash
   python scripts/tools/validate_config.py
   python scripts/tools/config_standardization.py
   ```

3. **查看现有Issue**:
   - [GitHub Issues](https://github.com/zhurong2020/workshop/issues)

4. **创建新Issue**:
   - 详细描述问题
   - 包含错误信息
   - 说明系统环境

---

## 🎉 成为贡献者

提交PR后，你的贡献会被记录在：

- 项目README.md的贡献者名单
- CHANGELOG中相关版本的变更
- Git历史中

感谢你的贡献，让有心工坊变得更好！

---

## 📚 推荐阅读

- [Python风格指南 - PEP 8](https://pep8.org/)
- [Git工作流](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [如何写好Commit Message](https://chris.beams.io/posts/git-commit/)
- [测试驱动开发](https://en.wikipedia.org/wiki/Test-driven_development)

---

**维护者**: Rong Zhu + Claude Code
**最后更新**: 2026-01-28
**文档版本**: v1.0
