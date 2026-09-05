# ecom-scraper 最终技术栈与依赖清单（AI 开发基线）

> 本文档是 `ecom-scraper` 的依赖与基础设施基线。
>
> 项目定位：**自研 Async Crawler Engine + 国内/海外电商多平台采集 + 分布式 Worker + 数据分析 + 生产管理平台**。
>
> 依赖选择原则：
>
> 1. 核心 Engine 自研。
> 2. HTTP、浏览器、HTML Parser、数据库驱动等底层能力使用成熟组件。
> 3. V2 开始 Async-first。
> 4. Redis 负责任务/状态/分布式协调；Kafka 只负责需要时的事件流。
> 5. MySQL 是 OLTP / Source of Truth；Elasticsearch 是 Search；ClickHouse 是 OLAP。
> 6. 分析计算使用 Polars，但不进入高并发采集主链路。
> 7. 第三方依赖按版本渐进引入，避免 V1 过度工程化。

---

# 1. 最终依赖分类

## 1.1 Runtime

```text
Python 3.12+
```

## 1.2 Project / Package

```text
uv
```

## 1.3 Core Engine

```text
自研
```

## 1.4 Network

```text
aiohttp
```

## 1.5 Browser

```text
Playwright
```

## 1.6 HTML / DOM

```text
lxml
selectolax
Scrapling（可选）
```

## 1.7 Schema

```text
Pydantic
```

## 1.8 Data Access

```text
SQLAlchemy 2.x
asyncmy
Alembic
```

## 1.9 Queue / State

```text
redis-py
```

## 1.10 JSON

```text
orjson
```

## 1.11 Analytics

```text
Polars
```

## 1.12 Search / OLAP

```text
Elasticsearch（可选）
ClickHouse（按需）
```

## 1.13 API

```text
FastAPI
Uvicorn
```

## 1.14 Observability

```text
structlog
prometheus-client
Prometheus
Grafana
```

## 1.15 Testing

```text
pytest
pytest-asyncio
pytest-mock（可选）
```

## 1.16 Quality

```text
Ruff
mypy
```

## 1.17 Deployment

```text
Docker
Docker Compose
GitHub Actions
```

## 1.18 Event / Object Storage

```text
Kafka（按需）
S3 / MinIO（按需）
```

---

# 2. 每个技术的职责

| 技术 | 类型 | 引入 | 主要职责 |
|---|---|---|---|
| Python | Runtime | V1 | 主开发语言 |
| uv | Tool | V1 | 环境、依赖、锁定、构建 |
| asyncio | Stdlib | V2 | Async Runtime |
| aiohttp | Library | V2 | 高并发 HTTP |
| Playwright | Library | V3 | 浏览器 / JS |
| lxml | Library | V1 | XPath / HTML / XML |
| selectolax | Library | V1 | CSS / DOM |
| Scrapling | Optional Library | V3 | Adaptive Parsing |
| Pydantic | Library | V1 | Schema / Validation |
| SQLAlchemy | Library | V1 | ORM / Repository |
| asyncmy | Library | V2 | Async MySQL Driver |
| Alembic | Library | V1 | Database Migration |
| redis | Library | V2 | Queue / State / Dedup / Lock |
| orjson | Library | V1 | JSON |
| Polars | Library | V5 | Batch Analytics |
| FastAPI | Library | V5 | Control / Analytics API |
| Uvicorn | Server | V5 | ASGI |
| structlog | Library | V2+ | Structured Logging |
| prometheus-client | Library | V5 | Python Metrics |
| pytest | Test | V1 | Testing |
| pytest-asyncio | Test | V2 | Async Testing |
| pytest-mock | Optional Test | 按需 | Mock |
| Ruff | Dev Tool | V1 | Lint / Format |
| mypy | Dev Tool | V1 | Type Check |
| Elasticsearch | Infra | V5 可选 | Search |
| ClickHouse | Infra | V5 按需 | OLAP |
| Kafka | Infra | V4/V5 按需 | Event Stream |
| S3/MinIO | Infra | V5 可选 | Object Storage |
| Docker | Infra | V5 | Container |
| Docker Compose | Infra | V2+ | Local / Single-node orchestration |
| GitHub Actions | CI | V1+ | CI/CD |

