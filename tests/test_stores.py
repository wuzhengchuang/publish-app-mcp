"""Tests for stores module"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

from publish_app_mcp.stores import get_store
from publish_app_mcp.stores.base import AppStoreBase
from publish_app_mcp.models import (
    AppStore,
    AppMetadata,
    VersionInfo,
    UploadResult,
    ReviewResult,
    UploadStatus,
    ReleaseTrack,
)


class TestGetStore:
    """Tests for get_store"""

    def test_get_app_store(self):
        """Test getting App Store client"""
        store = get_store("app_store")
        assert store.store_type == AppStore.APP_STORE

    def test_get_xiaomi(self):
        """Test getting Xiaomi client"""
        store = get_store("xiaomi")
        assert store.store_type == AppStore.XIAOMI

    def test_get_huawei(self):
        """Test getting Huawei client"""
        store = get_store("huawei")
        assert store.store_type == AppStore.HUAWEI

    def test_get_oppo(self):
        """Test getting OPPO client"""
        store = get_store("oppo")
        assert store.store_type == AppStore.OPPO

    def test_get_vivo(self):
        """Test getting vivo client"""
        store = get_store("vivo")
        assert store.store_type == AppStore.VIVO

    def test_get_samsung(self):
        """Test getting Samsung client"""
        store = get_store("samsung")
        assert store.store_type == AppStore.SAMSUNG

    def test_get_yingyongbao(self):
        """Test getting Yingyongbao client"""
        store = get_store("yingyongbao")
        assert store.store_type == AppStore.YINGYONGBAO

    def test_get_invalid_store(self):
        """Test getting invalid store"""
        with pytest.raises(ValueError):
            get_store("invalid_store")


class TestStoreBaseClass:
    """Tests for AppStoreBase"""

    class TestStore(AppStoreBase):
        """Test store implementation"""

        store_type = AppStore.APP_STORE

        async def upload_app(self, file_path, track=ReleaseTrack.PRODUCTION):
            return UploadResult(
                success=True,
                store=AppStore.APP_STORE,
                status=UploadStatus.SUCCESS,
                message="OK",
            )

        async def get_upload_status(self, build_id):
            return UploadStatus.SUCCESS

        async def update_metadata(self, metadata):
            return True

        async def submit_review(self, build_id=None, auto_release=False):
            return ReviewResult(
                success=True,
                store=AppStore.APP_STORE,
                status="submitted",
                message="OK",
            )

        async def get_version_info(self):
            return VersionInfo(
                version="1.0.0",
                store=AppStore.APP_STORE,
            )

        async def bump_version(self, version=None, build_number=None):
            return VersionInfo(
                version=version or "1.0.0",
                build_number=build_number,
                store=AppStore.APP_STORE,
            )

    @pytest.fixture
    def store(self):
        """Create a test store"""
        return self.TestStore()

    @pytest.mark.asyncio
    async def test_upload_app(self, store):
        """Test upload_app"""
        result = await store.upload_app(Path("test.ipa"))
        assert result.success is True
        assert result.status == UploadStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_get_upload_status(self, store):
        """Test get_upload_status"""
        status = await store.get_upload_status("123")
        assert status == UploadStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_update_metadata(self, store):
        """Test update_metadata"""
        meta = AppMetadata(title="Test")
        result = await store.update_metadata(meta)
        assert result is True

    @pytest.mark.asyncio
    async def test_submit_review(self, store):
        """Test submit_review"""
        result = await store.submit_review()
        assert result.success is True
        assert result.status == "submitted"

    @pytest.mark.asyncio
    async def test_get_version_info(self, store):
        """Test get_version_info"""
        info = await store.get_version_info()
        assert info is not None
        assert info.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_bump_version(self, store):
        """Test bump_version"""
        info = await store.bump_version(version="1.1.0")
        assert info.version == "1.1.0"

    @pytest.mark.asyncio
    async def test_bump_version_with_build(self, store):
        """Test bump_version with build number"""
        info = await store.bump_version(version="1.1.0", build_number="42")
        assert info.version == "1.1.0"
        assert info.build_number == "42"


class TestPlaceHolderStores:
    """Tests for placeholder stores"""

    @pytest.mark.asyncio
    async def test_xiaomi_upload(self):
        """Test Xiaomi upload (placeholder)"""
        store = get_store("xiaomi")
        result = await store.upload_app(Path("test.apk"))
        assert result.success is False
        assert "not implemented" in result.message.lower()

    @pytest.mark.asyncio
    async def test_huawei_upload(self):
        """Test Huawei upload (placeholder)"""
        store = get_store("huawei")
        result = await store.upload_app(Path("test.apk"))
        assert result.success is False

    @pytest.mark.asyncio
    async def test_oppo_upload(self):
        """Test OPPO upload (placeholder)"""
        store = get_store("oppo")
        result = await store.upload_app(Path("test.apk"))
        assert result.success is False

    @pytest.mark.asyncio
    async def test_vivo_upload(self):
        """Test vivo upload (placeholder)"""
        store = get_store("vivo")
        result = await store.upload_app(Path("test.apk"))
        assert result.success is False

    @pytest.mark.asyncio
    async def test_samsung_upload(self):
        """Test Samsung upload (placeholder)"""
        store = get_store("samsung")
        result = await store.upload_app(Path("test.apk"))
        assert result.success is False

    @pytest.mark.asyncio
    async def test_yingyongbao_upload(self):
        """Test Yingyongbao upload (placeholder)"""
        store = get_store("yingyongbao")
        result = await store.upload_app(Path("test.apk"))
        assert result.success is False
