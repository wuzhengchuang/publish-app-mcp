"""审核和发布工具"""
import logging
from typing import Optional

from ..models import ReviewResult, UploadStatus
from ..stores import get_store


logger = logging.getLogger(__name__)


async def submit_review(
    store_name: str,
    build_id: Optional[str] = None,
    auto_release: bool = False,
) -> ReviewResult:
    """提交审核"""
    store = get_store(store_name)
    return await store.submit_review(build_id, auto_release)


async def get_upload_status(
    store_name: str,
    build_id: str,
) -> UploadStatus:
    """获取上传状态"""
    store = get_store(store_name)
    return await store.get_upload_status(build_id)


async def wait_for_processing(
    store_name: str,
    build_id: str,
    timeout_seconds: int = 600,
    check_interval: int = 30,
) -> UploadStatus:
    """等待处理完成"""
    import asyncio
    import time

    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        status = await get_upload_status(store_name, build_id)

        if status in (UploadStatus.SUCCESS, UploadStatus.FAILED):
            return status

        logger.info(f"Status: {status}, checking again in {check_interval}s...")
        await asyncio.sleep(check_interval)

    return UploadStatus.FAILED
