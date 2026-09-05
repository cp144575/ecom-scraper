# ecom-scraper 五版本开发与 AI 交付路线（最终优化版）

> 本文档是 `ecom-scraper` 的产品、架构和 AI 开发执行基线。
>
> 项目定位：**自研 Async Crawler Engine + 国内/海外电商多平台采集 + 分布式 Worker + 数据分析 + 生产管理平台**。
>
> 本文重点解决的不只是“做什么”，还规定 **AI 如何在每个版本中计划、执行、验证、评审、收尾和交付**。

---

# 1. 产品目标

最终系统不是一个单平台 Spider，也不是一个 Scrapy 项目，而是：

```text
                    ecom-scraper
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      Crawling          Data          Analytics
        │                │                │
   Custom Engine       MySQL          Metrics
   Async Fetch        Redis          Trends
   Distributed        Search         Ranking
   Multi-platform     Object         Comparison
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                  Control Platform
                         │
               FastAPI + Dashboard
```

最终覆盖：

```text
采集
→ 调度
→ 高并发
→ 多平台
→ 数据标准化
→ 数据质量
→ 数据存储
→ 数据分析
→ 监控
→ 任务管理
→ 分布式 Worker
```

---

# 2. 五版本总览

| 版本 | 名称 | 核心目标 | 主要能力 |
|---|---|---|---|
| V1 | Minimal MVP | 建立自研同步爬虫最小闭环 | Request、Response、Engine、Scheduler、Downloader、Parser、Pipeline、MySQL |
| V2 | Async High Concurrency | 单机 Async-first 高并发 | asyncio、aiohttp、Concurrency、Retry、Rate Limit、Dedup、Backpressure、Redis |
| V3 | E-commerce Domain | 建立真正的国内+海外电商采集能力 | Product、SKU、Shop、Price、Inventory、Platform Adapter、Playwright、Proxy、基础分析 |
| V4 | Distributed Crawling | 多 Worker 稳定分布式采集 | Distributed Queue、Task Leasing、Heartbeat、Recovery、分布式去重/限流、事件流 |
| V5 | Production & Analytics Platform | 生产级管理、分析和运维平台 | FastAPI、Vue 3、Observability、Docker、CI/CD、Search、OLAP、Analytics |

---

# 3. 五版本演进原则

## 3.1 不推翻式演进

```text
V1
 ↓
V2
 ↓
V3
 ↓
V4
 ↓
V5
```

后续版本应尽量通过 Adapter、Interface、Implementation 扩展前一版本。

禁止：

```text
V2
→ 完全重写 V1

V3
→ 更换 Engine 公共接口

V4
→ 让所有平台重新实现基础设施
```

## 3.2 Architecture-ready，Deployment-later

从 V1 就保留：

```text
模块边界
接口抽象
可替换组件
任务模型
Worker 概念
状态模型
```

但不提前部署：

```text
Kafka
Kubernetes
大规模 ES
ClickHouse Cluster
```

## 3.3 Async-first 的边界

V1：

```text
允许同步 MVP
```

V2：

```text
网络 IO
Redis IO
DB IO
Browser control
```

全部进入异步体系。

CPU 密集型解析不强制异步。

## 3.4 数据采集与数据分析解耦

```text
Crawler
 ↓
Canonical Data
 ↓
Storage
 ↓
Analysis
```

不要让：

```text
Spider
```

直接执行复杂商业分析。

---

# 4. V1 —— Minimal MVP

## 4.1 目标

只证明：

> 自研 Engine 能够执行一次完整采集任务，并把结构化数据持久化到 MySQL。

## 4.2 技术

```text
Python 3.12+
uv
轻量 HTTP Client
lxml
selectolax
Pydantic
SQLAlchemy
MySQL
pytest
Ruff
mypy
```

V1 不引入完整异步体系。

## 4.3 核心模块

```text
Engine
├── Request
├── Response
├── Spider
├── Scheduler
├── Downloader
├── Parser
├── Item
└── Pipeline
```

## 4.4 请求流

```text
Spider
 ↓
Request
 ↓
Engine
 ↓
Scheduler
 ↓
Downloader
 ↓
HTTP
 ↓
Response
 ↓
Parser
 ↓
Item
 ↓
Pipeline
 ↓
Repository
 ↓
MySQL
```

## 4.5 V1 数据模型

```python
class Product(BaseModel):
    platform: str
    platform_product_id: str
    title: str
    price: Decimal | None = None
    currency: str = "CNY"
    url: str
```

## 4.6 V1 目录

