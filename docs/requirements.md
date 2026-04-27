# 需求文档：自动化上传 App 到应用商店 MCP Server

## 1. 项目概述

### 1.1 项目目标
开发一个 MCP (Model Context Protocol) Server，提供工具来自动化上传和发布 App 到各大应用商店。

### 1.2 背景
- 项目名称：publish-app-mcp
- 当前状态：全新项目，仅有 README.md
- Git 已初始化

---

## 2. 功能需求

### 2.1 核心功能

#### 2.1.1 应用商店支持
- [1] App Store (iOS/macOS)
- [ ] Google Play Store (Android)
- [1] 其他应用商店：小米，应用宝，华为，荣耀，三星，vivo，OPPO

#### 2.1.2 App 格式支持
- [1] .ipa (iOS)
- [1] .aab (Android App Bundle)
- [1] .apk (Android)

#### 2.1.3 上传功能
- [1] 上传 App 二进制文件到应用商店
- [1] 断点续传
- [1] 上传进度反馈

#### 2.1.4 版本管理
- [1] 自动读取当前版本信息
- [1] 自动增加版本号/构建号
- [1] 版本号策略配置

#### 2.1.5 元数据管理
- [1] 更新应用描述
- [1] 更新截图和预览视频
- [1] 更新关键字和分类
- [1] 多语言支持

#### 2.1.6 发布流程
- [1] 提交审核
- [1] 发布到生产环境
- [1] 分阶段发布（Phased Release）
- [1] 状态查询

### 2.2 MCP 工具列表

| 工具名称 | 描述 |
|---------|------|
| `upload_app` | 上传 App 到应用商店 |
| `get_upload_status` | 查询上传状态 |
| `update_metadata` | 更新应用元数据 |
| `submit_review` | 提交审核 |
| `get_version_info` | 获取版本信息 |

---

## 3. 技术选型

### 3.1 开发语言
- [ ] TypeScript (推荐)
- [ ] JavaScript
- [1] Python
- [ ] 其他：____

### 3.2 核心依赖

#### App Store 相关
- `fastlane` (deliver, pilot)
- `appstoreconnect-api`

#### Google Play 相关
- `fastlane` (supply)
- `google-play-developer-api`

#### MCP 相关
- `@modelcontextprotocol/sdk`

---

## 4. 项目结构

```
publish-app-mcp/
├── docs/                    # 文档目录
│   ├── requirements.md      # 需求文档（本文件）
│   ├── api.md              # API 文档
│   └── usage.md            # 使用指南
├── src/
│   ├── tools/              # MCP 工具实现
│   ├── services/           # 应用商店服务封装
│   ├── config/             # 配置管理
│   └── index.ts            # MCP Server 入口
├── package.json
├── tsconfig.json
└── README.md
```

---

## 5. 配置需求

### 5.1 认证配置
- App Store Connect API Key
- Google Play Service Account JSON

### 5.2 项目配置
- App 基本信息（Bundle ID / Package Name）
- 默认发布轨道

---

## 6. 后续步骤

1. 确认需求文档内容
2. 初始化项目结构和技术栈
3. 实现核心上传功能
4. 实现 MCP 工具封装
5. 测试和文档完善
