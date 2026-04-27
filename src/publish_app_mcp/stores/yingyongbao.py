import logging
from pathlib import Path
from typing import Optional

from ..config import config
from ..models import (
    AppStore,
    AppMetadata,
    VersionInfo,
    UploadResult,
    ReviewResult,
    UploadStatus,
    ReleaseTrack,
)
from .base import AppStoreBase


logger = logging.getLogger(__name__)


class YingyongbaoStore(AppStoreBase):
    """应用宝"""

    store_type = AppStore.YINGYONGBAO

    def __init__(self):
        super().__init__()
        self.config = config.yingyongbao

    async def upload_app(
        self,
        file_path: Path,
        track: ReleaseTrack = ReleaseTrack.PRODUCTION,
    ) -> UploadResult:
        logger.info(f"Uploading {file_path} to Yingyongbao...")
        return UploadResult(
            success=False,
            store=AppStore.YINGYONGBAO,
            status=UploadStatus.FAILED,
            message="Yingyongbao not implemented yet",
        )

    async def get_upload_status(self, build_id: str) -> UploadStatus:
        return UploadStatus.PENDING

    async def update_metadata(self, metadata: AppMetadata) -> bool:
        return False

    async def submit_review(
        self,
        build_id: Optional[str] = None,
        auto_release: bool = False,
    ) -> ReviewResult:
        return ReviewResult(
            success=False,
            store=AppStore.YINGYONGBAO,
            status="not_implemented",
            message="Yingyongbao not implemented yet",
        )

    async def get_version_info(self) -> Optional[VersionInfo]:
        return None

    async def bump_version(
        self,
        version: Optional[str] = None,
        build_number: Optional[str] = None,
    ) -> VersionInfo:
        return VersionInfo(
            version=version or "1.0.0",
            store=AppStore.YINGYONGBAO,
        )