```text
src/ecom_scraper/
├── engine/
├── request/
├── spider/
├── parser/
├── pipeline/
├── models/
└── storage/
```

## 4.7 V1 Milestones

```text
V1.1 项目初始化
V1.2 Request / Response
V1.3 Scheduler
V1.4 Downloader
V1.5 Spider
V1.6 Parser
V1.7 Pipeline
V1.8 MySQL Repository
V1.9 Test
V1.10 Quality / Refactor / Release
```

## 4.8 V1 验收

必须实现：

```text
URL
 ↓
Engine
 ↓
Product
 ↓
MySQL
```

必须：

- 单元测试通过
- 集成测试通过
- Ruff 通过
- mypy 通过
- README 能复现实例
- 一个小型端到端采集成功

---

# 5. V2 —— Async High Concurrency

## 5.1 目标

把 V1 演进为：

> **单机 Async-first 高并发采集 Engine。**

## 5.2 技术

```text
asyncio
aiohttp
redis
SQLAlchemy Async
asyncmy
pytest-asyncio
```

## 5.3 新增核心能力

```text
Async Engine
Concurrency Controller
Timeout
Retry
Rate Limiter
Fingerprint / Dedup
Backpressure
Redis Queue
Async DB
```

## 5.4 aiohttp

统一 HTTP：

```text
aiohttp.ClientSession
```

负责：

```text
Connection Pool
Keep-Alive
Timeout
Proxy
Cookie
Header
Streaming
Concurrent IO
```

规则：

> ClientSession 必须长生命周期复用，禁止每个 Request 建立新的 Session。

## 5.5 Concurrency Controller

至少：

```text
Global Limit
Domain Limit
Platform Limit
Fetcher Limit
```

示例：

```text
Global = 500
JD = 100
Taobao = 100
Other = 300
```

实际值必须通过负载测试决定。

## 5.6 Retry

```text
RetryPolicy
├── max_attempts
├── retryable_statuses
├── exponential_backoff
├── jitter
└── timeout_policy
```

禁止：

```text
无限重试
```

## 5.7 Rate Limit

初版：

```text
Token Bucket
```

必须区分：

```text
Concurrency
Rate
```

## 5.8 Backpressure

必须避免：

```text
无限 asyncio.Task
无限内存 Queue
```

## 5.9 Redis

V2 开始承担：

```text
Queue
Task State
Dedup
Lock
Cache
Rate Limit State
```

## 5.10 V2 Milestones

```text
V2.1 Async Engine
V2.2 aiohttp Fetcher
V2.3 Concurrency Controller
V2.4 Timeout / Retry
V2.5 Rate Limiter
V2.6 Fingerprint / Dedup
V2.7 Redis Queue
V2.8 Backpressure
V2.9 Async DB
V2.10 Load Test
```

## 5.11 V2 验收

测试基线：

```text
10,000 URLs
```

要求：

```text
高并发
无 Event Loop 阻塞
无无限 Task
Retry 有上限
Dedup 有效
Rate Limit 有效
Backpressure 有效
数据库异步
```

---

# 6. V3 —— E-commerce Domain

## 6.1 目标

从“爬虫引擎”升级为：

> **国内 + 海外电商数据采集系统。**

## 6.2 电商领域模型

```text
Platform
Shop
Product
ProductSKU
ProductImage
Category
Brand
PriceSnapshot
InventorySnapshot
Review
```

## 6.3 Canonical Model

必须：

```text
Platform Raw Data
 ↓
Platform Parser
 ↓
Platform Item
 ↓
Normalizer
 ↓
Canonical Model
 ↓
Validator
 ↓
Dedup
 ↓
Storage
```

## 6.4 Platform Adapter

```python
class PlatformAdapter(ABC):
    async def fetch_product(self, request: Request) -> Response:
        ...

    def parse_product(self, response: Response) -> Product:
        ...

    def parse_sku(self, response: Response) -> list[ProductSKU]:
        ...

    def parse_shop(self, response: Response) -> Shop:
        ...
```

平台不能直接实现：

```text
Scheduler
Redis Queue
DB Session
Retry
Proxy Pool
```

## 6.5 第一批平台

```text
JD
Taobao
Amazon
```

先验证：

```text
China Platform
+
Global Platform
```

是否都能进入统一 Canonical Model。

## 6.6 Playwright

负责：

```text
JS
SPA
Dynamic Render
Browser Context
Page
Network
```

必须：

```text
HTTP concurrency ≠ Browser concurrency
```

建议初始设计：

