# publish-app-mcp

MCP Server 用于自动化发布 App 到各大应用商店。

## 功能特性

### 应用商店支持

- ✅ App Store (iOS/macOS) - 使用 fastlane pilot/altool
- ⏳ 小米开放平台 - 占位实现
- ⏳ 华为应用市场 - 占位实现
- ⏳ OPPO 开放平台 - 占位实现
- ⏳ vivo 开放平台 - 占位实现
- ⏳ 三星应用商店 - 占位实现
- ⏳ 应用宝 - 占位实现

### App 格式

- `.ipa` - iOS App
- `.aab` - Android App Bundle
- `.apk` - Android APK

### MCP 工具

- `upload_app` - 上传 App 到应用商店
- `get_upload_status` - 查询上传状态
- `update_metadata` - 更新应用元数据
- `submit_review` - 提交审核
- `get_version_info` - 获取应用商店版本信息
- `get_project_version` - 获取本地项目版本号
- `set_project_version` - 设置本地项目版本号
- `increment_project_build` - 自动增加项目构建号

### 项目管理

- Xcode 项目 (Info.plist) 版本管理
- Android 项目 (build.gradle) 版本管理
- 语义化版本号递增

## 安装

```bash
# 克隆项目
git clone <repo-url>
cd publish-app-mcp

# 使用 pip 安装
pip install -e .
```

### 前置要求

- Python 3.10+
- Xcode 命令行工具 (用于 App Store)
- fastlane (可选，推荐)

```bash
# 安装 Xcode 命令行工具
xcode-select --install

# 安装 fastlane (推荐)
brew install fastlane
# 或
gem install fastlane
```

## 配置

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
# 编辑 .env
```

### App Store 配置

1. 在 App Store Connect 创建 API Key
2. 下载私钥文件 (AuthKey_XXXXXX.p8)
3. 配置环境变量：

```env
APP_STORE_KEY_ID=XXXXXX
APP_STORE_ISSUER_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
APP_STORE_PRIVATE_KEY_PATH=/path/to/AuthKey_XXXXXX.p8
APP_STORE_BUNDLE_ID=com.yourcompany.yourapp
```

## MCP 配置

在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "publish-app": {
      "command": "python",
      "args": ["-m", "publish_app_mcp.server"],
      "cwd": "/path/to/publish-app-mcp",
      "env": {
        "APP_STORE_KEY_ID": "...",
        "APP_STORE_ISSUER_ID": "...",
        "APP_STORE_PRIVATE_KEY_PATH": "..."
      }
    }
  }
}
```

## 使用

### 在 Claude 中使用

1. 启动 Claude Desktop
2. 告诉 Claude 你要发布 App

示例：

```
帮我发布新版本到 App Store：
1. 增加项目构建号
2. 上传 /path/to/app.ipa
3. 更新发布说明
4. 提交审核
```

### 作为 Python 库使用

```python
import asyncio
from publish_app_mcp.tools import upload_app
from publish_app_mcp.models import ReleaseTrack

async def main():
    result = await upload_app(
        store_name="app_store",
        file_path="/path/to/app.ipa",
        track=ReleaseTrack.BETA,
    )
    print(result)

asyncio.run(main())
```

## 文档

- [需求文档](docs/requirements.md)
- [架构设计](docs/architecture.md)
- [使用指南](docs/usage.md)

## 项目结构

```
publish-app-mcp/
├── docs/                     # 文档
├── examples/                 # 示例脚本
├── src/publish_app_mcp/
│   ├── server.py            # MCP Server
│   ├── models.py            # 数据模型
│   ├── config.py            # 配置
│   ├── tools/               # 工具模块
│   └── stores/              # 应用商店封装
├── pyproject.toml
├── .env.example
└── README.md
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 项目结构检查
tree -L 3 -I '__pycache__|*.pyc'
```

## 贡献

欢迎贡献！特别是国内 Android 商店的集成。

## License

MIT
