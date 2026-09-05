# Crawler and Platform Adapter Coding Standard

## 1. Platform Adapter

平台代码只负责平台差异：

```text
Request Construction
Response Interpretation
Parsing
Field Mapping
Platform-specific Rules
```

不要重新实现：

```text
Scheduler
Queue
Retry
Concurrency
DB
```

## 2. Canonical Output

平台最终输出：

```text
Product
SKU
Shop
Price
Inventory
Review
```

进入统一模型。

## 3. Parsing Strategy

优先级：

```text
Structured API / JSON
 ↓
Stable DOM
 ↓
CSS / XPath
 ↓
Adaptive Parsing
```

不要默认 Browser + Adaptive Parsing。

## 4. Raw Data

如果业务需要保存原始数据：

```text
Raw HTML
Raw JSON
Screenshot
Trace
```

进入 Raw/Object Storage 体系。

不要把大 Raw Payload 塞进核心 Product 表。

## 5. Product ID

平台字段：

```text
platform_product_id
```

内部字段：

```text
internal_product_id
```

二者不能混淆。

## 6. Price

必须同时记录：

```text
price
currency
captured_at
```

如果业务有：

```text
original_price
discount
promotion
```

应分别建模，不把价格信息全部放进一个字符串。

## 7. SKU

SKU 属性必须结构化：

```python
{
    "color": "Black",
    "size": "L",
}
```

不要将多维 SKU 信息拼成无法查询的长字符串。

## 8. Shop

商品与店铺关系必须明确：

```text
Product
 ↓
shop_id
 ↓
Shop
```

## 9. Platform Tests

每个平台必须有：

```text
fixtures
parser tests
normalization tests
regression tests
```

真实站点测试不能成为唯一测试手段。

## 10. Platform Failure

平台结构变化时：

```text
Fetch Success
≠
Parse Success
```

必须分别统计和处理。

## 11. Compliance

采集实现应遵守目标平台的适用条款、权限和法律要求。

不要为了规避访问控制而把平台特定绕过逻辑写入 Core Engine。
