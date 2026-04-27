"""上传工具"""
import logging
from pathlib import Path
from typing import Optional

from ..models import ReleaseTrack, UploadResult
from ..stores import get_store


logger = logging.getLogger(__name__)


async def upload_app(
    store_name: str,
    file_path: str | Path,
    track: str = "production",
) -> UploadResult:
    """上传 App 到应用商店"""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    release_track = ReleaseTrack(track)
    store = get_store(store_name)

    logger.info(f"Uploading {file_path} to {store_name} ({track})...")
    return await store.upload_app(file_path, release_track)


def validate_app_format(file_path: Path) -> Optional[str]:
    """验证 App 格式"""
    suffix = file_path.suffix.lower()
    if suffix == ".ipa":
        return "ipa"
    elif suffix == ".aab":
        return "aab"
    elif suffix == ".apk":
        return "apk"
    return None
