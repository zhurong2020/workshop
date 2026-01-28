# 第二阶段任务清单

> **创建时间**: 2026-01-28
> **阶段**: 关键改进（CI/CD + 测试）
> **状态**: 待开始
> **预计时间**: 8-12小时

---

## 📋 任务总览

| 分类 | 任务数 | 预计时间 | 优先级 |
|------|--------|---------|--------|
| Tier 2关键应用 | 4项 | 4-6小时 | 最高 |
| Tier 1核心研究 | 4项 | 4小时 | 高 |
| 依赖管理补充 | 2项 | 20分钟 | 中 |
| **合计** | **10项** | **8-12小时** | - |

---

## 🎯 优先级排序（基于项目演进）

### 最高优先级: smartnews-lite ⭐

**理由**:
- 活跃开发项目
- cnnvideo-timer的继任者
- 商业化Web平台

**任务清单**:
- [ ] 添加GitHub Actions CI/CD
  - Node.js测试工作流
  - ESLint代码检查
  - 预计时间: 1小时

- [ ] 添加测试框架
  - 前端测试（Jest）
  - API测试（可选）
  - 预计时间: 1.5-2小时

- [ ] 建立docs/目录
  - API文档
  - 部署指南
  - 用户手册
  - 预计时间: 30分钟-1小时

**预计总时间**: 3-4小时

---

### 高优先级: Tier 2其他关键应用

#### 1. moomoo_custom_strategies

**当前状态**: 评分85/100 (B)

**任务清单**:
- [ ] 添加pytest测试框架
  - 策略验证测试
  - 回测测试
  - 预计时间: 2小时

**预计总时间**: 2小时

---

#### 2. vpsserver

**当前状态**: 评分82/100 (B)

**任务清单**:
- [ ] 添加测试框架（可选）
  - 配置验证测试
  - 服务健康检查测试
  - 预计时间: 1小时

**预计总时间**: 1小时（可选）

---

#### 3. bizassist

**当前状态**: 评分75/100 (B-)

**任务清单**:
- [ ] 添加GitHub Actions CI/CD
  - Node.js测试工作流
  - ESLint代码检查
  - 预计时间: 1小时

- [ ] 添加测试框架
  - API测试
  - 数据库测试
  - 预计时间: 1.5-2小时

**预计总时间**: 2.5-3小时

---

### 高优先级: Tier 1核心研究（4项）

#### 1. ai-cac-research

**当前状态**: 评分87/100 (B+)

**任务清单**:
- [ ] 添加GitHub Actions CI/CD
  - Python测试工作流
  - pytest自动运行
  - 预计时间: 1小时

---

#### 2. cardiac-shared

**当前状态**: 评分84/100 (B)

**任务清单**:
- [ ] 添加GitHub Actions CI/CD
  - Python测试工作流
  - pytest自动运行
  - 预计时间: 1小时

---

#### 3. vbca

**当前状态**: 评分82/100 (B)

**任务清单**:
- [ ] 添加GitHub Actions CI/CD
  - Python测试工作流
  - pytest自动运行
  - 预计时间: 1小时

---

#### 4. pcfa

**当前状态**: 评分80/100 (B)

**任务清单**:
- [ ] 添加GitHub Actions CI/CD
  - Python测试工作流
  - pytest自动运行
  - 预计时间: 1小时

**Tier 1预计总时间**: 4小时

---

### 中优先级: 依赖管理补充（2项）

#### 1. claude-scientific-skills

**任务清单**:
- [ ] 创建requirements.txt
  - 列出所有依赖包
  - 固定版本号
  - 预计时间: 10分钟

---

#### 2. claude-colab-projects

**任务清单**:
- [ ] 创建requirements.txt
  - 列出所有依赖包
  - 固定版本号
  - 预计时间: 10分钟

**依赖管理预计总时间**: 20分钟

---

## 📊 预期成效

### 改进前（第一阶段后）

```
CI/CD覆盖率:     24% (5/21)
测试框架覆盖率:   43% (9/21)
平均评分:        77.5/100
```

---

### 改进后（第二阶段后）

```
CI/CD覆盖率:     60% (13/21) ⬆️ +36%
测试框架覆盖率:   65% (14/21) ⬆️ +22%
平均评分:        80.0/100    ⬆️ +2.5
```

---

