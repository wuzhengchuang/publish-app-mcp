# 使用指南

## 安装

### 1. 克隆项目

```bash
git clone <repo-url>
cd publish-app-mcp
```

### 2. 安装依赖

```bash
# 使用 pip
pip install -e .
```

## 配置

### App Store

1. 在 App Store Connect 创建 API Key
2. 下载私钥文件 (AuthKey_XXXXXX.p8)
3. 配置环境变量：

```env
APP_STORE_KEY_ID=XXXXXX
APP_STORE_ISSUER_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
APP_STORE_PRIVATE_KEY_PATH=/path/to/AuthKey_XXXXXX.p8
APP_STORE_BUNDLE_ID=com.yourcompany.yourapp
```

### 国内 Android 商店

各国内商店需要在对应开放平台申请 API 权限，详见各平台文档。

## 配置 Claude Desktop

在 `claude_desktop_config.json` 中添加：

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

## MCP 工具使用

### 1. 上传 App

```
请帮我上传 App 到 App Store
- 文件路径: /path/to/app.ipa
```

### 2. 查询上传状态

```
查询 build_id 12345 的上传状态
```

### 3. 更新元数据

```
更新应用元数据
- 标题: My Awesome App
- 发布说明: 修复了一些 bug
```

### 4. 提交审核

```
提交审核并自动发布
```

### 5. 获取版本信息

```
查看当前 App Store 的版本信息
```

### 6. 获取本地项目版本

```
查看当前项目的版本号
```

### 7. 设置项目版本

```
将项目版本设置为 1.2.0
```

### 8. 自动增加构建号

```
帮我增加一下项目的构建号
```

## 工作流程示例

### 完整发布流程

```bash
# 1. 构建 App
xcodebuild archive ...
```

然后在 Claude 中：

```
帮我执行完整的 App Store 发布流程：
1. 增加项目构建号
2. 上传 /path/to/app.ipa 到 TestFlight
3. 更新发布说明
4. 提交审核
```

## 命令行脚本使用

项目提供了示例脚本：

```bash
# 查看版本
python -m publish_app_mcp.tools.project

# 运行工作流示例
python examples/workflow.py
```

## 项目结构

```
publish-app-mcp/
├── src/publish_app_mcp/
│   ├── server.py          # MCP Server
│   ├── models.py          # 数据模型
│   ├── config.py          # 配置
│   ├── tools/             # 工具模块
│   │   ├── upload.py      # 上传工具
│   │   ├── version.py     # 版本管理
│   │   ├── metadata.py    # 元数据
│   │   ├── review.py      # 审核
│   │   └── project.py     # 项目文件管理
│   └── stores/            # 应用商店封装
│       ├── base.py
│       ├── app_store.py
│       ├── xiaomi.py
│       └── ...
```

## 常见问题

### fastlane 未安装

确保已安装 fastlane：

```bash
brew install fastlane
# 或
gem install fastlane
```

### Xcode 命令行工具未安装

```bash
xcode-select --install
```

### 权限问题

确保 API Key 有足够权限：
- App Manager
- Developer

### 国内 Android 商店集成

目前国内商店为占位实现，欢迎贡献！
