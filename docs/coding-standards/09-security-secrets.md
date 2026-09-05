# Security and Secrets Coding Standard

## 1. Secrets

禁止提交：

```text
Password
API Key
Token
Cookie
Proxy Credential
JWT Secret
Database Password
```

到 Git。

## 2. Configuration

敏感配置通过：

```text
Environment Variables
Secret Manager
Deployment Secret
```

注入。

## 3. Logging

禁止：

```text
Authorization
Cookie
Password
Token
Secret
```

进入普通日志。

## 4. Error Messages

对外错误信息不得暴露：

```text
SQL
Stack Trace
File Path
Credential
Internal Service Detail
```

## 5. Dependency Security

新增依赖前检查：

```text
是否必要
是否成熟
是否维护
是否与现有依赖冲突
```

依赖版本通过：

```text
pyproject.toml
uv.lock
```

管理。

## 6. Input Validation

所有外部输入：

```text
URL
Task Config
Platform Parameters
API Input
```

都必须在进入核心逻辑前完成基础校验。

## 7. SSRF / URL Safety

如果系统接受用户提供 URL，需要定义允许范围：

```text
Allowed Scheme
Allowed Host
Blocked Private Network
Blocked Internal Metadata Endpoint
```

不能默认允许任意内部地址。

## 8. Browser Security

Browser context 中的敏感 Cookie / Storage State：

```text
不要提交 Git
不要写普通日志
不要长期无保护保存
```

## 9. Principle

采用最小权限：

```text
API
→ 只访问需要的服务

Worker
→ 只访问需要的队列/数据库

Analysis
→ 只访问需要的数据
```
