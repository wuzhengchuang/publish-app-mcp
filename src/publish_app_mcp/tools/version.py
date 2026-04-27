"""版本管理工具"""
import logging
from typing import Optional

from ..models import VersionInfo
from ..stores import get_store


logger = logging.getLogger(__name__)


async def get_version_info(store_name: str) -> Optional[VersionInfo]:
    """获取版本信息"""
    store = get_store(store_name)
    return await store.get_version_info()


async def bump_version(
    store_name: str,
    version: Optional[str] = None,
    build_number: Optional[str] = None,
) -> VersionInfo:
    """增加版本号"""
    store = get_store(store_name)
    return await store.bump_version(version, build_number)


def parse_version(version_str: str) -> tuple[int, int, int]:
    """解析语义化版本号"""
    if not version_str:
        return 0, 0, 0

    parts = version_str.split(".")

    def safe_int(s: str) -> int:
        try:
            return int(s) if s else 0
        except ValueError:
            return 0

    major = safe_int(parts[0]) if len(parts) > 0 else 0
    minor = safe_int(parts[1]) if len(parts) > 1 else 0
    patch = safe_int(parts[2]) if len(parts) > 2 else 0
    return major, minor, patch


def increment_patch(version: str) -> str:
    """增加补丁版本号"""
    major, minor, patch = parse_version(version)
    return f"{major}.{minor}.{patch + 1}"


def increment_minor(version: str) -> str:
    """增加次版本号"""
    major, minor, _ = parse_version(version)
    return f"{major}.{minor + 1}.0"


def increment_major(version: str) -> str:
    """增加主版本号"""
    major, _, _ = parse_version(version)
    return f"{major + 1}.0.0"
