#!/usr/bin/env python3
"""上传示例脚本"""
import asyncio
from pathlib import Path
from publish_app_mcp.tools import upload_app


async def main():
    # 上传到 App Store
    result = await upload_app(
        store_name="app_store",
        file_path="/path/to/your/app.ipa",
        track="production",
    )

    print(f"Success: {result.success}")
    print(f"Status: {result.status}")
    print(f"Message: {result.message}")


if __name__ == "__main__":
    asyncio.run(main())
