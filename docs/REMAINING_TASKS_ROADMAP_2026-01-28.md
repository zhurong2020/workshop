# 剩余任务路线图

> 系统化推进workspace最佳实践的后续任务
> **创建时间**: 2026-01-28
> **最后更新**: 2026-01-28

---

## 📊 任务总览

| 优先级 | 任务类别 | 任务数 | 预计时间 | 状态 |
|--------|---------|--------|---------|------|
| **P0** | Git历史清理 | 1 | 30分钟 | 待执行 |
| **P0** | 远程推送 | 7 | 15分钟 | 待执行 |
| **P1** | 预防性安全加固 | 8 | 1小时 | 待执行 |
| **P1** | 项目深度评估 | 21 | 8-12小时 | 待规划 |
| **P2** | Workspace2评估 | 1 | 4-6小时 | 待开始 |
| **P2** | 自动化工具 | 3 | 2-3小时 | 待开始 |
| **P3** | 长期改进 | 多项 | 持续 | 待规划 |

---

## 🔴 P0 优先级（紧急重要）

### 1. Git历史清理 - cardiac-ml-research ⚠️ CRITICAL

**任务**: 使用git filter-repo清理RSA私钥的git历史记录

**背景**:
- `private_key.pem`和`public_key.pem`已从git追踪中移除
- 但密钥仍然存在于git历史中（2025-11-03首次提交）
- 仓库为私有，但应遵循最佳实践完全清理

**执行步骤**:

```bash
# 1. 进入项目目录
cd /home/wuxia/projects/cardiac-ml-research

# 2. 备份仓库（重要！）
cd ..
cp -r cardiac-ml-research cardiac-ml-research-backup-$(date +%Y%m%d)
cd cardiac-ml-research

# 3. 确保工作区干净
git status

# 4. 安装git-filter-repo（如果未安装）
pip install git-filter-repo

# 5. 清理私钥文件的所有历史记录
git filter-repo --path archive/old_tools/cardiac_calcium_scoring_20251103/keys/private_key.pem --invert-paths --force
git filter-repo --path archive/old_tools/cardiac_calcium_scoring_20251103/keys/public_key.pem --invert-paths --force

# 6. 重新添加远程仓库（filter-repo会删除）
git remote add origin https://github.com/zhurong2020/cardiac-ml-research.git

# 7. 强制推送到远程（仓库为私有，风险可控）
git push origin main --force

# 8. 验证清理效果
git log --all --full-history -- "archive/old_tools/cardiac_calcium_scoring_20251103/keys/private_key.pem"
# 应该返回空（无历史记录）
```

**风险评估**:
- 风险：git filter-repo会重写历史，所有commit SHA会改变
- 缓解：仓库为私有，只有你和Dr. Chen有权限
- 缓解：已创建备份
- 影响：Dr. Chen需要重新克隆或fetch --force

**后续**: 如果RSA密钥仍在使用，应生成新密钥对

**预计时间**: 30分钟

---

### 2. 推送所有安全修复到远程仓库

**任务**: 将所有本地安全修复commit推送到远程仓库

**需要推送的项目** (7个):

```bash
# 1. Workshop项目（10个commits）
cd /home/wuxia/projects/workshop
git push origin main

# 2. cardiac-ai-cac（1个commit）
cd /home/wuxia/projects/cardiac-ai-cac
git push origin main

# 3. cardiac-ml-research（1个commit + filter-repo后的历史）
cd /home/wuxia/projects/cardiac-ml-research
# 先执行上面的git filter-repo清理，再push

# 4. claude-colab-projects（1个commit）
cd /home/wuxia/projects/claude-colab-projects
git push origin main

# 5. digital-lipid-management（1个commit）
cd /home/wuxia/projects/digital-lipid-management
git push origin main

# 6. test-colab-cli（1个commit）
cd /home/wuxia/projects/test-colab-cli
git push origin master  # 注意：这个项目用的是master分支

# 7. zhurong2020.github.io（1个commit）
cd /home/wuxia/projects/zhurong2020.github.io
git push origin main
```

**一键批量推送脚本**:

```bash
#!/bin/bash
# 批量推送所有安全修复

projects=(
    "workshop:main"
    "cardiac-ai-cac:main"
    "claude-colab-projects:main"
    "digital-lipid-management:main"
    "test-colab-cli:master"
    "zhurong2020.github.io:main"
)

base_dir="/home/wuxia/projects"

for proj in "${projects[@]}"; do
    IFS=':' read -r name branch <<< "$proj"
    echo "推送 $name ..."
    cd "$base_dir/$name"
    git push origin "$branch" && echo "✅ $name 推送成功" || echo "❌ $name 推送失败"
done

echo ""
echo "注意：cardiac-ml-research需要单独处理（git filter-repo + force push）"
```

**预计时间**: 15分钟

---

## 🟡 P1 优先级（重要）

### 3. 预防性安全加固 - 8个项目

**任务**: 对8个项目的.gitignore加强.env排除规则

