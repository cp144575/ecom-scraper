---
name: project-guidance
description: Determines which ecom-scraper project standards and architecture documents an AI agent must read for a given task. Use before planning or modifying code to load only the relevant standards.
---

# ecom-scraper AI 文档调用与 Skill 路由规范

## 1. Purpose

本 Skill 不负责具体编码规范。

它负责：

> 根据当前任务类型、修改范围、项目版本和代码所在模块，自动决定必须读取哪些项目 MD 规范。

目标：

```text
减少无关上下文
提高 AI 理解准确度
避免遗漏关键规范
避免重复读取全部文档
降低错误修改概率
保持架构一致
```

---

# 2. Available Standards

本项目当前有 15 个核心规范文件：

```text
01-python-core-style.md
02-async-concurrency.md
03-error-handling.md
04-data-model-and-database.md
05-api-design.md
06-testing.md
07-logging-observability.md
08-performance.md
09-security-secrets.md
10-project-structure.md
11-crawler-platform-coding.md
12-data-analysis.md
13-code-review-and-delivery.md

ecom-scraper-5-versions-optimized-v2.md
ecom-scraper-dependencies-optimized-v2.md
```

---

# 3. Document Roles

## 3.1 Project Roadmap

```text
ecom-scraper-5-versions-optimized-v2.md
```

负责：

```text
当前 Version
Milestone
版本边界
技术引入顺序
架构演进
AI 开发流程
验收标准
```

它回答：

> “当前项目应该做什么？”

---

## 3.2 Dependency Baseline

```text
ecom-scraper-dependencies-optimized-v2.md
```

负责：

```text
技术栈
依赖
依赖职责
版本引入
依赖边界
技术选型
存储职责
```

它回答：

> “项目应该用什么技术？”

---

## 3.3 Python Coding

```text
01-python-core-style.md
```

负责：

```text
Python 语法
命名
类型
函数
Class
Docstring
Import
代码风格
```

它回答：

> “Python 代码应该怎么写？”

---

## 3.4 Async

```text
02-async-concurrency.md
```

负责：

```text
asyncio
aiohttp
Task
Semaphore
Concurrency
Rate
Backpressure
Cancellation
Timeout
Browser Concurrency
```

它回答：

> “异步和并发代码应该怎么写？”

---

## 3.5 Error

```text
03-error-handling.md
```

负责：

```text
Exception
Retry
Backoff
Failure Classification
Error Context
```

它回答：

> “错误应该怎么处理？”

---

## 3.6 Data / DB

```text
04-data-model-and-database.md
```

负责：

```text
Pydantic
Domain Model
ORM
Repository
MySQL
SQLAlchemy
asyncmy
Alembic
Money
Time
ID
```

它回答：

> “数据应该怎么建模和持久化？”

---

## 3.7 API

```text
05-api-design.md
```

负责：

```text
FastAPI
Router
Service
Schema
Pagination
Error Response
Idempotency
```

它回答：

> “API 应该怎么设计？”

---

## 3.8 Testing

```text
06-testing.md
```

负责：

```text
pytest
pytest-asyncio
Unit
Integration
E2E
Mock
Regression
Verification
```

它回答：

> “如何证明代码正确？”

---

## 3.9 Observability

```text
07-logging-observability.md
```

负责：

```text
structlog
Metrics
Prometheus
Grafana
Traceability
Sensitive Logs
```

它回答：

> “系统运行状态如何被观察？”

---

## 3.10 Performance

```text
08-performance.md
```

负责：

```text
Throughput
Latency
Memory
Connections
Browser Cost
Queue
Load Test
```

它回答：

> “如何优化，并如何证明真的优化了？”

---

## 3.11 Security

```text
09-security-secrets.md
```

负责：

```text
Secrets
Credentials
Cookie
Token
SSRF
Input Validation
Least Privilege
```

它回答：

> “代码是否安全？”

---

## 3.12 Project Structure

```text
10-project-structure.md
```

负责：

```text
Module Boundary
Dependency Direction
Platform Isolation
Fetcher
Repository
No God Object
Circular Dependency
```

它回答：

> “代码应该放在哪里，以及模块之间如何依赖？”

---

## 3.13 Crawler / Platform

```text
11-crawler-platform-coding.md
```

负责：

```text
Platform Adapter
Spider
Fetcher
Parser
Canonical Model
Product
SKU
Shop
Price
Inventory
Platform Regression
```

