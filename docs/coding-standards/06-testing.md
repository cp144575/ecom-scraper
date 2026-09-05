# Testing and Verification Coding Standard

## 1. Test Pyramid

优先级：

```text
Unit Test
   ↑
Integration Test
   ↑
E2E Test
```

不要所有问题都使用 E2E。

## 2. Every Feature Needs Tests

新功能必须先定义：

```text
Happy Path
Error Path
Boundary
Regression
```

并在实现过程中持续验证。

## 3. Unit Tests

适合：

```text
Request
Response
Scheduler
RetryPolicy
RateLimiter
Fingerprint
Parser
Normalizer
Validator
Domain Model
```

## 4. Integration Tests

适合：

```text
Redis
MySQL
aiohttp Fetcher
Repository
Pipeline
```

## 5. Parser Tests

优先使用固定 Fixture：

```text
fixture.html
 ↓
Parser
 ↓
Product
```

不要让所有 Parser 测试依赖真实网站。

## 6. Async Tests

使用：

```text
pytest
pytest-asyncio
```

测试：

```text
aiohttp
Redis Async
SQLAlchemy Async
asyncio
```

## 7. Mock Rules

Mock 外部依赖：

```text
HTTP
Redis
Database
Browser
External APIs
```

不要过度 Mock 自己的核心纯逻辑。

## 8. Regression Tests

任何真实线上问题：

```text
Bug
 ↓
Root Cause
 ↓
Regression Test
 ↓
Fix
```

禁止修完问题却没有对应回归测试。

## 9. Concurrency Tests

V2+ 至少验证：

```text
Concurrency Limit
Rate Limit
Timeout
Cancellation
Backpressure
Duplicate Request
```

## 10. Verification Before Completion

“完成”必须有证据：

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

必要时：

```text
Integration Test
Load Test
E2E
```

如果没有实际运行，不得声称“已验证通过”。

## 11. Test Naming

测试名称描述行为：

```python
def test_scheduler_returns_requests_in_fifo_order():
    ...
```

不要描述实现：

```python
def test_internal_list_pop():
    ...
```

## 12. Test Quality

测试应：

- 独立
- 可重复
- 快速
- 明确失败原因
- 不依赖执行顺序
