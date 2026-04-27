from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from ..models import (
    AppStore,
    AppMetadata,
    VersionInfo,
    UploadResult,
    ReviewResult,
    UploadStatus,
    ReleaseTrack,
)


class AppStoreBase(ABC):
    """应用商店基类"""

    store_type: AppStore

    def __init__(self):
        pass

    @abstractmethod
    async def upload_app(
        self,
        file_path: Path,
        track: ReleaseTrack = ReleaseTrack.PRODUCTION,
    ) -> UploadResult:
        """上传 App"""
        pass

    @abstractmethod
    async def get_upload_status(self, build_id: str) -> UploadStatus:
        """获取上传状态"""
        pass

    @abstractmethod
    async def update_metadata(self, metadata: AppMetadata) -> bool:
        """更新元数据"""
        pass

    @abstractmethod
    async def submit_review(
        self,
        build_id: Optional[str] = None,
        auto_release: bool = False,
    ) -> ReviewResult:
        """提交审核"""
        pass

    @abstractmethod
    async def get_version_info(self) -> Optional[VersionInfo]:
        """获取版本信息"""
        pass

    @abstractmethod
    async def bump_version(
        self,
        version: Optional[str] = None,
        build_number: Optional[str] = None,
    ) -> VersionInfo:
        """增加版本号"""
        pass