```text
HTTP  → 高并发
Browser → 低并发
```

## 6.7 Proxy Manager

```text
proxy/
├── base.py
├── pool.py
├── selector.py
├── validator.py
└── health.py
```

平台只声明：

```python
request.meta["proxy_policy"] = "residential"
```

## 6.8 Scrapling

可选：

```text
Scrapling Adapter
```

主要用于：

```text
Adaptive Parsing
Enhanced Selector
特殊 Fetch
```

Scrapling 不成为系统核心。

## 6.9 V3 基础分析

V3 开始建立：

```text
Price Metrics
Inventory Metrics
Product Metrics
Shop Metrics
Platform Comparison
```

例如：

```text
最低价
最高价
平均价
价格变化
库存变化
平台价格差
商品数量
店铺商品数
```

## 6.10 V3 Milestones

```text
V3.1 Ecommerce Models
V3.2 Canonical Model
V3.3 Platform Adapter
V3.4 JD
V3.5 Taobao
V3.6 Amazon
V3.7 Playwright
V3.8 Browser Pool
V3.9 Proxy Manager
V3.10 Scrapling Adapter
V3.11 Price / Inventory Analysis
V3.12 Regression Test
```

## 6.11 V3 验收

三个平台至少能够输出：

```text
Product
SKU
Shop
Price
```

同时：

```text
HTTP / Browser 解耦
Platform / Core 解耦
Raw / Canonical 解耦
Price History 可持续记录
```

---

# 7. V4 —— Distributed Crawling

## 7.1 目标

从：

```text
Single Machine
```

升级：

```text
Multi Worker Cluster
```

## 7.2 新能力

```text
Distributed Scheduler
Distributed Queue
Worker
Heartbeat
Task Leasing
Distributed Dedup
Distributed Rate Limit
Recovery
Task State
```

## 7.3 架构

```text
Scheduler
    ↓
Redis
    ↓
┌────────┬────────┬────────┐
↓        ↓        ↓
W1       W2       WN
│        │        │
Async   Async    Async
Engine  Engine   Engine
│        │        │
└────────┴────────┘
         ↓
      Pipeline
         ↓
       MySQL
```

## 7.4 Task Leasing

```text
Queue
 ↓
Worker A lease
 ↓
Heartbeat
 ↓
ACK
```

异常：

```text
Heartbeat timeout
 ↓
Lease expired
 ↓
Task returned to queue
```

## 7.5 Worker Heartbeat

```text
worker:{id}:heartbeat
worker:{id}:status
worker:{id}:load
worker:{id}:last_seen
```

## 7.6 Distributed Rate Limit

至少：

```text
Global
Platform
Domain
Proxy
```

## 7.7 Kafka

不是默认依赖。

只有出现：

```text
ProductDiscovered
ProductUpdated
PriceChanged
InventoryChanged
ReviewDiscovered
```

等事件，并需要：

```text
多个消费者
长期消息流
事件解耦
```

时才加入 Kafka。

职责：

```text
Redis → Task Queue
Kafka → Event Stream
```

## 7.8 V4 数据分析

开始支持：

```text
PriceChanged
InventoryChanged
ProductUpdated
```

事件驱动分析。

## 7.9 V4 Milestones

```text
V4.1 Worker
V4.2 Distributed Queue
V4.3 Task Leasing
V4.4 Heartbeat
V4.5 Distributed Dedup
V4.6 Distributed Rate Limit
V4.7 Recovery
V4.8 Kafka Event Stream（按需）
V4.9 Distributed Analytics Consumer
V4.10 Multi-worker Load Test
```

## 7.10 V4 验收

测试：

```text
1 Scheduler
3~10 Workers
100k+ Requests
```

必须：

- Worker 故障自动恢复
- Task 不因单 Worker 崩溃丢失
- 分布式去重
- 分布式限流
- Heartbeat
- Task Lease
- Queue 状态可恢复

---

# 8. V5 —— Production & Analytics Platform

## 8.1 目标

形成：

> **可管理、可观测、可分析、可部署的生产级电商数据平台。**

## 8.2 Control Plane

```text
Vue 3
 ↓
FastAPI
 ↓
Task / Platform / Worker / Analytics API
```

## 8.3 API

```text
POST /tasks
GET  /tasks
GET  /tasks/{id}
POST /tasks/{id}/start
POST /tasks/{id}/stop
POST /tasks/{id}/retry

GET /platforms
GET /workers
GET /workers/{id}

GET /analytics/products
GET /analytics/prices
GET /analytics/inventory
GET /analytics/platforms
GET /analytics/shops

GET /health
GET /metrics
```

