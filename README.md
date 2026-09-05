# ecom-scraper

自研异步爬虫引擎 + 国内/海外电商多平台采集 + 分布式 Worker + 数据分析 + 生产管理平台。

当前进度：**V5（Production & Analytics Platform）** —— 在 V4 分布式采集之上，加入 FastAPI 控制面（任务/平台/Worker/分析 API）、Prometheus 指标、Polars 批量分析、Docker Compose 与 GitHub Actions CI/CD。

## 目录结构

```text
src/ecom_scraper/
├── engine/        # AsyncEngine：异步 worker 编排
├── request/       # Request / Response / fingerprint 去重
├── queue/         # 有界队列（内存 / Redis）
├── distributed/   # 分布式队列 / 租约 / 心跳 / 恢复 / 去重 / 限流
├── concurrency/   # 全局 + 域名级并发控制
├── retry/         # RetryPolicy：指数退避 + 抖动
├── rate_limit/    # 令牌桶限流
├── fetcher/       # aiohttp / Playwright fetcher
├── browser/       # Playwright 浏览器管理与上下文池
├── proxy/         # 代理池 / 选择 / 校验 / 健康
├── spider/        # Spider 基类
├── platform/      # PlatformAdapter + cn/{jd,taobao} + intl/amazon
├── parser/        # ProductParser（selectolax）
├── normalizer/    # 价格 / 币种 / ID 归一
├── validator/     # Canonical Model 校验
├── models/        # Product / Shop / SKU / Snapshot
├── pipeline/      # 入库前处理
├── storage/       # SQLAlchemy 2.x 异步 ORM + Repository
├── analysis/      # 价格 / 库存指标 + 平台比较
├── config/        # 环境配置
├── api/           # FastAPI 控制面（tasks/platforms/workers/analytics）
├── observability/ # structlog 日志 + Prometheus 指标
└── exceptions/    # 异常层级
```

## 快速开始

```bash
uv sync
cp .env.example .env   # 默认异步 SQLite，开箱即用
uv run python examples/basic-crawler/main.py
```

平台解析采用 fixture 优先（合规、可复现），真实站点抓取需 Playwright 浏览器与代理：`playwright install chromium` 后启用浏览器测试。

## 测试与质量门禁

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

四条命令全部通过才算完成交付。

## API 服务

`ash
uv run uvicorn ecom_scraper.api.app:app --reload
`

接口：/health、/metrics、/tasks、/platforms、/workers、/products、/analytics/*。

## 多 worker 负载测试

`ash
uv run python scripts/benchmark/multi_worker_load_test.py 100000 5
``n
## 负载测试

```bash
uv run python scripts/benchmark/load_test.py 10000 100
```

## 使用 MySQL / Redis（生产路径）

MySQL 是 Source of Truth，Redis 承担队列/去重/限流状态。在 `.env` 配置：

```text
DATABASE_URL=mysql+asyncmy://root:password@127.0.0.1:3306/ecom_scraper?charset=utf8mb4
SYNC_DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/ecom_scraper?charset=utf8mb4
REDIS_URL=redis://127.0.0.1:6379/0
```

或 `docker compose up -d mysql redis`。建表走 Alembic：`uv run alembic upgrade head`。

## 路线图

- [五版本开发路线](roadmap/ecom-scraper-5-versions-optimized-v2.md)
- [技术栈与依赖清单](roadmap/ecom-scraper-dependencies-optimized-v2.md)
- [编码规范](docs/coding-standards/)


