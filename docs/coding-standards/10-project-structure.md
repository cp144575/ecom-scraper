# Project Structure and Dependency Boundary Standard

## 1. Structure

建议最终：

```text
src/ecom_scraper/
├── engine/
├── request/
├── scheduler/
├── queue/
├── concurrency/
├── retry/
├── rate_limit/
├── fetcher/
├── proxy/
├── platform/
├── parser/
├── pipeline/
├── models/
├── storage/
├── analysis/
├── observability/
└── api/
```

## 2. Dependency Direction

推荐：

```text
API
 ↓
Application / Task
 ↓
Engine
 ↓
Fetcher
 ↓
Platform / Parser
 ↓
Pipeline
 ↓
Repository
 ↓
Storage
```

分析：

```text
Storage
 ↓
Analysis
 ↓
Analytics API
```

## 3. Core Does Not Know Platform

核心 Engine 不允许 import：

```text
jd
taobao
amazon
```

反过来 Platform Adapter 可以依赖稳定 Core Interface。

## 4. Platform Isolation

平台之间不能相互依赖：

```text
JD → Taobao  ❌
Amazon → JD  ❌
```

共同逻辑进入：

```text
platform/base
core
shared
```

## 5. Spider Rules

Spider 不允许直接：

```text
DB
Redis internals
Proxy Pool internals
Browser internals
```

必须通过抽象：

```text
Fetcher
Queue
Repository
Proxy Policy
```

## 6. Fetcher Rules

统一接口：

```python
class Fetcher(Protocol):
    async def fetch(self, request: Request) -> Response:
        ...
```

实现：

```text
AioHttpFetcher
PlaywrightFetcher
ScraplingFetcher
```

## 7. No God Objects

禁止：

```text
CrawlerManager
EcomManager
SystemManager
UtilsManager
```

一个类包揽：

```text
Queue
Proxy
DB
Logging
Retry
Scheduling
```

## 8. Utils

`utils/` 只能保存真正通用的无状态工具。

业务逻辑不能大量堆进 `utils.py`。

## 9. Circular Dependency

出现循环依赖时，不应通过：

```python
import ...  # inside function
```

长期隐藏问题。

优先重新设计模块边界。

## 10. Public Interface

跨模块依赖必须通过稳定接口，而不是访问另一个模块的私有变量。

禁止：

```python
worker._internal_queue
```

作为模块间长期依赖。