**项目列表**:
1. cardiac-shared
2. claude-scientific-skills
3. cnnvideo-timer
4. docuforge
5. paper-writing-toolkit-source
6. schwabgridtrader
7. smartnews-lite
8. vbca

**当前状态**: 这些项目的.gitignore未明确排除.env，但当前无.env文件被追踪

**修复方案**:

对每个项目，检查并更新.gitignore：

```bash
# 检查模板
cd /home/wuxia/projects/[项目名]

# 检查.gitignore是否有.env排除
grep -n "^\.env" .gitignore

# 如果没有，添加以下规则（在合适位置）
# Environment variables
.env
.env.local
.env.*.local
*.env
```

**批量处理脚本**:

```bash
#!/bin/bash
# 批量检查并修复.env排除规则

projects=(
    "cardiac-shared"
    "claude-scientific-skills"
    "cnnvideo-timer"
    "docuforge"
    "paper-writing-toolkit-source"
    "schwabgridtrader"
    "smartnews-lite"
    "vbca"
)

base_dir="/home/wuxia/projects"

for proj in "${projects[@]}"; do
    echo "检查 $proj ..."
    cd "$base_dir/$proj"

    if ! grep -q "^\.env" .gitignore 2>/dev/null; then
        echo "  需要修复：.gitignore缺少.env排除"
        # 提示手动修复或自动添加
    else
        echo "  ✅ 已有.env排除规则"
    fi
done
```

**预计时间**: 1小时（8个项目 × 平均7-8分钟）

---

### 4. arong-unified其他项目深度评估

**任务**: 对21个项目进行完整的最佳实践评估（P1-P3问题）

**评估维度**:
1. **配置管理** (P1)
   - .env.example是否存在
   - 配置文件组织是否清晰
   - 敏感配置是否混在非敏感配置中
   - 是否有配置验证脚本

2. **文档完整性** (P1-P2)
   - README.md是否完整
   - 是否有快速开始指南
   - 是否有故障排查文档
   - 是否有贡献者指南
   - 是否有迁移文档

3. **开发工具** (P2)
   - 是否有启动脚本
   - 是否有测试框架
   - 是否有CI/CD配置
   - 是否有代码格式化工具

4. **项目组织** (P1-P2)
   - 目录结构是否清晰
   - 是否有冗余或重复文件
   - 依赖管理是否规范

**评估方法**:
- 使用workshop项目的评估模板
- 逐项检查，记录问题
- 按优先级分类
- 制定改造计划

**项目分组建议**:

**第一批 - 核心研究项目** (优先评估):
- ai-cac-research
- cardiac-ml-research (已有基础)
- cardiac-ai-cac (已有基础)
- cardiac-shared
- vbca
- pcfa

**第二批 - 工具和辅助项目**:
- paper-writing-toolkit
- paper-writing-toolkit-source
- docuforge
- claude-scientific-skills
- claude-colab-projects

**第三批 - 其他项目**:
- bizassist
- cnnvideo-timer
- digital-lipid-management
- home
- moomoo_custom_strategies
- schwabgridtrader
- smartnews-lite
- test-colab-cli
- vpsserver
- zhurong2020.github.io

**预计时间**:
- 第一批（6个项目）: 3-4小时
- 第二批（5个项目）: 2-3小时
- 第三批（10个项目）: 3-5小时
- **总计**: 8-12小时（可分多次进行）

---

## 🟢 P2 优先级（建议）

### 5. cardiac-research Workspace评估

**任务**: 评估并改造cardiac-research workspace（如果存在）

**背景**:
- 用户提到有"cardiac-research"这个workspace
- 目前尚未确认路径和包含的项目

**执行步骤**:

```bash
# 1. 确认workspace位置
# 可能的位置：
# - VS Code workspace文件: *.code-workspace
# - 单独的目录
# - 或者就是cardiac-ml-research项目本身

# 2. 列出项目
ls -la [cardiac-research路径]

# 3. 应用相同的评估流程
# - P0安全扫描
# - P1配置管理评估
# - P2文档和工具评估
```

**预计时间**: 4-6小时（取决于项目数量）

---

### 6. 自动化工具建设

**任务**: 建立持续的最佳实践维护机制

#### 6.1 Pre-commit Hook（防止敏感文件提交）

**目标**: 在git commit前自动检查敏感文件

**实现方案**:

```bash
# 为关键项目创建.git/hooks/pre-commit

#!/bin/bash
# Pre-commit hook: 防止敏感文件提交

# 检查是否有.env文件被staged
if git diff --cached --name-only | grep -q "^\.env$"; then
    echo "❌ 错误：不能提交.env文件！"
    echo "请将.env添加到.gitignore"
    exit 1
fi

# 检查是否有密钥文件被staged
if git diff --cached --name-only | grep -E "\.(pem|key|p12|pfx)$"; then
    echo "❌ 错误：不能提交密钥文件！"
    git diff --cached --name-only | grep -E "\.(pem|key|p12|pfx)$"
    exit 1
fi

exit 0
```