### 项目评分提升预测

| 项目 | 第一阶段后 | 第二阶段后 | 提升 |
|------|-----------|-----------|------|
| smartnews-lite | 78 | 84 | +6 |
| moomoo_custom_strategies | 85 | 88 | +3 |
| bizassist | 75 | 82 | +7 |
| ai-cac-research | 87 | 91 | +4 |
| cardiac-shared | 84 | 88 | +4 |
| vbca | 82 | 86 | +4 |
| pcfa | 80 | 84 | +4 |

---

## 🛠️ 实施模板

### Python项目CI/CD模板

**文件**: `.github/workflows/python-tests.yml`

```yaml
name: Python Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest tests/ --cov=./ --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

### Node.js项目CI/CD模板

**文件**: `.github/workflows/node-tests.yml`

```yaml
name: Node.js Tests

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14.x, 16.x, 18.x]

    steps:
    - uses: actions/checkout@v3

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Run linter
      run: npm run lint
```

---

## 📋 执行步骤

### 阶段1: 最高优先级（3-4小时）

**smartnews-lite完整配置**:

1. 创建`.github/workflows/`目录
2. 添加Node.js CI/CD配置
3. 添加Jest测试框架
4. 建立docs/目录
5. 测试CI/CD管道

---

### 阶段2: Tier 1核心研究（4小时）

**批量添加CI/CD**:

```bash
# 为每个项目创建相同的Python CI/CD配置
for project in ai-cac-research cardiac-shared vbca pcfa; do
  mkdir -p /home/wuxia/projects/$project/.github/workflows
  cp python-tests.yml /home/wuxia/projects/$project/.github/workflows/
  # 提交并推送
done
```

---

### 阶段3: 其他Tier 2项目（2.5-3小时）

**按优先级处理**:

1. moomoo_custom_strategies: 添加测试
2. bizassist: 添加CI/CD + 测试
3. vpsserver: 可选

---

### 阶段4: 依赖管理（20分钟）

**快速修复**:

```bash
cd /home/wuxia/projects/claude-scientific-skills
pip freeze > requirements.txt

cd /home/wuxia/projects/claude-colab-projects
pip freeze > requirements.txt
```

---

## ⚠️ 注意事项

### 组织仓库权限

以下2个项目需要组织权限才能推送CI/CD配置：

1. **paper-writing-toolkit-source** (chenqz-hub)
   - 已有LICENSE和.env.example等待推送
   - CI/CD配置也需要组织权限

2. **claude-scientific-skills** (K-Dense-AI)
   - 已有.env.example等待推送
   - CI/CD配置也需要组织权限

**建议**: 在添加CI/CD前先解决权限问题。

---

## 📈 成功指标

### 定量指标

- [ ] CI/CD覆盖率达到60%以上
- [ ] 测试框架覆盖率达到65%以上
- [ ] 平均评分提升到80+
- [ ] 所有Tier 1和Tier 2关键项目有CI/CD

---

### 定性指标

- [ ] 代码质量自动检查
- [ ] PR合并前自动测试
- [ ] 持续集成流程建立
- [ ] 测试覆盖率可见

---

## 🔄 与第三阶段的关系

**第二阶段**: 关键项目CI/CD + 测试
**第三阶段**: 批量完善（CONTRIBUTING + 文档优化）

第二阶段完成后，第三阶段可以：
- 复用CI/CD经验批量推广
- 基于测试框架优化文档
- 建立统一的CONTRIBUTING指南

---

## 📚 相关文档

1. **GLOBAL_PROJECTS_SUMMARY_AND_REMEDIATION.md** - 全局整改计划
2. **PHASE1_FINAL_STATUS_REPORT.md** - 第一阶段总结
3. **PHASE2_TASKS_TODO.md** - 本文档

---

## 🎯 启动指令（未来使用）

当准备开始第二阶段时：

```
请开始第二阶段整改任务。

参考文档: docs/PHASE2_TASKS_TODO.md

优先级:
1. smartnews-lite (最高优先级，3-4小时)
2. Tier 1核心研究 (4项，4小时)
3. 其他Tier 2项目 (按需)

预计总时间: 8-12小时

请从smartnews-lite开始。
```

---

**文档版本**: v1.0
**创建时间**: 2026-01-28
**状态**: 待开始
**创建者**: Claude Code