它回答：

> “电商爬虫代码应该怎么写？”

---

## 3.14 Analytics

```text
12-data-analysis.md
```

负责：

```text
Metrics
Trend
Ranking
Comparison
Polars
OLTP / Search / OLAP
```

它回答：

> “采集后的电商数据如何分析？”

---

## 3.15 Review / Delivery

```text
13-code-review-and-delivery.md
```

负责：

```text
Code Review
Quality Gate
Git Diff
Commit
Definition of Done
AI Completion
```

它回答：

> “什么时候算真正交付完成？”

---

# 4. Always Load

任何代码修改任务开始前，必须读取：

```text
10-project-structure.md
01-python-core-style.md
```

原因：

```text
10 → 决定“放哪里”
01 → 决定“怎么写”
```

任何架构或跨模块任务额外必须读取：

```text
ecom-scraper-5-versions-optimized-v2.md
ecom-scraper-dependencies-optimized-v2.md
```

---

# 5. Task Routing

AI 必须根据任务内容自动选择额外文件。

## 5.1 新增 Python 文件 / 修改普通 Python

读取：

```text
01-python-core-style.md
10-project-structure.md
06-testing.md
```

如果有异常：

```text
03-error-handling.md
```

如果有日志：

```text
07-logging-observability.md
```

---

# 6. API Task

当任务包含以下关键词：

```text
API
FastAPI
Router
Endpoint
HTTP API
REST
Request Schema
Response Schema
Controller
```

必须读取：

```text
05-api-design.md
01-python-core-style.md
10-project-structure.md
04-data-model-and-database.md
06-testing.md
13-code-review-and-delivery.md
```

如果涉及：

```text
Auth
Token
Credential
Cookie
Secret
```

增加：

```text
09-security-secrets.md
```

---

# 7. Database Task

当任务涉及：

```text
MySQL
SQLAlchemy
ORM
Repository
Database
Migration
Alembic
Schema
Index
Transaction
```

必须读取：

```text
04-data-model-and-database.md
01-python-core-style.md
10-project-structure.md
06-testing.md
13-code-review-and-delivery.md
```

如果任务涉及异步数据库：

```text
02-async-concurrency.md
```

如果涉及数据模型迁移：

```text
ecom-scraper-dependencies-optimized-v2.md
```

---

# 8. Async / aiohttp Task

当任务涉及：

```text
asyncio
aiohttp
async
await
concurrency
parallel
task
semaphore
rate limit
backpressure
timeout
cancellation
connection pool
```

必须读取：

```text
02-async-concurrency.md
01-python-core-style.md
03-error-handling.md
06-testing.md
08-performance.md
```

如果涉及 Redis：

```text
04-data-model-and-database.md
```

并检查：

```text
redis.asyncio
```

---

# 9. Crawler Engine Task

当任务涉及：

```text
Engine
Crawler
Scheduler
Downloader
Request
Response
Spider
Queue
Retry
Middleware
```

必须读取：

```text
ecom-scraper-5-versions-optimized-v2.md
10-project-structure.md
01-python-core-style.md
11-crawler-platform-coding.md
03-error-handling.md
06-testing.md
```

如果是 V2+：

```text
02-async-concurrency.md
```

如果涉及性能：

```text
08-performance.md
```

---

# 10. Platform Adapter Task

当任务涉及：

```text
JD
Taobao
Amazon
PDD
1688
eBay
Walmart
Shopee
Lazada
Platform Adapter
Product Parser
Shop Parser
SKU Parser
```

必须读取：

```text
11-crawler-platform-coding.md
10-project-structure.md
01-python-core-style.md
06-testing.md
03-error-handling.md
```

如果涉及：

```text
aiohttp
Playwright
Scrapling
```

分别增加：

```text
02-async-concurrency.md
08-performance.md
ecom-scraper-dependencies-optimized-v2.md
```

---

# 11. Playwright / Browser Task

关键词：

```text
Playwright
Browser
Context
Page
JS
SPA
Dynamic Render
Browser Pool
```

必须读取：

```text
02-async-concurrency.md
08-performance.md
09-security-secrets.md
11-crawler-platform-coding.md
06-testing.md
```

如果任务涉及页面测试：

```text
06-testing.md
```

如果涉及 Cookie / Storage State：

```text
09-security-secrets.md
```

---

# 12. Scrapling Task

关键词：

```text
Scrapling
Adaptive Parsing
Adaptive Selector
Selector
```

