# RSA密钥泄露详细分析

> **发现日期**: 2026-01-28
> **项目**: cardiac-ml-research
> **严重程度**: MEDIUM-HIGH（仓库私有，但不应在版本控制中）

---

## 🔍 泄露内容详情

### 泄露的文件

**位置**: `archive/old_tools/cardiac_calcium_scoring_20251103/keys/`

1. **private_key.pem** (1,704字节)
   - RSA私钥
   - 格式：PKCS#8
   - 用途：签名软件许可证

2. **public_key.pem** (451字节)
   - RSA公钥
   - 格式：X.509
   - 用途：验证软件许可证

### Git历史信息

**首次提交**: 2025-11-03 17:12:08
**Commit**: `4e27b69ba753e716769f43c875de29b6e3b87081`
**提交信息**: 目录重组相关

**历史范围**: 2025-11-03 至 2026-01-28（约3个月）

---

## 🎯 密钥用途分析

### 软件许可证系统

这对RSA密钥用于**cardiac_calcium_scoring工具的许可证验证系统**：

**工作原理**:
```
1. 私钥(private_key.pem) → 生成和签名许可证文件
2. 公钥(public_key.pem) → 分发给用户，验证许可证真伪
```

**代码证据**:
```python
# archive/old_tools/.../cli/validate_license.py
default_key = project_root / "tools" / "cardiac_calcium_scoring" / "keys" / "public_key.pem"

# archive/old_tools/.../cli/calcium_scoring.py
public_key_path = Path(__file__).resolve().parent.parent / "shared" / "licensing" / "public_key.pem"
```

### 当前使用状态

**评估结果**: ⚠️ **可能不再使用**

**证据**:
1. ✅ 密钥位于 `archive/old_tools/` 目录（归档）
2. ✅ 目录名包含日期 `20251103`（旧版本快照）
3. ✅ 当前主代码库未引用这些密钥路径
4. ⚠️ 但无法100%确认是否有其他工具依赖

---

## 🚨 风险评估

### 实际风险：MEDIUM

**缓解因素** (降低风险):
1. ✅ **仓库为私有** - GitHub仓库设置为PRIVATE
   - 只有你和Dr. Chen有访问权限
   - 未公开暴露到互联网

2. ✅ **密钥位于归档目录** - `archive/old_tools/`
   - 表明这是旧版本的工具
   - 可能已被新系统替换

3. ✅ **用途明确** - 软件许可证签名
   - 不是SSH密钥（不能直接登录服务器）
   - 不是API密钥（不能访问外部服务）
   - 影响范围相对有限

**风险因素** (需要关注):
1. ⚠️ **私钥在版本控制中** - 违反安全最佳实践
   - 即使是私有仓库，也不应存储私钥
   - Git历史中永久保存（除非清理）

2. ⚠️ **无法确认是否仍在使用**
   - 如果仍在生成许可证，密钥泄露会有影响
   - 如果已废弃，风险更低

3. ⚠️ **协作者访问** - Dr. Chen也能访问
   - 如果Dr. Chen的账号被攻破，密钥会暴露
   - 需要评估协作者的安全措施

---

## 💡 影响分析

### 如果密钥被恶意使用

**场景1: 密钥仍在使用（生产环境）**
- 攻击者可以：生成伪造的许可证
- 影响：绕过许可证验证，未授权使用软件
- 严重性：HIGH

**场景2: 密钥已废弃（归档状态）**
- 攻击者可以：生成旧版本的许可证
- 影响：可能影响旧版本工具
- 严重性：LOW

**场景3: 仓库继续为私有**
- 当前风险：LOW（只有可信人员访问）
- 前提：仓库不会意外公开

---

## ✅ 推荐行动方案

### 立即执行（P0）

#### 1. Git历史清理 ✅ 已准备

**原因**: 从版本控制中完全移除密钥

**方法**: 使用 git filter-repo（已在P0_TASKS_EXECUTION_GUIDE.md中提供详细步骤）

**完成标准**:
```bash
# 清理后验证（应返回空）
git log --all --full-history -- "archive/old_tools/.../keys/private_key.pem"
```

---

#### 2. 确认密钥使用状态 ⚠️ 需要你确认

**关键问题**:
```
Q1: cardiac_calcium_scoring工具是否仍在使用？
Q2: 是否仍在生成新的许可证？
Q3: 是否有用户在使用基于此密钥的许可证？
```

**检查方法**:
```bash
# 搜索当前代码库中的许可证生成代码
cd /home/wuxia/projects/cardiac-ml-research
grep -r "generate.*license\|sign.*license" --include="*.py" scripts/ src/

# 检查是否有许可证文件
find . -name "*.jwt" -o -name "*license*" | grep -v ".git"

# 检查配置文件中的密钥路径
grep -r "private_key\|public_key" config/ --include="*.yaml" --include="*.json"
```

---

### 根据使用状态决策

#### 场景A: 密钥仍在使用（生产环境）

**推荐**: 🔴 **必须轮换密钥**

