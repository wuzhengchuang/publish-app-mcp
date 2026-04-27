import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class AppStoreConfig(BaseSettings):
    """App Store 配置"""
    key_id: Optional[str] = None
    issuer_id: Optional[str] = None
    private_key_path: Optional[str] = None
    bundle_id: Optional[str] = None

    model_config = {
        "env_prefix": "APP_STORE_",
    }


class XiaomiConfig(BaseSettings):
    """小米开放平台配置"""
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    package_name: Optional[str] = None

    model_config = {
        "env_prefix": "XIAOMI_",
    }


class HuaweiConfig(BaseSettings):
    """华为应用市场配置"""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    package_name: Optional[str] = None

    model_config = {
        "env_prefix": "HUAWEI_",
    }


class OppoConfig(BaseSettings):
    """OPPO 开放平台配置"""
    app_key: Optional[str] = None
    app_secret: Optional[str] = None
    package_name: Optional[str] = None

    model_config = {
        "env_prefix": "OPPO_",
    }


class VivoConfig(BaseSettings):
    """vivo 开放平台配置"""
    app_id: Optional[str] = None
    app_key: Optional[str] = None
    package_name: Optional[str] = None

    model_config = {
        "env_prefix": "VIVO_",
    }


class SamsungConfig(BaseSettings):
    """三星应用商店配置"""
    service_account_id: Optional[str] = None
    private_key_path: Optional[str] = None
    package_name: Optional[str] = None

    model_config = {
        "env_prefix": "SAMSUNG_",
    }


class YingyongbaoConfig(BaseSettings):
    """应用宝配置"""
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    package_name: Optional[str] = None

    model_config = {
        "env_prefix": "YYB_",
    }


class Config:
    """全局配置管理"""

    def __init__(self):
        self.app_store = AppStoreConfig()
        self.xiaomi = XiaomiConfig()
        self.huawei = HuaweiConfig()
        self.oppo = OppoConfig()
        self.vivo = VivoConfig()
        self.samsung = SamsungConfig()
        self.yingyongbao = YingyongbaoConfig()


config = Config()