必须读取：

```text
11-crawler-platform-coding.md
10-project-structure.md
01-python-core-style.md
06-testing.md
ecom-scraper-dependencies-optimized-v2.md
```

并检查：

```text
Scrapling = Adapter
```

不能因为引入 Scrapling 而改变：

```text
Engine
Scheduler
Task
Pipeline
```

---

# 13. Product / SKU / Shop Task

关键词：

```text
Product
SKU
Shop
Brand
Category
Price
Inventory
Review
```

必须读取：

```text
04-data-model-and-database.md
11-crawler-platform-coding.md
12-data-analysis.md
01-python-core-style.md
06-testing.md
```

如果涉及价格：

```text
Money
Decimal
Currency
PriceHistory
PriceSnapshot
```

重点检查：

```text
04-data-model-and-database.md
```

---

# 14. Data Analysis Task

关键词：

```text
Analysis
Analytics
Price Trend
Inventory Trend
Ranking
Comparison
Metrics
Polars
ClickHouse
Elasticsearch
OLAP
```

必须读取：

```text
12-data-analysis.md
04-data-model-and-database.md
08-performance.md
01-python-core-style.md
06-testing.md
```

如果涉及 Elasticsearch：

```text
ecom-scraper-dependencies-optimized-v2.md
```

如果涉及 ClickHouse：

```text
ecom-scraper-dependencies-optimized-v2.md
```

---

# 15. Redis / Distributed Task

关键词：

```text
Redis
Distributed
Worker
Heartbeat
Lease
Distributed Queue
Distributed Dedup
Distributed Rate Limit
```

必须读取：

```text
ecom-scraper-5-versions-optimized-v2.md
ecom-scraper-dependencies-optimized-v2.md
02-async-concurrency.md
03-error-handling.md
08-performance.md
10-project-structure.md
06-testing.md
```

---

# 16. Kafka / Event Task

关键词：

```text
Kafka
Event
Event Stream
Consumer
Producer
PriceChanged
ProductUpdated
InventoryChanged
```

必须读取：

```text
ecom-scraper-5-versions-optimized-v2.md
ecom-scraper-dependencies-optimized-v2.md
04-data-model-and-database.md
12-data-analysis.md
03-error-handling.md
06-testing.md
08-performance.md
```

必须明确：

```text
Redis
→ Task Queue

Kafka
→ Event Stream
```

不要让 Kafka 替代 Redis 的任务调度职责，除非新的架构决策明确要求。

---

# 17. Performance Task

关键词：

```text
performance
optimization
benchmark
load test
throughput
latency
memory
CPU
QPS
concurrency
```

必须读取：

```text
08-performance.md
02-async-concurrency.md
06-testing.md
13-code-review-and-delivery.md
```

如果优化架构：

```text
10-project-structure.md
ecom-scraper-5-versions-optimized-v2.md
```

性能结论必须尽量有 Benchmark / Metrics 证据。

---

# 18. Security Task

关键词：

```text
security
secret
token
cookie
password
credential
auth
SSRF
permission
```

必须读取：

```text
09-security-secrets.md
01-python-core-style.md
05-api-design.md
06-testing.md
13-code-review-and-delivery.md
```

禁止输出或记录：

```text
Password
Token
Authorization
完整 Cookie
Secret
Proxy Credential
```

---

# 19. Logging / Monitoring Task

关键词：

```text
log
logging
structlog
Prometheus
Grafana
metrics
trace
observability
monitoring
```

必须读取：

```text
07-logging-observability.md
01-python-core-style.md
08-performance.md
06-testing.md
```

如果涉及 API：

```text
05-api-design.md
```

如果涉及 Worker：

```text
ecom-scraper-5-versions-optimized-v2.md
```

---

# 20. Testing Task

关键词：

```text
test
pytest
pytest-asyncio
mock
fixture
integration
E2E
regression
load test
```

必须读取：

```text
06-testing.md
01-python-core-style.md
13-code-review-and-delivery.md
```

然后根据测试对象增加：

```text
Async
→ 02-async-concurrency.md

Database
→ 04-data-model-and-database.md

API
→ 05-api-design.md

Crawler
→ 11-crawler-platform-coding.md

Analytics
→ 12-data-analysis.md
```

---

# 21. Refactor Task

如果任务是：

```text
重构
Refactor
Cleanup
Architecture Improvement
Simplify
Remove Duplication
```

