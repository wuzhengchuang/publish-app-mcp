#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .stores import get_store
from .models import ReleaseTrack


logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


app = Server("publish-app-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的 MCP 工具"""
    return [
        Tool(
            name="upload_app",
            description="上传 App 到应用商店",
            inputSchema={
                "type": "object",
                "properties": {
                    "store": {
                        "type": "string",
                        "description": "应用商店名称: app_store, xiaomi, huawei, oppo, vivo, samsung, yingyongbao",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "App 文件路径 (.ipa, .aab, .apk)",
                    },
                    "track": {
                        "type": "string",
                        "description": "发布轨道: production, beta, alpha, internal",
                        "default": "production",
                    },
                },
                "required": ["store", "file_path"],
            },
        ),
        Tool(
            name="get_upload_status",
            description="查询上传状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "store": {"type": "string", "description": "应用商店名称"},
                    "build_id": {"type": "string", "description": "构建 ID"},
                },
                "required": ["store", "build_id"],
            },
        ),
        Tool(
            name="update_metadata",
            description="更新应用元数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "store": {"type": "string", "description": "应用商店名称"},
                    "title": {"type": "string", "description": "应用标题", "optional": True},
                    "description": {"type": "string", "description": "应用描述", "optional": True},
                    "release_notes": {"type": "string", "description": "发布说明", "optional": True},
                },
                "required": ["store"],
            },
        ),
        Tool(
            name="submit_review",
            description="提交审核",
            inputSchema={
                "type": "object",
                "properties": {
                    "store": {"type": "string", "description": "应用商店名称"},
                    "build_id": {"type": "string", "description": "构建 ID", "optional": True},
                    "auto_release": {
                        "type": "boolean",
                        "description": "审核通过后自动发布",
                        "default": False,
                    },
                },
                "required": ["store"],
            },
        ),
        Tool(
            name="get_version_info",
            description="获取应用商店版本信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "store": {"type": "string", "description": "应用商店名称"},
                },
                "required": ["store"],
            },
        ),
        Tool(
            name="get_project_version",
            description="获取本地项目版本号",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "项目根目录路径",
                        "default": ".",
                    },
                },
            },
        ),
        Tool(
            name="set_project_version",
            description="设置本地项目版本号",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "项目根目录路径", "default": "."},
                    "version": {"type": "string", "description": "版本号 (如 1.0.0)"},
                    "build_number": {"type": "string", "description": "构建号 (可选)", "optional": True},
                },
                "required": ["version"],
            },
        ),
        Tool(
            name="increment_project_build",
            description="自动增加项目构建号",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "项目根目录路径", "default": "."},
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """调用 MCP 工具"""
    try:
        if name == "upload_app":
            return await _handle_upload_app(arguments)
        elif name == "get_upload_status":
            return await _handle_get_upload_status(arguments)
        elif name == "update_metadata":
            return await _handle_update_metadata(arguments)
        elif name == "submit_review":
            return await _handle_submit_review(arguments)
        elif name == "get_version_info":
            return await _handle_get_version_info(arguments)
        elif name == "get_project_version":
            return await _handle_get_project_version(arguments)
        elif name == "set_project_version":
            return await _handle_set_project_version(arguments)
        elif name == "increment_project_build":
            return await _handle_increment_project_build(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.exception(f"Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def _handle_upload_app(args: dict) -> list[TextContent]:
    store_name = args["store"]
    file_path = Path(args["file_path"])
    track = ReleaseTrack(args.get("track", "production"))

    if not file_path.exists():
        return [TextContent(type="text", text=f"File not found: {file_path}")]

    store = get_store(store_name)
    result = await store.upload_app(file_path, track)

    message = f"Upload to {store_name} {'succeeded' if result.success else 'failed'}: {result.message}"
    if result.error:
        message += f"\nError: {result.error}"

    return [TextContent(type="text", text=message)]


async def _handle_get_upload_status(args: dict) -> list[TextContent]:
    store_name = args["store"]
    build_id = args["build_id"]

    store = get_store(store_name)
    status = await store.get_upload_status(build_id)

    return [TextContent(type="text", text=f"Build {build_id} status: {status.value}")]


async def _handle_update_metadata(args: dict) -> list[TextContent]:
    store_name = args["store"]

    from .models import AppMetadata
    metadata = AppMetadata(
        title=args.get("title"),
        description=args.get("description"),
        release_notes=args.get("release_notes"),
    )

    store = get_store(store_name)
    success = await store.update_metadata(metadata)

    return [TextContent(
        type="text",
        text=f"Update metadata {'succeeded' if success else 'failed'} for {store_name}"
    )]


async def _handle_submit_review(args: dict) -> list[TextContent]:
    store_name = args["store"]
    build_id = args.get("build_id")
    auto_release = args.get("auto_release", False)

    store = get_store(store_name)
    result = await store.submit_review(build_id, auto_release)

    message = f"Submit review to {store_name}: {result.status} - {result.message}"
    return [TextContent(type="text", text=message)]


async def _handle_get_version_info(args: dict) -> list[TextContent]:
    store_name = args["store"]

    store = get_store(store_name)
    version_info = await store.get_version_info()

    if version_info:
        message = f"Version: {version_info.version}"
        if version_info.build_number:
            message += f"\nBuild: {version_info.build_number}"
        if version_info.status:
            message += f"\nStatus: {version_info.status}"
    else:
        message = "No version info available"

    return [TextContent(type="text", text=message)]


async def _handle_get_project_version(args: dict) -> list[TextContent]:
    from .tools.project import get_project_manager

    project_path = Path(args.get("project_path", ".")).resolve()
    manager = get_project_manager(project_path)

    if not manager:
        return [TextContent(type="text", text=f"Could not detect project type at {project_path}")]

    lines = [f"Project at: {project_path}"]

    if hasattr(manager, "get_version"):
        version = manager.get_version()
        if version:
            lines.append(f"Version: {version}")

    if hasattr(manager, "get_version_name"):
        version_name = manager.get_version_name()
        if version_name:
            lines.append(f"Version Name: {version_name}")

    if hasattr(manager, "get_build_number"):
        build = manager.get_build_number()
        if build:
            lines.append(f"Build Number: {build}")

    if hasattr(manager, "get_version_code"):
        version_code = manager.get_version_code()
        if version_code:
            lines.append(f"Version Code: {version_code}")

    return [TextContent(type="text", text="\n".join(lines))]


async def _handle_set_project_version(args: dict) -> list[TextContent]:
    from .tools.project import get_project_manager

    project_path = Path(args.get("project_path", ".")).resolve()
    version = args.get("version")
    build_number = args.get("build_number")

    manager = get_project_manager(project_path)
    if not manager:
        return [TextContent(type="text", text=f"Could not detect project type at {project_path}")]

    results = []

    if version:
        if hasattr(manager, "set_version"):
            if manager.set_version(version):
                results.append(f"Version set to: {version}")
            else:
                results.append(f"Failed to set version")
        elif hasattr(manager, "set_version_name"):
            if manager.set_version_name(version):
                results.append(f"Version Name set to: {version}")
            else:
                results.append(f"Failed to set version name")

    if build_number:
        if hasattr(manager, "set_build_number"):
            if manager.set_build_number(build_number):
                results.append(f"Build Number set to: {build_number}")
            else:
                results.append(f"Failed to set build number")
        elif hasattr(manager, "set_version_code"):
            try:
                code = int(build_number)
                if manager.set_version_code(code):
                    results.append(f"Version Code set to: {code}")
                else:
                    results.append(f"Failed to set version code")
            except ValueError:
                results.append(f"Invalid version code: {build_number}")

    return [TextContent(type="text", text="\n".join(results) if results else "No changes made")]


async def _handle_increment_project_build(args: dict) -> list[TextContent]:
    from .tools.project import get_project_manager

    project_path = Path(args.get("project_path", ".")).resolve()
    manager = get_project_manager(project_path)

    if not manager:
        return [TextContent(type="text", text=f"Could not detect project type at {project_path}")]

    new_build = None

    if hasattr(manager, "increment_build_number"):
        new_build = manager.increment_build_number()
        if new_build:
            return [TextContent(type="text", text=f"Build Number incremented to: {new_build}")]

    if hasattr(manager, "increment_version_code"):
        new_code = manager.increment_version_code()
        if new_code:
            return [TextContent(type="text", text=f"Version Code incremented to: {new_code}")]

    return [TextContent(type="text", text="Failed to increment build number")]


async def main():
    """启动 MCP Server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
