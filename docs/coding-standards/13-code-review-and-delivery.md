# Code Review and Delivery Standard

## 1. Review Before Merge

任何核心模块变更必须经过 Review：

```text
Code
+
Tests
+
Architecture
+
Security
```

## 2. Review Order

```text
Correctness
 ↓
Architecture
 ↓
Error Handling
 ↓
Concurrency
 ↓
Performance
 ↓
Tests
 ↓
Style
```

不要只纠结格式而忽略行为错误。

## 3. Changed Files

提交前检查：

```bash
git diff
git status
```

确认没有：

```text
debug code
temporary files
secrets
unrelated changes
```

## 4. Quality Commands

统一：

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

## 5. Commit Scope

优先：

```text
一个 Milestone
一个小提交
```

示例：

```text
feat(v2): add async downloader
feat(v2): add retry policy
test(v2): add downloader tests
```

不要把多个不相关功能塞到一个提交。

## 6. AI Completion Standard

AI 不得只说：

```text
“实现完成”
```

必须报告：

```text
Changed Files
Behavior Changes
Tests
Lint
Type Check
Known Limitations
```

## 7. Verification

没有实际运行：

```text
pytest
Ruff
mypy
```

不得声称验证通过。

## 8. Refactoring

重构前必须明确：

```text
Current Behavior
Desired Behavior
Risk
Tests
Rollback
```

大规模重构必须先 Plan。

## 9. Definition of Done

```text
□ Goal 完成
□ Scope 未扩大
□ 测试通过
□ Ruff 通过
□ mypy 通过
□ 无明显资源泄漏
□ 无明显阻塞 IO
□ 无敏感信息
□ 文档更新
□ Git diff 已检查
□ Commit 清晰
```