**步骤**:
```bash
# 1. 生成新的RSA密钥对
ssh-keygen -t rsa -b 4096 -m PEM -f new_license_key.pem
# 这会生成：
# - new_license_key.pem (私钥)
# - new_license_key.pem.pub (公钥)

# 2. 转换为正确格式（如需要）
openssl rsa -in new_license_key.pem -pubout -out new_public_key.pem

# 3. 更新代码中的密钥路径
# 指向新密钥文件

# 4. 重新生成所有许可证
# 使用新私钥签名

# 5. 分发新公钥给用户
# 更新客户端的公钥文件

# 6. 废弃旧密钥
# 从代码和服务器中删除旧密钥
```

**时间表**:
- 立即：生成新密钥
- 1周内：重新生成许可证
- 2周内：完成用户迁移
- 1个月后：废弃旧密钥

**通知用户**:
```
需要通知所有使用该工具的用户更新公钥文件：
1. 下载新的public_key.pem
2. 替换旧文件
3. 或重新下载工具包
```

---

#### 场景B: 密钥已废弃（归档状态）

**推荐**: 🟡 **清理Git历史即可**

**步骤**:
```bash
# 1. 执行Git历史清理（按P0执行指南操作）
# 2. 可选：删除本地密钥文件（如果确认不再需要）
rm archive/old_tools/cardiac_calcium_scoring_20251103/keys/*.pem

# 3. 提交删除
git add archive/old_tools/cardiac_calcium_scoring_20251103/keys/
git commit -m "security: 删除已废弃的许可证密钥文件"
```

**不需要**:
- ✅ 生成新密钥（已废弃）
- ✅ 重新生成许可证（已废弃）
- ✅ 通知用户（工具已不使用）

---

### 预防性措施（P1）

#### 1. 更新 .gitignore

**已完成**: ✅ cardiac-ml-research的.gitignore已包含

```gitignore
# 第140-150行
*.pem
*.key
*.jwt
**/<private_key.pem
**/public_key.pem
```

#### 2. 密钥管理最佳实践

**建议**:
```bash
# 密钥应存储在git仓库外
# 推荐位置：
~/.ssh/cardiac_ml_keys/
    ├── private_key.pem (chmod 600)
    └── public_key.pem (chmod 644)

# 在代码中使用环境变量引用
export LICENSE_PRIVATE_KEY="$HOME/.ssh/cardiac_ml_keys/private_key.pem"
export LICENSE_PUBLIC_KEY="$HOME/.ssh/cardiac_ml_keys/public_key.pem"
```

#### 3. Pre-commit Hook

创建 `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# 防止提交密钥文件

if git diff --cached --name-only | grep -E "\.(pem|key|p12|pfx)$"; then
    echo "❌ 错误：不能提交密钥文件！"
    git diff --cached --name-only | grep -E "\.(pem|key|p12|pfx)$"
    exit 1
fi
```

---

## 📊 风险矩阵

| 场景 | 密钥状态 | 仓库状态 | 实际风险 | 推荐行动 |
|------|---------|---------|---------|---------|
| A | 生产使用 | 私有 | MEDIUM-HIGH | 必须轮换密钥 |
| B | 生产使用 | 公开 | CRITICAL | 立即轮换+事件响应 |
| C | 已废弃 | 私有 | LOW | 清理Git历史 |
| D | 已废弃 | 公开 | LOW-MEDIUM | 清理历史+公告 |

**当前状态**: 场景A或C（取决于密钥是否仍在使用）

---

## 🔍 确认清单

请确认以下问题以决定最终行动方案：

### 密钥使用状态
- [ ] cardiac_calcium_scoring工具是否仍在使用？
- [ ] 是否仍在生成新的许可证？
- [ ] 当前有多少用户在使用基于此密钥的许可证？
- [ ] 最近一次生成许可证的时间？

### 代码检查结果
```bash
# 执行以下命令并记录结果
cd /home/wuxia/projects/cardiac-ml-research

# 1. 搜索许可证生成代码
grep -r "generate.*license\|sign" --include="*.py" scripts/ src/ 2>/dev/null

# 2. 查找许可证文件
find . -name "*.jwt" -o -name "*license*" | grep -v ".git" | grep -v "old_tools"

# 3. 检查密钥引用
grep -r "private_key.pem\|public_key.pem" scripts/ src/ config/ 2>/dev/null | grep -v "old_tools"
```

### 决策依据

**如果上述命令返回结果** → 密钥可能仍在使用 → **必须轮换密钥（场景A）**

**如果上述命令返回空** → 密钥已废弃 → **只需清理Git历史（场景B）**

---

## 📞 下一步行动

### 立即执行（无论密钥状态）

1. ✅ 执行Git历史清理
   - 使用 `docs/P0_TASKS_EXECUTION_GUIDE.md` 中的步骤
   - 预计时间：30分钟

### 根据确认结果执行

**如果密钥仍在使用**:
2. 🔴 生成新密钥对
3. 🔴 更新代码引用
4. 🔴 重新生成许可证
5. 🔴 通知用户更新

**如果密钥已废弃**:
2. 🟡 可选：删除本地密钥文件
3. 🟡 文档记录（本文档）

---

## 📚 相关文档

- `docs/P0_TASKS_EXECUTION_GUIDE.md` - Git历史清理步骤
- `docs/P0_SECURITY_SCAN_REPORT_2026-01-28.md` - 完整安全审计
- GitHub密钥管理最佳实践: https://docs.github.com/en/authentication

---

**分析完成时间**: 2026-01-28
**分析者**: Claude Code
**建议审查者**: Rong Zhu
**最后更新**: 2026-01-28
