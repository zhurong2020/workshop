# P0任务执行指南

> 详细的逐步执行指南，用于完成P0优先级任务
> **创建时间**: 2026-01-28
> **执行建议**: 手动执行以确保安全

---

## ⚠️ 重要说明

P0任务涉及**破坏性操作**（Git历史重写）和**远程推送**，建议**手动执行**以确保：
1. 充分理解每个步骤的影响
2. 在关键节点进行验证
3. 出现问题时可以及时回滚

---

## 🔴 Task P0-1: Git历史清理 - cardiac-ml-research

### ⚠️ 任务性质

- **破坏性**: 会重写整个Git历史
- **影响**: 所有commit SHA会改变
- **协作影响**: Dr. Chen需要重新克隆或fetch
- **风险**: 中等（仓库为私有，已备份）

### 📋 执行步骤

#### 步骤1: 备份仓库（重要！）

```bash
# 进入项目父目录
cd /home/wuxia/projects

# 创建带时间戳的备份
cp -r cardiac-ml-research cardiac-ml-research-backup-$(date +%Y%m%d-%H%M%S)

# 验证备份成功
ls -lh | grep cardiac-ml-research
```

**预期结果**: 看到两个目录
```
drwxr-xr-x cardiac-ml-research
drwxr-xr-x cardiac-ml-research-backup-20260128-100530
```

---

#### 步骤2: 检查当前状态

```bash
cd cardiac-ml-research

# 确保工作区干净
git status

# 确认要清理的文件确实在历史中
git log --all --full-history -- "archive/old_tools/cardiac_calcium_scoring_20251103/keys/private_key.pem" | head -20
```

**预期结果**: 应该看到commit历史（如果看到说明文件在历史中）

---

#### 步骤3: 安装git-filter-repo

```bash
# 检查是否已安装
which git-filter-repo

# 如果未安装，使用pip安装
pip install git-filter-repo

# 验证安装
git-filter-repo --version
```

**预期结果**: 显示版本号，例如 `git-filter-repo 2.38.0`

---

#### 步骤4: 执行历史清理（⚠️ 破坏性操作）

```bash
# 确保在cardiac-ml-research目录中
pwd  # 应该显示 /home/wuxia/projects/cardiac-ml-research

# 清理private_key.pem的所有历史
git filter-repo \
  --path archive/old_tools/cardiac_calcium_scoring_20251103/keys/private_key.pem \
  --invert-paths \
  --force

# 清理public_key.pem的所有历史
git filter-repo \
  --path archive/old_tools/cardiac_calcium_scoring_20251103/keys/public_key.pem \
  --invert-paths \
  --force
```

**注意**:
- `--force` 是必需的，因为会重写历史
- 执行后，远程仓库配置会被删除（这是正常的）

**预期结果**:
```
Parsed X commits
New history written in Y seconds...
```

---

#### 步骤5: 验证清理效果

```bash
# 检查文件是否还在历史中（应该返回空）
git log --all --full-history -- "archive/old_tools/cardiac_calcium_scoring_20251103/keys/private_key.pem"

# 检查本地文件是否还存在（应该还在）
ls -la archive/old_tools/cardiac_calcium_scoring_20251103/keys/
```

**预期结果**:
- `git log` 命令应该返回空（无历史记录）
- `ls` 命令应该显示文件仍在本地（如果需要的话）

---

#### 步骤6: 重新添加远程仓库

```bash
# 添加远程仓库（filter-repo会删除远程配置）
git remote add origin https://github.com/zhurong2020/cardiac-ml-research.git

# 验证远程仓库
git remote -v
```

**预期结果**:
```
origin  https://github.com/zhurong2020/cardiac-ml-research.git (fetch)
origin  https://github.com/zhurong2020/cardiac-ml-research.git (push)
```

---

#### 步骤7: 强制推送到远程（⚠️ 破坏性操作）

```bash
# 检查当前分支
git branch

# 强制推送到远程main分支
git push origin main --force

# 如果推送失败，检查分支名称可能是master
# git push origin master --force
```

**预期结果**:
```
+ xxx...yyy main -> main (forced update)
```

**⚠️ 警告**: 这会**重写远程仓库历史**！Dr. Chen需要重新克隆。

---

#### 步骤8: 通知协作者

如果Dr. Chen也在使用这个仓库，发送通知：

```
Hi Dr. Chen,

我刚刚清理了cardiac-ml-research仓库的Git历史（移除了意外提交的密钥文件）。

请执行以下操作来同步：

方案A（推荐）- 重新克隆:
git clone https://github.com/zhurong2020/cardiac-ml-research.git cardiac-ml-research-new

方案B - 强制更新（如果有本地修改）:
cd cardiac-ml-research
git fetch origin
git reset --hard origin/main

注意：所有commit SHA已改变。
```

---

#### 步骤9: 最终验证

```bash
# 验证远程仓库的历史中没有密钥文件
git clone https://github.com/zhurong2020/cardiac-ml-research.git /tmp/verify-clean
cd /tmp/verify-clean
git log --all --full-history -- "archive/old_tools/cardiac_calcium_scoring_20251103/keys/private_key.pem"

# 应该返回空
```

---

