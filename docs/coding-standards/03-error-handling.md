# Error Handling and Retry Standard

## 1. Goals

错误处理必须做到：

```text
可区分
可追踪
可恢复
不吞错
不泄露敏感信息
```

## 2. Exception Hierarchy

建议：

```text
EcomScraperError
├── ConfigurationError
├── RequestError
├── FetchError
├── TimeoutError
├── ParseError
├── ValidationError
├── PersistenceError
├── TaskError
└── PlatformError
```

业务代码优先捕获具体异常。

## 3. 禁止裸 except

禁止：

```python
try:
    ...
except:
    pass
```

禁止：

```python
except Exception:
    return None
```

除非明确记录、转换或重新抛出。

## 4. Preserve Cause

需要转换异常时：

```python
try:
    ...
except aiohttp.ClientError as exc:
    raise FetchError("Failed to fetch product") from exc
```

不要丢失原始异常链。

## 5. Retry

Retry 必须集中在：

```text
RetryPolicy
```

不能让每个平台自己写 while/for 重试循环。

配置：

```text
max_attempts
retryable_statuses
retryable_exceptions
backoff
jitter
```

禁止无限重试。

## 6. Retry Classification

不是所有错误都应该 Retry。

需要区分：

```text
Transient
Permanent
Unknown
```

例如：

```text
Timeout
Connection reset
503
```

通常属于 transient 候选。

而：

```text
Invalid URL
Schema error
Programming error
```

通常不应盲目 retry。

具体策略必须基于当前平台和业务定义。

## 7. Backoff

推荐：

```text
Exponential Backoff
+
Jitter
```

避免多个 Worker 在同一时间同时重试。

## 8. Error Context

异常必须尽可能提供：

```text
task_id
request_id
platform
url
status_code
attempt
```

但不能写入：

```text
password
token
完整 Cookie
secret
```

## 9. Error Boundary

建议按边界处理：

```text
Fetcher
→ FetchError

Parser
→ ParseError

Validator
→ ValidationError

Repository
→ PersistenceError

Platform Adapter
→ PlatformError
```

不要在每个函数里重复进行全局异常处理。

## 10. Error Handling Checklist

- 是否捕获了具体异常？
- 是否保留原始异常？
- 是否需要 Retry？
- Retry 是否有上限？
- 是否泄露敏感信息？
- 是否带有 task/request/platform 上下文？
- 是否正确统计 Metrics？
- 是否需要进入失败任务队列？
