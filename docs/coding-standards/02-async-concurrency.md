# Async and Concurrency Coding Standard

## 1. Scope

适用于 V2+ Async Engine，以及所有网络、Redis、数据库、浏览器相关代码。

## 2. Async-first

V2 开始：

```text
HTTP IO        → aiohttp
Redis IO       → redis.asyncio
Database IO    → SQLAlchemy Async
Browser        → Playwright Async API
```

禁止在 Async Core 中直接使用同步阻塞 IO：

```python
requests.get(...)
time.sleep(...)
同步 DB API
```

## 3. Event Loop

Event Loop 必须保持可调度。

禁止：

```python
for item in huge_dataset:
    expensive_cpu_operation(item)
```

长时间阻塞 Event Loop。

CPU 密集型任务必要时转移到专用线程/进程执行。

## 4. Task Creation

禁止无限：

```python
asyncio.create_task(...)
```

错误：

```python
for url in urls:
    asyncio.create_task(fetch(url))
```

应使用：

```text
Queue
+
Worker
+
Semaphore / Concurrency Controller
+
Backpressure
```

## 5. Concurrency vs Rate

两者必须分离：

```text
Concurrency
→ 同时执行多少任务

Rate
→ 单位时间启动多少请求
```

例如：

```text
Concurrency = 100
Rate = 20 req/s
```

不允许把二者混成一个配置。

## 6. Semaphore

并发边界应有明确 owner：

```text
Global
Domain
Platform
Fetcher
Browser
```

不要到处创建私有 Semaphore，造成不可控的总并发。

## 7. Backpressure

生产者不得无限快于消费者。

必须控制：

```text
Queue Size
Task Count
Memory
Browser Count
DB Writes
```

当队列达到阈值：

```text
Producer
 ↓
Backpressure
 ↓
减速/暂停
```

## 8. Cancellation

异步任务必须支持取消。

不要无意义吞掉：

```python
asyncio.CancelledError
```

资源清理放在：

```python
finally:
    ...
```

## 9. Timeout

所有外部 IO 必须有 timeout：

```text
HTTP
Redis
Database
Browser
External API
```

禁止无限等待。

## 10. aiohttp

项目核心 HTTP Client：

```python
aiohttp.ClientSession
```

Session 长生命周期复用。

禁止：

```python
async with aiohttp.ClientSession():
    ...
```

在每个请求里重新创建 Session。

推荐：

```text
Worker
 ↓
Fetcher
 ↓
Long-lived ClientSession
 ↓
Connection Pool
```

## 11. Browser Concurrency

Browser 并发必须独立于 HTTP：

```text
HTTP = high concurrency
Browser = low concurrency
```

禁止：

```text
1000 requests
→ 1000 browser instances
```

使用：

```text
Browser Pool
Browser Context
Page
```

## 12. Async Code Review

Review 必须检查：

- 是否存在阻塞调用
- 是否无限创建 Task
- 是否存在无限 Queue
- 是否缺少 timeout
- 是否正确处理 cancellation
- 是否存在 resource leak
- 是否有 backpressure
- 是否有合理的 concurrency owner
