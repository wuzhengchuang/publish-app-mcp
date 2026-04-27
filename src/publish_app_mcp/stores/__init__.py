from .base import AppStoreBase
from .app_store import AppStoreClient
from .xiaomi import XiaomiStore
from .huawei import HuaweiStore
from .oppo import OppoStore
from .vivo import VivoStore
from .samsung import SamsungStore
from .yingyongbao import YingyongbaoStore

__all__ = [
    "AppStoreBase",
    "AppStoreClient",
    "XiaomiStore",
    "HuaweiStore",
    "OppoStore",
    "VivoStore",
    "SamsungStore",
    "YingyongbaoStore",
]


def get_store(store_name: str) -> AppStoreBase:
    """获取对应的应用商店客户端"""
    stores = {
        "app_store": AppStoreClient,
        "xiaomi": XiaomiStore,
        "huawei": HuaweiStore,
        "oppo": OppoStore,
        "vivo": VivoStore,
        "samsung": SamsungStore,
        "yingyongbao": YingyongbaoStore,
    }
    store_cls = stores.get(store_name)
    if not store_cls:
        raise ValueError(f"Unsupported store: {store_name}")
    return store_cls()
