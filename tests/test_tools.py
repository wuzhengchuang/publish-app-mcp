"""Tests for tools module"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

from publish_app_mcp.tools.upload import validate_app_format
from publish_app_mcp.models import ReleaseTrack


class TestValidateAppFormat:
    """Tests for validate_app_format"""

    def test_validate_ipa(self, tmp_path):
        """Test validating IPA file"""
        path = tmp_path / "test.ipa"
        path.touch()
        result = validate_app_format(path)
        assert result == "ipa"

    def test_validate_apk(self, tmp_path):
        """Test validating APK file"""
        path = tmp_path / "test.apk"
        path.touch()
        result = validate_app_format(path)
        assert result == "apk"

    def test_validate_aab(self, tmp_path):
        """Test validating AAB file"""
        path = tmp_path / "test.aab"
        path.touch()
        result = validate_app_format(path)
        assert result == "aab"

    def test_validate_uppercase(self, tmp_path):
        """Test validating uppercase extension"""
        path = tmp_path / "TEST.IPA"
        path.touch()
        result = validate_app_format(path)
        assert result == "ipa"

    def test_validate_unknown(self, tmp_path):
        """Test validating unknown format"""
        path = tmp_path / "test.zip"
        path.touch()
        result = validate_app_format(path)
        assert result is None

    def test_validate_no_extension(self, tmp_path):
        """Test validating file with no extension"""
        path = tmp_path / "test"
        path.touch()
        result = validate_app_format(path)
        assert result is None


class TestReleaseTrack:
    """Tests for ReleaseTrack enum"""

    def test_production(self):
        """Test production track"""
        track = ReleaseTrack.PRODUCTION
        assert track.value == "production"

    def test_beta(self):
        """Test beta track"""
        track = ReleaseTrack.BETA
        assert track.value == "beta"

    def test_alpha(self):
        """Test alpha track"""
        track = ReleaseTrack.ALPHA
        assert track.value == "alpha"

    def test_internal(self):
        """Test internal track"""
        track = ReleaseTrack.INTERNAL
        assert track.value == "internal"

    def test_from_string(self):
        """Test creating from string"""
        track = ReleaseTrack("beta")
        assert track == ReleaseTrack.BETA

    def test_invalid_string(self):
        """Test creating from invalid string"""
        with pytest.raises(ValueError):
            ReleaseTrack("invalid")