---

# 3. Python / uv

## Python

```text
Python >= 3.12
```

整个系统：

```text
Engine
Scheduler
Fetcher
Parser
Pipeline
Platform
Storage
Analysis
API
```

都使用 Python。

## uv

```text
uv
```

负责：

```text
Virtual Environment
Dependency Management
Lock
Build
Run
Python Version
```

核心：

```text
pyproject.toml
uv.lock
```

AI 不应随意使用全局：

```text
pip install
```

优先：

```bash
uv add <package>
uv remove <package>
uv lock
uv sync
```

---

# 4. Async Runtime

## asyncio

标准库。

V2+：

```text
Event Loop
Coroutine
Task
Semaphore
Queue
Lock
Timeout
Cancellation
```

Async 组件：

```text
aiohttp
redis.asyncio
SQLAlchemy Async
Playwright Async
```

---

# 5. HTTP

## aiohttp

```text
aiohttp
```

定位：

> **Crawler Engine 的主 HTTP Client。**

负责：

```text
HTTP/HTTPS
Connection Pool
Keep-Alive
Timeout
Cookie
Header
Proxy
Streaming
Concurrent IO
```

原则：

```text
长生命周期 ClientSession
+
连接池
```

禁止：

```text
每个 Request 创建 ClientSession
```

不同时把：

```text
requests
httpx
aiohttp
```

作为同等级主 HTTP Client。

---

# 6. Browser

## Playwright

```text
playwright
```

V3 引入。

定位：

> Browser Runtime。

负责：

```text
JavaScript
SPA
Dynamic Render
Browser Context
Page
Network
Screenshot
Trace
```

HTTP 与 Browser 并发独立：

```text
HTTP concurrency
≠
Browser concurrency
```

Browser 必须通过 Pool / Lifecycle 管理，禁止一请求一浏览器。

---

# 7. HTML / DOM

## lxml

```text
lxml
```

用途：

```text
XPath
XML
HTML
Complex DOM
```

## selectolax

```text
selectolax
```

用途：

```text
CSS Selector
DOM Traversal
High-throughput HTML
```

推荐：

```text
XPath / XML / Complex DOM
→ lxml

CSS / High-throughput HTML
→ selectolax
```

## Scrapling

```text
scrapling
```

V3 可选。

定位：

```text
Adaptive Parsing
Enhanced Selector
特殊 Fetch
```

原则：

```text
Scrapling = Adapter
```

不是：

```text
Scrapling = Core
```

---

# 8. Schema / Domain Model

## Pydantic

```text
pydantic
```

统一：

```text
Request Schema
Task Schema

Platform
Shop
Product
SKU
Price
Inventory
Review

Analysis Result
API Response
```

平台数据：

```text
Raw
 ↓
Normalize
 ↓
Pydantic
 ↓
Validate
```

---

# 9. Database

## MySQL

```text
MySQL 8+
```

定位：

> Source of Truth / OLTP。

核心表：

```text
platform
shop
brand
category

product
product_sku
product_image

price_history
inventory_snapshot
review

crawl_task
crawl_request
crawl_result
crawl_error
```

---

## SQLAlchemy 2.x

```text
sqlalchemy
```

负责：

```text
ORM
AsyncSession
Repository
Transaction
Connection Pool
```

架构：

```text
Pipeline
 ↓
Repository
 ↓
SQLAlchemy Async
 ↓
asyncmy
 ↓
MySQL
```

Spider 禁止直接访问数据库。

---

## asyncmy

```text
asyncmy
```

V2 起使用。

作用：

```text
Async MySQL Driver
```

