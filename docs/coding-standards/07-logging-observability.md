# Logging and Observability Coding Standard

## 1. Logging

生产代码禁止使用：

```python
print(...)
```

统一使用结构化日志，例如：

```text
structlog
```

## 2. Event Naming

事件名使用稳定、可搜索的语义：

```text
request_started
request_completed
request_failed

parse_started
parse_failed

task_started
task_completed
task_failed
```

避免：

```text
something_wrong
debug
test
```

## 3. Context

日志尽量携带：

```text
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

## 4. Sensitive Data

绝对禁止日志输出：

```text
Password
Token
Authorization
Secret
完整 Cookie
Proxy Credential
```

必要时进行：

```text
mask
hash
redaction
```

## 5. Metrics

Metrics 与日志职责分离。

日志：

```text
发生了什么？
```

Metrics：

```text
发生了多少？
比例是多少？
趋势如何？
```

## 6. Core Metrics

至少维护：

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

## 7. Platform Metrics

建议增加：

```text
platform_request_success_rate
platform_parse_success_rate
platform_latency
platform_retry_rate
platform_error_rate
```

## 8. Analysis Metrics

数据分析相关 Metrics 建议独立：

```text
price_snapshot_count
inventory_snapshot_count
product_update_count
analysis_job_duration
analysis_job_failure
```

不要把业务分析指标和 crawler runtime 指标混成无法区分的指标体系。

## 9. Traceability

一次任务应尽量能够关联：

```text
task_id
request_id
worker_id
platform
```

形成完整链路：

```text
Task
 ↓
Request
 ↓
Fetcher
 ↓
Parser
 ↓
Pipeline
 ↓
Storage
```