必须读取：

```text
10-project-structure.md
01-python-core-style.md
02-async-concurrency.md（如果是 Async）
06-testing.md
08-performance.md（如果涉及性能）
13-code-review-and-delivery.md
ecom-scraper-5-versions-optimized-v2.md
```

重构必须先确认：

```text
Current Behavior
Desired Behavior
Risk
Tests
Rollback
```

禁止借重构名义扩大任务范围。

---

# 22. New Dependency Task

当 AI 想：

```text
增加 pip package
增加第三方库
替换技术
```

必须读取：

```text
ecom-scraper-dependencies-optimized-v2.md
ecom-scraper-5-versions-optimized-v2.md
10-project-structure.md
```

并回答：

```text
Purpose
Alternative
Current Version
Dependency Conflict
Architecture Impact
Testing Impact
```

改变核心技术必须考虑 ADR。

---

# 23. Architecture Task

关键词：

```text
Architecture
Design
Module
System Design
Boundary
Interface
Dependency
Engine
Distributed
Storage
```

必须读取：

```text
ecom-scraper-5-versions-optimized-v2.md
ecom-scraper-dependencies-optimized-v2.md
10-project-structure.md
```

如果产生重要技术决策：

```text
architecture-decision-records
```

需要同步更新 ADR。

---

# 24. Code Review Task

关键词：

```text
review
code review
quality
audit
quality gate
```

必须读取：

```text
13-code-review-and-delivery.md
01-python-core-style.md
10-project-structure.md
06-testing.md
```

按模块增加：

```text
Async → 02
DB → 04
API → 05
Crawler → 11
Analytics → 12
Security → 09
```

---

# 25. Release / Delivery Task

关键词：

```text
release
merge
PR
commit
delivery
finish
branch
deployment
```

必须读取：

```text
13-code-review-and-delivery.md
06-testing.md
ecom-scraper-5-versions-optimized-v2.md
```

如果 Docker：

```text
docker-patterns
```

如果部署：

```text
deployment-patterns
```

---

# 26. Docker Task

关键词：

```text
Docker
Dockerfile
Compose
Container
Image
Volume
Network
Healthcheck
```

必须读取：

```text
13-code-review-and-delivery.md
ecom-scraper-dependencies-optimized-v2.md
```

并调用：

```text
docker-patterns
```

如果涉及生产部署：

```text
deployment-patterns
```

---

# 27. Deployment Task

关键词：

```text
Deploy
Production
CI/CD
GitHub Actions
Release
Rollback
Blue-Green
Canary
```

必须读取：

```text
ecom-scraper-5-versions-optimized-v2.md
ecom-scraper-dependencies-optimized-v2.md
13-code-review-and-delivery.md
```

并调用：

```text
deployment-patterns
```

---

# 28. Git Task

关键词：

```text
Git
branch
commit
merge
PR
worktree
rebase
```

应该调用：

```text
git-workflow
```

如果并行 Agent：

```text
using-git-worktrees
dispatching-parallel-agents
```

如果开发结束：

```text
finishing-a-development-branch
```

---

# 29. AI Development Planning Task

关键词：

```text
计划
Plan
开发方案
Implementation Plan
Milestone
Task Breakdown
```

调用：

```text
goal
brainstorming
writing-plans
```

然后：

```text
ecom-scraper-5-versions-optimized-v2.md
```

确认当前 Version / Milestone。

---

# 30. AI Implementation Task

开始实际编码时：

```text
goal
 ↓
writing-plans
 ↓
executing-plans
 ↓
01-feature / 04-agent-coding
```

然后根据代码类型读取：

```text
Python
→ 01-python-core-style

Async
→ 02-async-concurrency

DB
→ 04-data-model-and-database

API
→ 05-api-design

Crawler
→ 11-crawler-platform-coding
```

---

# 31. AI Debug Task

遇到：

```text
Bug
Failure
Exception
Regression
Unexpected Result
```

调用：

```text
systematic-debugging
```

再根据问题读取：

```text
Async → 02-async-concurrency
Error → 03-error-handling
DB → 04-data-model-and-database
Crawler → 11-crawler-platform-coding
Performance → 08-performance
```

禁止没有证据直接修改代码。

---

# 32. Parallel Agent Task

出现多个独立任务：

```text
Product
Shop
Price
```

可以：

```text
dispatching-parallel-agents
```

如果使用 Git Worktree：

```text
using-git-worktrees
```