### ✅ 完成标准

- [ ] 备份仓库已创建
- [ ] git-filter-repo已安装
- [ ] 历史清理成功执行
- [ ] 验证：git log显示无密钥文件历史
- [ ] 远程仓库已重新添加
- [ ] 强制推送成功
- [ ] 协作者已通知（如适用）
- [ ] 最终验证通过

---

### 🔄 回滚方案

如果需要回滚：

```bash
# 删除清理后的仓库
cd /home/wuxia/projects
rm -rf cardiac-ml-research

# 恢复备份
cp -r cardiac-ml-research-backup-XXXXXX cardiac-ml-research

# 进入恢复的仓库
cd cardiac-ml-research
git status
```

---

## 🔴 Task P0-2: 推送所有安全修复到远程

### 📋 推送清单

执行以下命令推送所有安全修复：

#### 1. Workshop项目（10 commits）

```bash
cd /home/wuxia/projects/workshop
git status
git push origin main
```

**预期结果**:
```
Enumerating objects: XX, done.
...
main -> main
```

---

#### 2. cardiac-ai-cac（1 commit）

```bash
cd /home/wuxia/projects/cardiac-ai-cac
git status
git push origin main
```

---

#### 3. cardiac-ml-research（清理后推送）

⚠️ 此项目在完成P0-1任务后已推送，跳过此步骤。

---

#### 4. claude-colab-projects（1 commit）

```bash
cd /home/wuxia/projects/claude-colab-projects
git status
git push origin main
```

---

#### 5. digital-lipid-management（1 commit）

```bash
cd /home/wuxia/projects/digital-lipid-management
git status
git push origin main
```

---

#### 6. test-colab-cli（1 commit）

```bash
cd /home/wuxia/projects/test-colab-cli
git status
git push origin master  # ⚠️ 注意：这个项目用master分支
```

---

#### 7. zhurong2020.github.io（1 commit）

```bash
cd /home/wuxia/projects/zhurong2020.github.io
git status
git push origin main
```

---

### 📜 批量推送脚本（可选）

如果想一次性推送所有项目（除cardiac-ml-research外）：

```bash
#!/bin/bash
# 保存为: /tmp/push_all_security_fixes.sh

projects=(
    "workshop:main"
    "cardiac-ai-cac:main"
    "claude-colab-projects:main"
    "digital-lipid-management:main"
    "test-colab-cli:master"
    "zhurong2020.github.io:main"
)

base_dir="/home/wuxia/projects"
failed_projects=()

echo "开始批量推送安全修复..."
echo "======================================"

for proj in "${projects[@]}"; do
    IFS=':' read -r name branch <<< "$proj"
    echo ""
    echo "📦 推送 $name (分支: $branch) ..."
    cd "$base_dir/$name"

    if git push origin "$branch" 2>&1; then
        echo "✅ $name 推送成功"
    else
        echo "❌ $name 推送失败"
        failed_projects+=("$name")
    fi
done

echo ""
echo "======================================"
echo "推送完成"

if [ ${#failed_projects[@]} -eq 0 ]; then
    echo "✅ 所有项目推送成功！"
else
    echo "⚠️  以下项目推送失败："
    for proj in "${failed_projects[@]}"; do
        echo "  - $proj"
    done
    exit 1
fi
```

**使用方法**:
```bash
chmod +x /tmp/push_all_security_fixes.sh
bash /tmp/push_all_security_fixes.sh
```

---

### ✅ 完成标准

- [ ] workshop - 推送成功
- [ ] cardiac-ai-cac - 推送成功
- [ ] cardiac-ml-research - 已在P0-1中推送
- [ ] claude-colab-projects - 推送成功
- [ ] digital-lipid-management - 推送成功
- [ ] test-colab-cli - 推送成功
- [ ] zhurong2020.github.io - 推送成功

---

## 📊 进度更新指令

完成每个任务后，更新进度文件：

### 更新P0-1完成状态

```bash
# 在TASK_EXECUTION_PROGRESS.md中标记完成
# 手动编辑或使用sed命令更新
```

### 更新P0-2完成状态

同上。

---

## 🎯 完成P0任务后的下一步

完成P0任务后：
1. 更新 `docs/TASK_EXECUTION_PROGRESS.md`
2. 查看 `docs/REMAINING_TASKS_ROADMAP_2026-01-28.md` 中的P1任务
3. 开始执行P1预防性安全加固（8个项目）

---

## 🆘 遇到问题？

### Git历史清理失败

**问题**: git filter-repo执行失败

**解决**:
1. 确保工作区干净（`git status`）
2. 确保没有未提交的修改
3. 尝试使用`--force`参数
4. 查看详细错误信息

---

### 推送失败

**问题**: git push失败

**常见原因**:
1. 网络问题 - 检查网络连接
2. 权限问题 - 确认GitHub凭证
3. 分支保护 - 检查GitHub分支保护规则
4. 没有本地commits - 检查`git log`

**解决**:
```bash
# 检查远程连接
git remote -v

# 检查本地commits
git log --oneline -5

# 尝试详细输出
git push origin main --verbose
```

---

**维护者**: Claude Code
**版本**: v1.0
**创建时间**: 2026-01-28