禁止同步 DB API 阻塞 Event Loop。

---

## Alembic

```text
alembic
```

负责：

```text
Schema Migration
Revision
Upgrade
Downgrade
```

---

# 10. Redis

## redis-py

```text
redis
```

V2 起使用：

```python
from redis import asyncio as redis
```

职责：

```text
Request Queue
Task Queue
Task State
Dedup
Distributed Lock
Rate Limit State
Cache
Worker Coordination
```

职责边界：

```text
Redis
→ Queue / State / Coordination

MySQL
→ Business Data
```

---

# 11. JSON

## orjson

```text
orjson
```

负责：

```text
JSON Encode
JSON Decode
Redis Payload
API Payload
Kafka Message
```

适合高吞吐场景。

---

# 12. Data Analytics

## Polars

```text
polars
```

V5 推荐。

用途：

```text
Batch Analytics
Aggregation
Time Series
Report
Ranking
Comparison
```

典型：

```text
MySQL / ClickHouse
 ↓
Query
 ↓
Polars
 ↓
Metrics / Report
```

不要：

```text
Crawler
 ↓
Polars
```

直接进入在线采集主链路。

---

# 13. Analysis Domain

不是一个第三方库，而是项目自身模块：

```text
analysis/
├── metrics/
├── trends/
├── comparison/
├── ranking/
└── reports/
```

## Product Metrics

```text
Product Count
SKU Count
Price
Review Count
```

## Price Metrics

```text
Min
Max
Average
Change
Volatility
Discount
```

## Inventory Metrics

```text
Current Stock
Stock Change
Out-of-stock
Restock
```

## Platform Metrics

```text
Price Difference
Product Coverage
Brand Coverage
Inventory Difference
```

## Shop / Brand / Category

```text
Count
Average Price
Price Distribution
Inventory
Review
Coverage
```

---

# 14. Elasticsearch

```text
elasticsearch
```

V5 可选。

定位：

```text
Search
```

负责：

```text
全文检索
模糊搜索
过滤
聚合
搜索排序
```

原则：

```text
MySQL = Source of Truth
Elasticsearch = Search
```

---

# 15. ClickHouse

```text
ClickHouse
```

V5 按数据规模启用。

适合：

```text
大量 Price Snapshot
大量 Inventory Snapshot
Event Analytics
Time Series
OLAP
```

职责：

```text
ClickHouse = OLAP
```

最终：

```text
MySQL
→ OLTP

Elasticsearch
→ Search

ClickHouse
→ OLAP
```

不是三套主数据库同时承担相同职责。

---

# 16. Kafka

```text
Apache Kafka
```

V4/V5 按需。

用途：

```text
ProductDiscovered
ProductUpdated
PriceChanged
InventoryChanged
ReviewDiscovered
```

消费者：

```text
Storage
Search
Analytics
Alert
```

职责：

```text
Redis → Task Queue
Kafka → Event Stream
```

没有事件流需求时不引入。

---

# 17. Object Storage

## S3 / MinIO

V5 可选。

用于：

```text
Raw HTML
Raw JSON
Images
Screenshots
Playwright Trace
Downloaded Files
```

Python 客户端：

```text
boto3
```

---

# 18. API

## FastAPI

```text
fastapi
```

V5。

负责：

```text
Task API
Platform API
Worker API
Analytics API
Health API
Metrics API
```

不直接运行长时间 Crawl Job。

---

## Uvicorn

```text
uvicorn
```

作为 FastAPI ASGI Server。

---

# 19. Logging

## structlog

```text
structlog
```

建议字段：

```text
timestamp
level
event
task_id
request_id
worker_id
platform
spider
url
status_code
duration
retry_count
error_type
```

---

# 20. Metrics

## prometheus-client

Python Metrics：

```text
crawler_requests_total
crawler_requests_success_total
crawler_requests_failed_total
crawler_request_duration_seconds

crawler_items_total
crawler_parse_failed_total
crawler_retry_total

crawler_queue_size
crawler_worker_count
crawler_worker_load
```

