# 架构设计

## 目录结构

```
publish-app-mcp/
├── docs/                           # 文档
├── src/
│   └── publish_app_mcp/
│       ├── __init__.py
│       ├── server.py               # MCP Server 入口
│       ├── models.py               # 数据模型 (Pydantic)
│       ├── config.py               # 配置管理
│       ├── tools/                  # MCP 工具层
│       └── stores/                 # 应用商店封装
│           ├── base.py             # 基类
│           ├── app_store.py        # App Store
│           ├── xiaomi.py           # 小米
│           ├── huawei.py           # 华为
│           ├── oppo.py             # OPPO
│           ├── vivo.py             # vivo
│           ├── samsung.py          # 三星
│           └── yingyongbao.py      # 应用宝
├── pyproject.toml
└── .env.example
```

## 分层架构

### 1. MCP Server 层 (server.py)
- 实现 MCP 协议
- 暴露工具端点
- 处理请求路由

### 2. 工具层 (tools/)
- 业务逻辑编排
- 参数验证
- 错误处理

### 3. 商店层 (stores/)
- 各应用商店 API 封装
- 统一接口
- 各商店独立实现

### 4. 模型层 (models.py)
- 数据结构定义
- 类型安全

### 5. 配置层 (config.py)
- 环境变量加载
- 配置管理

## 扩展新的应用商店

1. 继承 `AppStoreBase`
2. 实现所有抽象方法
3. 在 `stores/__init__.py` 中注册

```python
# stores/my_store.py
from .base import AppStoreBase

class MyStore(AppStoreBase):
    store_type = AppStore.MY_STORE

    async def upload_app(self, file_path, track):
        # 实现上传
        pass
```

## 数据流

```
MCP Client
    ↓
Server.call_tool()
    ↓
Store.upload_app()
    ↓
第三方 API
    ↓
返回结果
```
