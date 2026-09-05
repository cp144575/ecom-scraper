# Data Analysis Coding Standard

## 1. Scope

适用于 V3 基础分析及 V5 Analysis Domain。

## 2. Separation

分析不直接修改采集核心状态。

```text
Crawler
 ↓
Storage / Event
 ↓
Analysis
```

## 3. Analysis Modules

```text
analysis/
├── metrics/
├── trends/
├── comparison/
├── ranking/
└── reports/
```

## 4. Metrics

典型：

```text
Product Count
SKU Count
Average Price
Min Price
Max Price
Price Change
Price Volatility
Inventory Trend
Review Growth
Platform Price Difference
```

## 5. Time Series

价格、库存等指标应尽量保留 Snapshot：

```text
entity
value
currency
captured_at
```

不要只保存最新值，否则无法计算趋势。

## 6. OLTP / Search / OLAP

职责：

```text
MySQL
→ OLTP / Source of Truth

Elasticsearch
→ Search

ClickHouse
→ OLAP
```

不要让一个数据库承担所有类型查询。

## 7. Polars

批量分析可以：

```text
Query
 ↓
Polars
 ↓
Aggregation
 ↓
Report
```

不要把 Polars 放入：

```text
Crawler → Parser
```

在线主链路。

## 8. Reproducibility

分析结果必须尽可能可以追溯：

```text
data range
filters
source
calculation rule
version
```

## 9. Business Metrics

业务指标命名必须明确：

```text
price_change_rate_30d
average_price
out_of_stock_rate
```

不要：

```text
rate1
value2
score
```

## 10. Validation

分析结果必须检查：

```text
null
outlier
currency
time zone
duplicate snapshot
```

不能因为“能算出结果”就认为结果正确。