## Prometheus

```text
Metric Storage
Query
Alert
```

## Grafana

```text
Dashboard
Visualization
```

---

# 21. Testing

## pytest

V1 起。

测试：

```text
Engine
Request
Response
Scheduler
Downloader
Fetcher
Parser
Pipeline
Repository
Platform Adapter
Analysis
```

## pytest-asyncio

V2 起。

测试：

```text
asyncio
aiohttp
redis.asyncio
SQLAlchemy Async
```

## pytest-mock

按需。

用于：

```text
HTTP
Redis
Repository
Fetcher
Platform Adapter
```

---

# 22. Code Quality

## Ruff

负责：

```text
Lint
Format
Import
Code Style
Unused Code
```

## mypy

负责：

```text
Static Type Check
```

重点保护：

```text
Request
Response
Product
Task
Pipeline
Repository
Platform Adapter
Analysis
```

---

# 23. Docker

## Docker

V5 为正式生产组件。

服务：

```text
api
scheduler
worker
redis
mysql
prometheus
grafana
```

按需：

```text
elasticsearch
clickhouse
kafka
minio
```

## Docker Compose

适合：

```text
Local Development
Integration Test
Single-node Deployment
```

---

# 24. GitHub Actions

CI：

```text
Ruff
 ↓
mypy
 ↓
pytest
 ↓
Integration Test
 ↓
Docker Build
```

Release：

```text
Tag
 ↓
Build Image
 ↓
Push Registry
 ↓
Deploy
```

---

# 25. 五版本依赖引入矩阵

| 依赖/组件 | V1 | V2 | V3 | V4 | V5 |
|---|---:|---:|---:|---:|---:|
| Python | ✅ | ✅ | ✅ | ✅ | ✅ |
| uv | ✅ | ✅ | ✅ | ✅ | ✅ |
| asyncio | ❌ | ✅ | ✅ | ✅ | ✅ |
| aiohttp | 简单/临时 | ✅ | ✅ | ✅ | ✅ |
| lxml | ✅ | ✅ | ✅ | ✅ | ✅ |
| selectolax | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pydantic | ✅ | ✅ | ✅ | ✅ | ✅ |
| SQLAlchemy | ✅ | ✅ | ✅ | ✅ | ✅ |
| asyncmy | ❌ | ✅ | ✅ | ✅ | ✅ |
| Alembic | ✅ | ✅ | ✅ | ✅ | ✅ |
| Redis | ❌ | ✅ | ✅ | ✅ | ✅ |
| orjson | ✅ | ✅ | ✅ | ✅ | ✅ |
| Playwright | ❌ | ❌ | ✅ | ✅ | ✅ |
| Scrapling | ❌ | ❌ | ⭕ | ⭕ | ⭕ |
| Proxy Manager | ❌ | 基础 | ✅ | ✅ | ✅ |
| Polars | ❌ | ❌ | 基础指标可不需要 | ⭕ | ✅ |
| FastAPI | ❌ | ❌ | ❌ | ❌ | ✅ |
| Uvicorn | ❌ | ❌ | ❌ | ❌ | ✅ |
| structlog | 基础 | ✅ | ✅ | ✅ | ✅ |
| prometheus-client | ❌ | 基础 | 基础 | ✅ | ✅ |
| Prometheus | ❌ | ❌ | ❌ | ⭕ | ✅ |
| Grafana | ❌ | ❌ | ❌ | ⭕ | ✅ |
| pytest | ✅ | ✅ | ✅ | ✅ | ✅ |
| pytest-asyncio | ❌ | ✅ | ✅ | ✅ | ✅ |
| pytest-mock | ⭕ | ⭕ | ⭕ | ⭕ | ⭕ |
| Ruff | ✅ | ✅ | ✅ | ✅ | ✅ |
| mypy | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kafka | ❌ | ❌ | ❌ | ⭕ | ⭕ |
| Elasticsearch | ❌ | ❌ | ❌ | ⭕ | ✅ |
| ClickHouse | ❌ | ❌ | ❌ | ❌ | ⭕ |
| S3/MinIO | ❌ | ❌ | ❌ | ⭕ | ⭕ |
| Docker | ⭕ | ⭕ | ⭕ | ✅ | ✅ |
| Docker Compose | ⭕ | ✅ | ✅ | ✅ | ✅ |
| GitHub Actions | ✅ | ✅ | ✅ | ✅ | ✅ |