**推广策略**:
- 先在关键项目试用（cardiac-ml-research, ai-cac-research）
- 验证效果后推广到其他项目

---

#### 6.2 定期安全扫描任务

**目标**: 每月自动执行P0安全扫描

**实现方案**:

```bash
# 创建cron任务或定期手动执行

# 脚本：/home/wuxia/scripts/monthly_security_scan.sh
#!/bin/bash
bash /tmp/claude/.../scratchpad/p0_security_scan.sh
# 发送报告到邮件或保存到固定位置
```

---

#### 6.3 配置管理工具改进

**目标**: 扩展workshop的配置验证工具，支持其他项目

**改进方向**:
- 通用化`validate_config.py`，支持任意项目
- 添加自动修复功能
- 集成到CI/CD流程

**预计时间**: 2-3小时

---

## 🔵 P3 优先级（长期改进）

### 7. 文档体系完善

**任务**: 为核心项目建立workshop级别的文档体系

**包括**:
- DOCS_MAP.md - 文档导航
- TROUBLESHOOTING.md - 故障排查
- CONTRIBUTING.md - 贡献指南
- 智能启动脚本

**适用项目**:
- ai-cac-research
- cardiac-ml-research
- vbca

---

### 8. 测试覆盖提升

**任务**: 为关键项目添加或完善测试

**评估标准**:
- 是否有测试框架
- 核心功能是否有测试
- 测试覆盖率是否足够

---

### 9. CI/CD集成

**任务**: 建立持续集成和持续部署流程

**包括**:
- GitHub Actions工作流
- 自动化测试
- 自动化安全扫描
- 自动化部署

---

## 🗓️ 推荐执行顺序

### 第一阶段：紧急安全（今天完成）

**时间**: 1小时

1. ✅ Git历史清理 - cardiac-ml-research (30分钟)
2. ✅ 推送所有安全修复 (15分钟)
3. ✅ 验证推送成功 (15分钟)

---

### 第二阶段：预防性加固（本周完成）

**时间**: 1-2小时

1. ✅ 8个项目的.env排除规则加强 (1小时)
2. ✅ 验证修复效果 (30分钟)
3. ✅ 提交并推送 (30分钟)

---

### 第三阶段：深度评估（分批进行）

**时间**: 8-12小时（可分多次）

**周一**: 核心研究项目评估（3-4小时）
- ai-cac-research
- cardiac-shared
- vbca
- pcfa

**周二**: 工具项目评估（2-3小时）
- paper-writing-toolkit系列
- docuforge
- claude-scientific-skills

**周三**: 其他项目评估（3-5小时）
- 剩余10个项目批量评估

**周四**: cardiac-research workspace（4-6小时）
- 如果存在，进行完整评估

---

### 第四阶段：自动化建设（按需进行）

**时间**: 2-3小时

1. Pre-commit hook部署
2. 定期扫描任务设置
3. 配置管理工具改进

---

### 第五阶段：长期改进（持续）

根据实际需求和优先级逐步推进。

---

## 📋 快速启动指令

### 今天立即执行（P0）

```bash
# 1. Git历史清理
cd /home/wuxia/projects/cardiac-ml-research
# 执行上述git filter-repo步骤

# 2. 批量推送
# 执行批量推送脚本或逐个推送
```

### 本周执行（P1）

```bash
# 预防性加固
# 对8个项目加强.env排除
```

### 下周规划（P1-P2）

```
开始深度评估第一批项目
```

---

## 🔗 相关文档

- `docs/P0_SECURITY_SCAN_REPORT_2026-01-28.md` - P0安全审计报告
- `docs/WORKSPACE_BEST_PRACTICES_ROADMAP.md` - 总体路线图
- `docs/MIGRATION_GUIDE.md` - 迁移指南
- `DOCS_MAP.md` - 文档导航

---

## 📊 进度跟踪

### P0任务进度

- [ ] Git历史清理 - cardiac-ml-research
- [ ] 推送workshop项目（10 commits）
- [ ] 推送cardiac-ai-cac
- [ ] 推送cardiac-ml-research（清理后）
- [ ] 推送claude-colab-projects
- [ ] 推送digital-lipid-management
- [ ] 推送test-colab-cli
- [ ] 推送zhurong2020.github.io

### P1任务进度

- [ ] cardiac-shared - .env排除加强
- [ ] claude-scientific-skills - .env排除加强
- [ ] cnnvideo-timer - .env排除加强
- [ ] docuforge - .env排除加强
- [ ] paper-writing-toolkit-source - .env排除加强
- [ ] schwabgridtrader - .env排除加强
- [ ] smartnews-lite - .env排除加强
- [ ] vbca - .env排除加强

### 深度评估进度（21个项目）

- [ ] 第一批（6个核心研究项目）
- [ ] 第二批（5个工具项目）
- [ ] 第三批（10个其他项目）

---

**维护者**: Rong Zhu + Claude Code
**版本**: v1.0
**最后更新**: 2026-01-28
