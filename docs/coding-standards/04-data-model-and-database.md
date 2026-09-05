# Data Model and Database Coding Standard

## 1. Responsibilities

数据层必须区分：

```text
Domain Model
ORM Model
API Schema
Raw Platform Data
```

不要让一种 Model 承担所有职责。

## 2. Pydantic

跨模块传递的结构化数据优先使用 Pydantic。

例如：

```python
class Product(BaseModel):
    platform: str
    platform_product_id: str
    title: str
    price: Decimal | None = None
    currency: str
```

避免大型模块之间使用：

```python
dict[str, Any]
```

作为长期接口。

## 3. Canonical Model

平台数据必须：

```text
Raw Platform Data
 ↓
Platform Item
 ↓
Normalizer
 ↓
Canonical Model
 ↓
Validator
 ↓
Pipeline
```

平台不能直接将原始字段写入主业务表。

## 4. Money

价格核心类型使用：

```python
Decimal
```

不要使用 `float` 保存核心金额。

金额必须和币种同时存在：

```text
amount
currency
```

不要假设所有平台使用 CNY。

## 5. Time

跨平台时间统一使用 timezone-aware datetime。

业务数据必须明确：

```text
captured_at
created_at
updated_at
```

涉及跨市场数据时保存明确时区语义。

## 6. IDs

明确区分：

```text
internal_product_id
platform_product_id

internal_shop_id
platform_shop_id

task_id
request_id
worker_id
```

禁止一个 `id` 在多个层级承担不同语义。

## 7. SQLAlchemy

使用：

```text
SQLAlchemy 2.x
AsyncSession
```

Repository 负责持久化访问。

推荐：

```text
Pipeline
 ↓
Repository
 ↓
SQLAlchemy
 ↓
Driver
 ↓
MySQL
```

## 8. Repository

Repository 应负责：

```text
CRUD
Query
Transaction boundary
```

不要把复杂业务分析塞进 Repository。

不要让 Spider 直接访问 Session。

## 9. ORM vs Domain

不要强迫 ORM Model 直接成为所有业务层对象。

需要时使用：

```text
ORM Model
↕
Mapper
↕
Domain Model
```

## 10. Transaction

事务边界必须清晰。

避免：

```text
一个巨大事务
```

跨越：

```text
Fetch
Parse
多个业务操作
长时间网络等待
```

网络 IO 不应该长时间占用数据库事务。

## 11. Migrations

Schema 修改使用 Alembic。

禁止手工修改生产 Schema 后不提交 Migration。

## 12. Indexing

索引应基于查询模式设计。

重点考虑：

```text
platform + platform_product_id
shop_id
captured_at
task_id
status
```

不要没有查询证据就大量建立索引。

## 13. Database Quality Checklist

- 是否正确区分 Domain / ORM / API Model？
- 是否使用 Decimal？
- 是否保存 currency？
- 时间是否带时区？
- ID 是否语义明确？
- Repository 是否隔离？
- 事务是否过大？
- Migration 是否存在？
- Index 是否有查询依据？