---

# 26. 推荐 pyproject.toml 分组

```toml
[project]
requires-python = ">=3.12"

dependencies = [
    "lxml",
    "selectolax",
    "pydantic",
    "sqlalchemy>=2",
    "alembic",
    "orjson",
]

[project.optional-dependencies]

async = [
    "aiohttp",
    "asyncmy",
    "redis",
]

browser = [
    "playwright",
]

scrapling = [
    "scrapling",
]

api = [
    "fastapi",
    "uvicorn",
]

analytics = [
    "polars",
]

observability = [
    "structlog",
    "prometheus-client",
]

search = [
    "elasticsearch",
]

object-storage = [
    "boto3",
]

test = [
    "pytest",
    "pytest-asyncio",
    "pytest-mock",
]

dev = [
    "ruff",
    "mypy",
]
```

Kafka / ClickHouse 建议等实际采用后再添加对应客户端，避免在没有业务需求时预装大型基础设施。

---

# 27. 依赖边界

## HTTP

```text
主 HTTP Client
→ aiohttp
```

不要：

```text
requests + httpx + aiohttp
```

全部作为主客户端。

## Crawl Framework

```text
Custom Engine
```

不是：

```text
Scrapy + Scrapling + Custom Engine
```

同时当主框架。

## Search

```text
Elasticsearch = Search
```

## OLTP

```text
MySQL = Source of Truth
```

## OLAP

```text
ClickHouse = Analytics
```

## Task Queue

```text
Redis = Task Queue
```

## Event Stream

```text
Kafka = Event Stream
```

---

# 28. 最终技术链

```text
Python 3.12+
    ↓
uv
    ↓
Custom Crawler Engine
    ↓
asyncio
    ↓
aiohttp
    │
    ├──────────────→ Playwright
    │
    └──────────────→ Scrapling Adapter（可选）
    ↓
lxml / selectolax
    ↓
Pydantic
    ↓
Pipeline
    ↓
SQLAlchemy Async
    ↓
MySQL
    │
    ├── Redis
    │     └── Queue / State / Dedup / Lock
    │
    ├── Elasticsearch
    │     └── Search
    │
    ├── Polars
    │     └── Batch Analytics
    │
    └── ClickHouse（按规模）
          └── OLAP

Control:
FastAPI + Uvicorn

Observability:
structlog + Prometheus + Grafana

Deployment:
Docker + Docker Compose + GitHub Actions

Events:
Kafka（按需）

Objects:
S3 / MinIO（按需）
```

---

# 29. AI 依赖管理规则

AI 新增依赖前必须回答：

```text
1. 这个库解决什么问题？
2. 当前 Version 是否需要？
3. 是否已有组件可以解决？
4. 会不会重复承担已有组件职责？
5. 是否增加同步阻塞？
6. 是否增加核心耦合？
7. 是否需要 ADR？
8. 是否需要加入 pyproject.toml？
9. 是否需要新增测试？
```

如果当前 Milestone 不需要：

```text
不要引入。
```

---

# 30. 最终原则

```text
少而明确的依赖
+
清晰的职责边界
+
可替换的 Adapter
+
版本渐进引入
+
AI 可验证交付
```

最终目标不是：

```text
使用最多的技术
```

而是：

```text
用最少且职责明确的技术
构建可扩展的电商采集与分析系统。
```
