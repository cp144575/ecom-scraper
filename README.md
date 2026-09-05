# ecom-scraper

自研异步爬虫引擎 + 国内/海外电商多平台采集 + 分布式 Worker + 数据分析 + 生产管理平台。

当前进度：**V2（Async High Concurrency）** —— 单机 Async-first 高并发采集 Engine，在 V1 的 `URL → Engine → Product → MySQL` 闭环基础上加入异步抓取、并发控制、超时重试、限流、去重、有界队列背压与异步入库。

## 目录结构

```text
src/ecom_scraper/
├── engine/        # AsyncEngine：异步 worker 编排
├── request/       # Request / Response / fingerprint 去重
├── queue/         # 有界队列（内存 / Redis）
├── concurrency/   # 全局 + 域名级并发控制
├── retry/         # RetryPolicy：指数退避 + 抖动
├── rate_limit/    # 令牌桶限流
├── fetcher/       # Fetcher 协议 + aiohttp 实现
├── spider/        # Spider 基类 + 演示 Spider
├── parser/        # ProductParser（selectolax）
├── models/        # Product 规范模型（Pydantic）
├── pipeline/      # 入库前处理
├── storage/       # SQLAlchemy 2.x 异步 ORM + Repository
├── config/        # 环境配置
├── observability/ # structlog 结构化日志
└── exceptions/    # 异常层级
```

## 快速开始

```bash
uv sync
cp .env.example .env   # 默认异步 SQLite，开箱即用
uv run python examples/basic-crawler/main.py
```

演示脚本会异步抓取 `books.toscrape.com` 的一个商品页，并把解析出的 `Product` 写入数据库（默认 SQLite 文件 `ecom_scraper.db`）。

## 测试与质量门禁

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

四条命令全部通过才算完成交付。

## 负载测试

```bash
uv run python scripts/benchmark/load_test.py 10000 100
```

输出吞吐、p50/p95 延迟、错误率等基线指标。

## 使用 MySQL / Redis（生产路径）

MySQL 是 Source of Truth，Redis 承担队列/去重/限流状态。两种方式：

1. 本地已有服务：在 `.env` 配置 `DATABASE_URL=mysql+asyncmy://...` 与 `SYNC_DATABASE_URL=mysql+pymysql://...`（迁移用）、`REDIS_URL=...`。
2. 用 Docker（可选）：
   ```bash
   docker compose up -d mysql redis
   ```

建表走 Alembic 迁移：

```bash
uv run alembic upgrade head
```

## 路线图

- [五版本开发路线](roadmap/ecom-scraper-5-versions-optimized-v2.md)
- [技术栈与依赖清单](roadmap/ecom-scraper-dependencies-optimized-v2.md)
- [编码规范](docs/coding-standards/)
