from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AppStore(str, Enum):
    """支持的应用商店枚举"""
    APP_STORE = "app_store"
    XIAOMI = "xiaomi"
    HUAWEI = "huawei"
    OPPO = "oppo"
    VIVO = "vivo"
    SAMSUNG = "samsung"
    YINGYONGBAO = "yingyongbao"


class AppType(str, Enum):
    """App 格式类型"""
    IPA = "ipa"
    AAB = "aab"
    APK = "apk"


class ReleaseTrack(str, Enum):
    """发布轨道"""
    PRODUCTION = "production"
    BETA = "beta"
    ALPHA = "alpha"
    INTERNAL = "internal"


class UploadStatus(str, Enum):
    """上传状态"""
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"


class Localization(BaseModel):
    """多语言本地化数据"""
    language: str
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    release_notes: Optional[str] = None


class AppMetadata(BaseModel):
    """应用元数据"""
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    release_notes: Optional[str] = None
    localizations: Optional[List[Localization]] = None
    screenshots: Optional[List[str]] = None
    preview_video: Optional[str] = None


class VersionInfo(BaseModel):
    """版本信息"""
    version: str
    build_number: Optional[str] = None
    upload_date: Optional[str] = None
    status: Optional[str] = None
    store: AppStore


class UploadResult(BaseModel):
    """上传结果"""
    success: bool
    store: AppStore
    build_id: Optional[str] = None
    status: UploadStatus
    message: str
    error: Optional[str] = None


class ReviewResult(BaseModel):
    """审核提交结果"""
    success: bool
    store: AppStore
    review_id: Optional[str] = None
    status: str
    message: str