## 8.4 Analytics Domain

```text
analysis/
├── metrics/
│   ├── product.py
│   ├── price.py
│   ├── inventory.py
│   ├── shop.py
│   ├── brand.py
│   └── category.py
├── trends/
├── comparison/
├── ranking/
└── reports/
```

### 分析内容

```text
Product
Price
Inventory
Shop
Brand
Category
Platform
```

### 典型指标

```text
Min Price
Max Price
Average Price
Price Change
Price Volatility
Inventory Trend
Product Count
SKU Count
Platform Price Difference
Brand Ranking
Category Ranking
```

## 8.5 Polars

V5 引入，用于：

```text
Batch Analytics
Aggregation
Time Series
Report
```

不要进入：

```text
Crawler → Parser
```

主链路。

## 8.6 Storage 三层职责

```text
MySQL
→ OLTP / Source of Truth

Elasticsearch
→ Search

ClickHouse
→ OLAP
```

ClickHouse 只有在大量时间序列/聚合真正出现后才部署。

## 8.7 Object Storage

S3 / MinIO：

```text
Raw HTML
Raw JSON
Product Images
Screenshot
Trace
Downloaded Files
```

## 8.8 Observability

```text
structlog
+
prometheus-client
+
Prometheus
+
Grafana
```

核心：

```text
Request QPS
Success Rate
Error Rate
Timeout Rate
Retry Rate
Parse Success
Queue Size
Worker Count
Worker Load
Proxy Health
Task Duration
Platform Health
```

## 8.9 Docker

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

## 8.10 GitHub Actions

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
Release
 ↓
Image Build
 ↓
Registry
 ↓
Deploy
```

## 8.11 V5 Milestones

```text
V5.1 FastAPI
V5.2 Task API
V5.3 Worker API
V5.4 Analytics API
V5.5 Vue Dashboard
V5.6 Metrics
V5.7 Grafana
V5.8 Docker Compose
V5.9 GitHub Actions
V5.10 Elasticsearch
V5.11 Polars Analysis
V5.12 ClickHouse（按需）
V5.13 Production Hardening
V5.14 Documentation
```

---

# 9. AI 开发工作流

本项目采用固定的 AI 工程流水线：

```text
Goal
 ↓
Brainstorming
 ↓
Writing Plans
 ↓
Architecture / ADR
 ↓
01-feature
 ↓
TDD
 ↓
Agent Coding
 ↓
Verification
 ↓
Quality Review
 ↓
Code Review
 ↓
Finish Branch
 ↓
Commit / PR
```

对应 Skill：

```text
goal
brainstorming
writing-plans
executing-plans
architecture-decision-records
01-feature
test-driven-development
04-agent-coding
verification-before-completion
02-quality
requesting-code-review
receiving-code-review
finishing-a-development-branch
```

---

# 10. AI 每次开发的强制协议

任何新功能必须先回答：

```text
1. 当前 Version？
2. 当前 Milestone？
3. Goal 是什么？
4. 成功标准是什么？
5. 影响哪些模块？
6. 哪些模块明确不能修改？
7. 是否需要 ADR？
8. 是否可以并行？
9. 测试策略是什么？
10. 如何验证完成？
```

然后：

```text
Plan
 ↓
Implement
 ↓
Test
 ↓
Verify
 ↓
Review
 ↓
Commit
```

---

# 11. Goal：目标锚定

每个任务必须写清：

```text
Goal:
实现什么

Constraints:
不能改什么

Acceptance:
什么算完成

Out of Scope:
这次明确不做什么
```

示例：

```text
Goal:
实现 V2.3 Concurrency Controller。

Acceptance:
- 支持全局并发限制
- 支持平台级并发限制
- 不阻塞 Event Loop
- 单元测试通过
- 并发测试通过

Out of Scope:
- 不实现 Redis 分布式限流
- 不实现 Browser Pool
```

---

# 12. Brainstorming：先思考再编码

先分析：

```text
现有实现
依赖模块
风险
替代方案
接口
测试
```

不要一上来写代码。

输出至少：

```text
Current State
Problem
Options
Recommendation
Risks
```

---

# 13. Writing Plans：施工计划

计划必须细化到：

```text
Step
File
Change
Test
Verification
```

例如：

```text
1. 新建 concurrency/controller.py
2. 定义 ConcurrencyPolicy
3. 增加 acquire/release
4. 增加测试
5. 修改 Downloader
6. 运行 pytest
7. 运行 Ruff
8. 运行 mypy
```

---

# 14. Executing Plans：计划执行器

执行时：

```text
只执行已批准计划
```

如果发现新的架构问题：

```text
停止当前变更
 ↓