核心共享接口任务：

```text
Request
Engine
Scheduler
```

不要在接口尚未稳定时盲目并行。

---

# 33. Feature Development Task

新功能完整流程：

```text
01-feature
```

配合：

```text
goal
brainstorming
writing-plans
executing-plans
test-driven-development
04-agent-coding
verification-before-completion
```

代码类型再加载对应技术规范。

---

# 34. Completion Routing

任何功能完成前：

```text
verification-before-completion
```

然后：

```text
06-testing
13-code-review-and-delivery
```

最后：

```text
finishing-a-development-branch
```

---

# 35. Required Reading Matrix

| 任务 | 必读 |
|---|---|
| 普通 Python | 01 + 10 + 06 |
| Async | 01 + 02 + 03 + 06 + 08 |
| Error | 01 + 03 + 06 |
| Database | 01 + 04 + 06 + 10 |
| API | 01 + 04 + 05 + 06 + 10 |
| Crawler Engine | Roadmap + 01 + 10 + 11 + 03 + 06 |
| Platform | 01 + 06 + 10 + 11 |
| Playwright | 02 + 06 + 08 + 09 + 11 |
| Scrapling | 01 + 06 + 10 + 11 + Dependencies |
| Product/SKU | 01 + 04 + 06 + 11 + 12 |
| Analytics | 01 + 04 + 06 + 08 + 12 |
| Redis/Distributed | Roadmap + Dependencies + 02 + 03 + 06 + 08 + 10 |
| Kafka | Roadmap + Dependencies + 03 + 04 + 06 + 08 + 12 |
| Performance | 02 + 06 + 08 + 13 |
| Security | 01 + 05 + 06 + 09 + 13 |
| Observability | 01 + 06 + 07 + 08 |
| Refactor | Roadmap + 01 + 06 + 10 + 13 |
| Dependency | Roadmap + Dependencies + 10 |
| Architecture | Roadmap + Dependencies + 10 + ADR |
| Review | 01 + 06 + 10 + 13 |
| Docker | Dependencies + 13 + docker-patterns |
| Deployment | Roadmap + Dependencies + 13 + deployment-patterns |

---

# 36. Priority Rules

当多个文件匹配时按以下优先级：

```text
P0
当前 Version / Milestone
        ↓
P1
Project Structure
        ↓
P2
Domain / Technical Standard
        ↓
P3
Testing / Error / Security
        ↓
P4
Performance / Observability
        ↓
P5
Delivery
```

例如：

```text
“实现 V3 Amazon Product Parser”
```

读取：

```text
P0:
ecom-scraper-5-versions-optimized-v2

P1:
10-project-structure

P2:
11-crawler-platform-coding
01-python-core-style

P3:
06-testing
03-error-handling

P4:
08-performance

P5:
13-code-review-and-delivery
```

---

# 37. Avoid Context Explosion

禁止每个任务无条件读取全部 15 个 Markdown。

例如普通函数修改：

```text
只需要：
01
10
06
```

而不是：

```text
15 files
```

只有以下情况才读取 Roadmap + Dependencies：

```text
Version Planning
Architecture
Dependency Change
Cross-module Change
Distributed Change
Major Refactor
```

---

# 38. Conflict Resolution

如果不同文档存在冲突：

```text
当前任务明确要求
        ↓
当前 Version 约束
        ↓
Architecture / Dependency Baseline
        ↓
Specific Technical Standard
```

发现真正架构冲突时：

```text
停止直接修改
 ↓
Brainstorming
 ↓
Writing Plan
 ↓
ADR
 ↓
再实施
```

AI 不允许自行悄悄改变项目技术基线。

---

# 39. Final Routing Rule

AI 每次开始代码任务必须先执行：

```text
Step 1
识别任务类型

Step 2
识别当前 Version / Milestone

Step 3
读取 Project Structure

Step 4
读取对应技术规范

Step 5
读取 Testing / Error / Security 等相关规范

Step 6
开始 Plan

Step 7
Implementation

Step 8
Verification

Step 9
Review

Step 10
Delivery
```

最终形成：

```text
Task
 ↓
Task Classification
 ↓
Relevant Standards
 ↓
Goal
 ↓
Plan
 ↓
Implementation
 ↓
Test
 ↓
Verification
 ↓
Review
 ↓
Commit
```

任何没有经过上述路由判断的代码修改，都视为不符合 `ecom-scraper` AI 开发规范。