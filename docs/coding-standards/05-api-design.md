# API and Service Coding Standard

## 1. Scope

适用于 V5 FastAPI 控制面和 Analytics API。

## 2. Layering

API 不直接操作：

```text
SQLAlchemy Session
Redis internals
Crawler Engine internals
```

推荐：

```text
Router
 ↓
Application Service
 ↓
Domain / Task Service
 ↓
Repository / Queue
```

## 3. Request / Response Schema

API 使用独立 Pydantic Schema：

```text
CreateTaskRequest
TaskResponse
ProductResponse
AnalyticsResponse
```

不要直接把 ORM 对象作为 API 合约。

## 4. HTTP Semantics

正确使用：

```text
GET
POST
PUT/PATCH
DELETE
```

状态码需要表达明确语义。

## 5. Pagination

列表 API 必须考虑分页。

例如：

```text
page
page_size
```

或：

```text
cursor
limit
```

不要默认返回无限数据。

## 6. Error Response

错误响应应统一结构，例如：

```json
{
  "code": "TASK_NOT_FOUND",
  "message": "Task was not found",
  "request_id": "..."
}
```

不要向客户端返回内部 stack trace。

## 7. Idempotency

涉及：

```text
创建任务
启动任务
停止任务
重试任务
```

等状态变更操作时，要明确是否需要幂等。

## 8. Authentication

认证实现与业务服务解耦。

凭据、Token、Secret 不允许硬编码。

## 9. Validation

输入参数在 API 边界完成基础校验。

业务规则由 Application/Domain 层验证。

## 10. API Quality Checklist

- Schema 是否独立？
- API 是否直接访问 DB？
- 是否有分页？
- 状态码是否正确？
- 错误格式是否统一？
- 是否泄露内部异常？
- 是否需要幂等？
- 是否具备 request_id？