重新评估
 ↓
更新计划
```

不要让 AI 自己不断扩大任务范围。

---

# 15. Subagent-driven Development

只有任务可以真正拆开时才并行。

适合：

```text
Product Model
Shop Model
Price Model
```

不适合：

```text
Request Interface
Engine
Scheduler
```

这种强耦合核心任务。

推荐：

```text
Main Agent
   │
   ├── Agent A
   ├── Agent B
   └── Agent C
        ↓
Integration Agent
        ↓
Test
        ↓
Review
```

---

# 16. Git Worktree

并行开发使用：

```text
git worktree
```

例如：

```text
main
├── worktree/product
├── worktree/shop
└── worktree/price
```

每个 Agent：

```text
独立目录
独立分支
独立测试
```

完成后统一合并。

---

# 17. Architecture Decision Records

所有重要技术决策记录：

```text
docs/adr/
├── ADR-001-custom-engine.md
├── ADR-002-aiohttp.md
├── ADR-003-redis.md
├── ADR-004-playwright.md
├── ADR-005-platform-adapter.md
├── ADR-006-mysql-source-of-truth.md
└── ADR-007-analytics-layer.md
```

触发 ADR 的典型场景：

```text
新增核心依赖
替换基础设施
改变公共接口
改变数据模型
改变任务模型
改变存储职责
改变并发模型
```

---

# 18. Quality Gate

每个 Milestone 完成前：

```text
pytest
 ↓
Ruff
 ↓
mypy
 ↓
Integration Test
 ↓
Architecture Review
 ↓
Code Review
```

AI 必须提供：

```text
Changed Files
Behavior Changes
Tests Run
Test Result
Known Limitations
```

---

# 19. Finishing a Development Branch

完成后：

```text
Working Tree Clean
 ↓
Tests Green
 ↓
Quality Green
 ↓
Commit
 ↓
PR
 ↓
Review
 ↓
Merge
 ↓
Delete Worktree
```

禁止：

```text
测试未通过就 Merge
```

---

# 20. 五版本依赖边界

```text
V1
只做：
同步 Engine + MySQL

V2
增加：
asyncio + aiohttp + Redis + 高并发控制

V3
增加：
Playwright + Proxy + Platform Adapter + Scrapling + 基础业务分析

V4
增加：
Multi Worker + Distributed State + Kafka（按需）

V5
增加：
FastAPI + Vue + Observability + Search + Analytics + OLAP + Docker
```

严格禁止提前：

```text
V1 → Kafka
V1 → Playwright
V1 → Elasticsearch
V1 → ClickHouse

V2 → Multi-worker Cluster

除非当前 Milestone 明确要求。
```

---

# 21. 最终验收模型

每个版本都有四个结果：

```text
Code
+
Tests
+
Docs
+
Evidence
```

不是：

```text
Code
```

才算完成。

---

# 22. 最终产品能力

完成 V5 后：

```text
                           ecom-scraper
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
      Crawling                 Data                 Analytics
         │                      │                      │
      Engine                  MySQL                Metrics
      Scheduler               Redis                Trends
      Fetcher                 Search               Ranking
      Worker                  Object               Compare
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                         Control Plane
                                │
                        FastAPI + Vue
                                │
                    Prometheus + Grafana
```

最终它应该能够：

```text
✓ 国内电商采集
✓ 海外电商采集
✓ HTTP 高并发
✓ Browser 动态采集
✓ 多平台统一模型
✓ Proxy 管理
✓ 分布式 Worker
✓ 任务恢复
✓ 数据质量控制
✓ 价格分析
✓ 库存分析
✓ 商品分析
✓ 平台比较
✓ 搜索
✓ 监控
✓ Web 管理
✓ Docker 部署
✓ CI/CD
```

---

# 23. 最重要的开发原则

```text
先 Goal
再 Brainstorm
再 Plan
再 Implement
再 Test
再 Verify
再 Review
再 Commit
```

而不是：

```text
一句需求
 ↓
AI 生成大量代码
 ↓
不知道为什么能跑
 ↓
不断修 bug
```

`ecom-scraper` 的 AI 开发目标不是让 AI “写得最多”，而是让 AI：

```text
理解准确
修改最小
边界清晰
验证充分
交付可复现
```

这样五个版本才能稳定向前演进。
