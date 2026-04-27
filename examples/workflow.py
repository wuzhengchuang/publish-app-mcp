#!/usr/bin/env python3
"""完整发布工作流示例"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from publish_app_mcp.tools import (
    upload_app,
    get_upload_status,
    update_metadata,
    submit_review,
    wait_for_processing,
    get_project_manager,
    increment_patch,
)
from publish_app_mcp.models import ReleaseTrack, AppMetadata


async def main():
    """完整发布流程"""
    print("=" * 60)
    print("App 自动发布工作流")
    print("=" * 60)

    project_path = Path(".")
    app_path = None  # 需要设置你的 .ipa/.aab/.apk 路径

    # 1. 检测项目
    print("\n[1/6] 检测项目...")
    manager = get_project_manager(project_path)
    if not manager:
        print("  ✗ 无法检测项目类型")
        return

    print("  ✓ 项目检测成功")

    # 2. 获取当前版本
    print("\n[2/6] 获取当前版本...")
    current_version = None
    if hasattr(manager, "get_version"):
        current_version = manager.get_version()
    elif hasattr(manager, "get_version_name"):
        current_version = manager.get_version_name()

    if current_version:
        print(f"  当前版本: {current_version}")

        # 3. 增加补丁版本号
        print("\n[3/6] 增加版本号...")
        new_version = increment_patch(current_version)
        print(f"  新版本: {new_version}")

        if hasattr(manager, "set_version"):
            manager.set_version(new_version)
        elif hasattr(manager, "set_version_name"):
            manager.set_version_name(new_version)

        # 4. 增加构建号
        if hasattr(manager, "increment_build_number"):
            new_build = manager.increment_build_number()
            if new_build:
                print(f"  新构建号: {new_build}")
        elif hasattr(manager, "increment_version_code"):
            new_code = manager.increment_version_code()
            if new_code:
                print(f"  新 Version Code: {new_code}")
    else:
        print("  ⚠ 无法获取版本号")

    # 5. 构建 (这里需要你自己执行)
    print("\n[4/6] 请构建你的 App...")
    print("  (这里需要执行你的构建命令)")

    if not app_path or not Path(app_path).exists():
        print("\n  ⚠ 请设置 app_path 变量后继续")
        return

    # 6. 上传
    print("\n[5/6] 上传 App...")
    result = await upload_app(
        store_name="app_store",
        file_path=app_path,
        track=ReleaseTrack.BETA,
    )

    if result.success:
        print(f"  ✓ {result.message}")

        # 更新元数据
        print("\n[6/6] 更新元数据...")
        metadata = AppMetadata(
            release_notes="Bug fixes and improvements",
        )
        updated = await update_metadata("app_store", metadata)
        if updated:
            print("  ✓ 元数据更新成功")

        # 提交审核
        print("\n提交审核 (可选)...")
        answer = input("  是否提交审核? (y/n): ")
        if answer.lower() == "y":
            review_result = await submit_review(
                store_name="app_store",
                auto_release=True,
            )
            print(f"  {review_result.message}")
    else:
        print(f"  ✗ {result.message}")
        if result.error:
            print(f"  {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
