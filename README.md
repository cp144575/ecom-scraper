# ecom-scraper

自研异步爬虫引擎 + 国内/海外电商多平台采集 + 分布式 Worker + 数据分析 + 生产管理平台。

当前进度：**V1（Minimal MVP）** —— 用自研同步爬虫引擎跑通 `URL → Engine → Product → MySQL` 最小闭环，作为后续版本的地基。

## V1 目标与范围

- 跑通一次完整采集：请求 → 调度 → 下载 → 解析 → 规范模型 → 入库。
- 仅实现 V1 核心模块；不引入异步并发体系、平台适配器、分布式、API、浏览器（这些分别属于 V2/V3/V4/V5）。

## 目录结构

```text
src/ecom_scraper/
├── engine/        # Engine：编排全链路
├── request/       # Request / Response
├── scheduler/     # 内存 FIFO 调度 + URL 去重
├── fetcher/       # Fetcher 协议 + httpx 实现
├── spider/        # Spider 基类 + 演示 Spider
├── parser/        # ProductParser（selectolax）
├── models/        # Product 规范模型（Pydantic）
├── pipeline/      # 入库前处理
├── storage/       # SQLAlchemy ORM + Repository + session
├── config/        # 环境配置
└── exceptions/    # 异常层级
```

## 快速开始

```bash
uv sync
cp .env.example .env   # 默认 SQLite，开箱即用
uv run python examples/basic-crawler/main.py
```

演示脚本会抓取 `books.toscrape.com` 的一个商品页，并把解析出的 `Product` 写入数据库（默认 SQLite 文件 `ecom_scraper.db`）。

## 测试与质量门禁

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

四条命令全部通过才算完成交付。

## 使用 MySQL（生产路径）

MySQL 是 V1 的 Source of Truth。两种方式：

1. 本地已有 MySQL：在 `.env` 里配置
   `DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/ecom_scraper?charset=utf8mb4`
2. 用 Docker（可选）：
   ```bash
   docker compose up -d mysql
   ```

建表走 Alembic 迁移：

```bash
uv run alembic upgrade head
```

## 路线图

- [五版本开发路线](roadmap/ecom-scraper-5-versions-optimized-v2.md)
- [技术栈与依赖清单](roadmap/ecom-scraper-dependencies-optimized-v2.md)
- [编码规范](docs/coding-standards/)
