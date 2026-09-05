# Performance and Resource Coding Standard

## 1. Principle

优化顺序：

```text
Correctness
 ↓
Measurement
 ↓
Optimization
 ↓
Benchmark
```

没有指标或 Benchmark，不要随意声称“性能更好”。

## 2. Network

优先：

```text
Connection Pool
Keep-Alive
合理 Timeout
合理 Concurrency
```

不要：

```text
One Request
→ One Session
→ One Connection
```

## 3. Memory

禁止无界：

```text
Queue
Task
List
Cache
Browser
```

需要明确：

```text
最大数量
TTL
回收策略
```

## 4. Backpressure

当 Producer > Consumer：

```text
Queue Growth
 ↓
Backpressure
 ↓
Producer Slowdown
```

而不是：

```text
Queue Growth
 ↓
Memory Explosion
```

## 5. Database

批量写入优先于逐条写入，但必须结合：

```text
transaction size
latency
memory
lock contention
```

不要为了 batch 一味扩大事务。

## 6. Parser

优先：

```text
结构化 API / JSON
 ↓
稳定 DOM
 ↓
CSS/XPath
 ↓
Adaptive Parsing
```

不要所有页面都运行 Browser。

## 7. Browser

Browser 是高成本资源：

```text
Browser concurrency << HTTP concurrency
```

必须监控：

```text
Browser count
Context count
Page count
Memory
CPU
```

## 8. Serialization

高吞吐 JSON 场景可以使用：

```text
orjson
```

但不要为了序列化性能牺牲数据正确性。

## 9. CPU-heavy Work

CPU 密集型分析不要阻塞 Event Loop。

必要时使用：

```text
Process Pool
Dedicated Worker
Batch Job
```

## 10. Load Testing

V2 起必须进行负载测试。

至少记录：

```text
Throughput
P50
P95
P99
Error Rate
Memory
CPU
Queue Size
Connections
```

对比优化前后再决定是否保留优化。
