"""元数据管理工具"""
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from ..models import AppMetadata, Localization
from ..stores import get_store


logger = logging.getLogger(__name__)


async def update_metadata(
    store_name: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    release_notes: Optional[str] = None,
    screenshots: Optional[List[str]] = None,
    localizations: Optional[List[Dict[str, Any]]] = None,
) -> bool:
    """更新应用元数据"""
    locs = None
    if localizations:
        locs = [Localization(**loc) for loc in localizations]

    metadata = AppMetadata(
        title=title,
        description=description,
        keywords=keywords,
        release_notes=release_notes,
        screenshots=screenshots,
        localizations=locs,
    )

    store = get_store(store_name)
    return await store.update_metadata(metadata)


def load_metadata_from_file(file_path: Path) -> AppMetadata:
    """从文件加载元数据 (JSON/YAML)"""
    import json

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return AppMetadata(**data)
