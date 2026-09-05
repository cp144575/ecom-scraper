# Python Core Coding Standard

## 1. Scope

适用于 `ecom-scraper` 全部 Python 源码。

技术基线：

- Python 3.12+
- `uv` 管理依赖
- Ruff 负责 lint/format
- mypy 负责类型检查
- pytest 负责测试

## 2. General Principles

代码优先级：

1. 正确性
2. 可维护性
3. 可测试性
4. 类型安全
5. 性能
6. 简洁

规则：

- Explicit over clever。
- Small change over broad refactor。
- Single Responsibility。
- 不为了少写几行代码引入复杂抽象。
- 不修改与当前任务无关的代码。

## 3. Naming

模块、函数、变量：

```python
retry_policy.py
fetch_product()
max_attempts
```

类：

```python
RetryPolicy
ProductParser
AioHttpFetcher
```

常量：

```python
DEFAULT_TIMEOUT = 10.0
MAX_RETRY_ATTEMPTS = 3
```

布尔值：

```python
is_active
has_stock
should_retry
```

禁止无语义命名：

```python
data
obj
tmp
x
manager
helper
utils
```

除非上下文明确且生命周期极短。

## 4. Type Hints

公共函数必须标注参数和返回值：

```python
async def fetch_product(
    request: Request,
    *,
    timeout: float = 10.0,
) -> Response:
    ...
```

Python 3.12+ 优先：

```python
list[str]
dict[str, int]
str | None
```

避免新代码使用：

```python
Optional[str]
List[str]
Dict[str, int]
```

避免无理由使用：

```python
Any
cast(...)
# type: ignore
```

## 5. Functions

函数单一职责。

推荐：

```python
def normalize_price(value: str) -> Decimal:
    ...


def normalize_currency(value: str) -> str:
    ...
```

避免：

```python
def process_product_everything(...):
    ...
```

一个函数同时承担请求、解析、校验、持久化和日志。

## 6. Parameters

可选参数优先 keyword-only：

```python
async def fetch(
    request: Request,
    *,
    timeout: float = 10.0,
    proxy: Proxy | None = None,
) -> Response:
    ...
```

避免不必要的 `*args` / `**kwargs`。

## 7. Imports

顺序：

```text
标准库
↓
第三方库
↓
本地项目
```

示例：

```python
import asyncio
from collections.abc import Sequence

import aiohttp
from pydantic import BaseModel

from ecom_scraper.models.product import Product
```

禁止循环导入。

## 8. Constants

魔法值必须提取：

```python
DEFAULT_TIMEOUT = 10.0
MAX_PAGE_SIZE = 100
```

不要：

```python
await client.get(url, timeout=37)
```

## 9. Comments

注释解释 Why，不重复 What。

不要：

```python
# Increment counter
counter += 1
```

应该：

```python
# Keep logical-request count stable across retries.
counter += 1
```

## 10. Docstrings

公共 API 使用 Google-style docstring。

```python
def normalize_price(value: str) -> Decimal:
    """Normalize a platform price string.

    Args:
        value: Raw price text.

    Returns:
        Normalized decimal price.

    Raises:
        ValueError: If the value cannot be parsed.
    """
```

## 11. Mutable Defaults

禁止：

```python
def func(items=[]):
    ...
```

应该：

```python
def func(items: list[str] | None = None) -> None:
    if items is None:
        items = []
```

## 12. Resource Lifecycle

有生命周期的资源必须显式管理：

```text
HTTP Session
Redis Connection
DB Session
Browser
Context
Page
File
```

优先：

```python
async with ...
```

或：

```python
try:
    ...
finally:
    cleanup()
```

## 13. Public API

稳定公共接口必须谨慎修改。

修改公共接口前：

- 检查调用方
- 添加/更新测试
- 评估向后兼容
- 必要时创建 ADR

## 14. Python Quality Gate

提交前：

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

代码未通过质量门禁不得标记为完成。
