"""Tests for models module"""
import pytest
from publish_app_mcp.models import (
    AppStore,
    AppType,
    ReleaseTrack,
    UploadStatus,
    Localization,
    AppMetadata,
    VersionInfo,
    UploadResult,
    ReviewResult,
)


class TestAppStore:
    """Tests for AppStore enum"""

    def test_has_all_stores(self):
        """Test that all stores are present"""
        assert AppStore.APP_STORE.value == "app_store"
        assert AppStore.XIAOMI.value == "xiaomi"
        assert AppStore.HUAWEI.value == "huawei"
        assert AppStore.OPPO.value == "oppo"
        assert AppStore.VIVO.value == "vivo"
        assert AppStore.SAMSUNG.value == "samsung"
        assert AppStore.YINGYONGBAO.value == "yingyongbao"


class TestAppType:
    """Tests for AppType enum"""

    def test_has_all_types(self):
        """Test that all types are present"""
        assert AppType.IPA.value == "ipa"
        assert AppType.AAB.value == "aab"
        assert AppType.APK.value == "apk"


class TestReleaseTrack:
    """Tests for ReleaseTrack enum"""

    def test_has_all_tracks(self):
        """Test that all tracks are present"""
        assert ReleaseTrack.PRODUCTION.value == "production"
        assert ReleaseTrack.BETA.value == "beta"
        assert ReleaseTrack.ALPHA.value == "alpha"
        assert ReleaseTrack.INTERNAL.value == "internal"


class TestUploadStatus:
    """Tests for UploadStatus enum"""

    def test_has_all_statuses(self):
        """Test that all statuses are present"""
        assert UploadStatus.PENDING.value == "pending"
        assert UploadStatus.UPLOADING.value == "uploading"
        assert UploadStatus.PROCESSING.value == "processing"
        assert UploadStatus.SUCCESS.value == "success"
        assert UploadStatus.FAILED.value == "failed"


class TestLocalization:
    """Tests for Localization model"""

    def test_create_simple(self):
        """Test creating a simple localization"""
        loc = Localization(language="zh-Hans")
        assert loc.language == "zh-Hans"

    def test_create_complete(self):
        """Test creating a complete localization"""
        loc = Localization(
            language="zh-Hans",
            title="我的应用",
            description="这是一个很棒的应用",
            keywords=["效率", "工具"],
            release_notes="修复了一些 bug",
        )
        assert loc.language == "zh-Hans"
        assert loc.title == "我的应用"
        assert loc.description == "这是一个很棒的应用"
        assert loc.keywords == ["效率", "工具"]
        assert loc.release_notes == "修复了一些 bug"


class TestAppMetadata:
    """Tests for AppMetadata model"""

    def test_create_empty(self):
        """Test creating empty metadata"""
        meta = AppMetadata()
        assert meta.title is None
        assert meta.description is None
        assert meta.keywords is None
        assert meta.release_notes is None
        assert meta.localizations is None
        assert meta.screenshots is None
        assert meta.preview_video is None

    def test_create_with_title(self):
        """Test creating metadata with title"""
        meta = AppMetadata(title="My Awesome App")
        assert meta.title == "My Awesome App"

    def test_create_with_release_notes(self):
        """Test creating metadata with release notes"""
        meta = AppMetadata(release_notes="Bug fixes and improvements")
        assert meta.release_notes == "Bug fixes and improvements"

    def test_create_with_localizations(self):
        """Test creating metadata with localizations"""
        loc1 = Localization(language="en-US", title="My App")
        loc2 = Localization(language="zh-Hans", title="我的应用")
        meta = AppMetadata(localizations=[loc1, loc2])
        assert len(meta.localizations) == 2


class TestVersionInfo:
    """Tests for VersionInfo model"""

    def test_create_simple(self):
        """Test creating simple version info"""
        info = VersionInfo(version="1.0.0", store=AppStore.APP_STORE)
        assert info.version == "1.0.0"
        assert info.store == AppStore.APP_STORE
        assert info.build_number is None
        assert info.upload_date is None
        assert info.status is None

    def test_create_complete(self):
        """Test creating complete version info"""
        info = VersionInfo(
            version="1.2.3",
            build_number="456",
            upload_date="2024-01-15",
            status="ready",
            store=AppStore.HUAWEI,
        )
        assert info.version == "1.2.3"
        assert info.build_number == "456"
        assert info.upload_date == "2024-01-15"
        assert info.status == "ready"
        assert info.store == AppStore.HUAWEI


class TestUploadResult:
    """Tests for UploadResult model"""

    def test_create_success(self):
        """Test creating a successful upload result"""
        result = UploadResult(
            success=True,
            store=AppStore.APP_STORE,
            build_id="12345",
            status=UploadStatus.SUCCESS,
            message="Upload completed",
        )
        assert result.success is True
        assert result.store == AppStore.APP_STORE
        assert result.build_id == "12345"
        assert result.status == UploadStatus.SUCCESS
        assert result.message == "Upload completed"
        assert result.error is None

    def test_create_failure(self):
        """Test creating a failed upload result"""
        result = UploadResult(
            success=False,
            store=AppStore.XIAOMI,
            status=UploadStatus.FAILED,
            message="Upload failed",
            error="Connection timeout",
        )
        assert result.success is False
        assert result.store == AppStore.XIAOMI
        assert result.status == UploadStatus.FAILED
        assert result.error == "Connection timeout"


class TestReviewResult:
    """Tests for ReviewResult model"""

    def test_create_submitted(self):
        """Test creating a submitted review result"""
        result = ReviewResult(
            success=True,
            store=AppStore.APP_STORE,
            review_id="rev-123",
            status="submitted",
            message="Submitted for review",
        )
        assert result.success is True
        assert result.store == AppStore.APP_STORE
        assert result.review_id == "rev-123"
        assert result.status == "submitted"
        assert result.message == "Submitted for review"

    def test_create_failed(self):
        """Test creating a failed review result"""
        result = ReviewResult(
            success=False,
            store=AppStore.HUAWEI,
            status="failed",
            message="Rejected",
        )
        assert result.success is False
        assert result.status == "failed"
        assert result.review_id is None
