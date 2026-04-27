"""Tests for version tools"""
import pytest
from publish_app_mcp.tools.version import (
    parse_version,
    increment_patch,
    increment_minor,
    increment_major,
)


class TestParseVersion:
    """Tests for parse_version"""

    def test_simple_version(self):
        """Test parsing simple version"""
        major, minor, patch = parse_version("1.0.0")
        assert major == 1
        assert minor == 0
        assert patch == 0

    def test_version_with_patch(self):
        """Test parsing version with patch"""
        major, minor, patch = parse_version("1.2.3")
        assert major == 1
        assert minor == 2
        assert patch == 3

    def test_version_without_patch(self):
        """Test parsing version without patch"""
        major, minor, patch = parse_version("1.2")
        assert major == 1
        assert minor == 2
        assert patch == 0

    def test_version_without_minor(self):
        """Test parsing version without minor"""
        major, minor, patch = parse_version("1")
        assert major == 1
        assert minor == 0
        assert patch == 0

    def test_empty_version(self):
        """Test parsing empty version"""
        major, minor, patch = parse_version("")
        assert major == 0
        assert minor == 0
        assert patch == 0


class TestIncrementPatch:
    """Tests for increment_patch"""

    def test_increment_simple(self):
        """Test incrementing patch"""
        assert increment_patch("1.0.0") == "1.0.1"

    def test_increment_with_patch(self):
        """Test incrementing existing patch"""
        assert increment_patch("1.2.3") == "1.2.4"

    def test_increment_without_patch(self):
        """Test incrementing without patch in string"""
        assert increment_patch("1.2") == "1.2.1"

    def test_increment_large_patch(self):
        """Test incrementing large patch"""
        assert increment_patch("0.0.999") == "0.0.1000"


class TestIncrementMinor:
    """Tests for increment_minor"""

    def test_increment_simple(self):
        """Test incrementing minor"""
        assert increment_minor("1.0.0") == "1.1.0"

    def test_increment_with_existing(self):
        """Test incrementing minor with existing patch"""
        assert increment_minor("1.2.3") == "1.3.0"

    def test_increment_resets_patch(self):
        """Test that patch is reset to 0"""
        result = increment_minor("1.2.999")
        assert result == "1.3.0"


class TestIncrementMajor:
    """Tests for increment_major"""

    def test_increment_simple(self):
        """Test incrementing major"""
        assert increment_major("1.0.0") == "2.0.0"

    def test_increment_with_existing(self):
        """Test incrementing major with existing minor and patch"""
        assert increment_major("1.2.3") == "2.0.0"

    def test_increment_resets_others(self):
        """Test that minor and patch are reset to 0"""
        result = increment_major("0.9.999")
        assert result == "1.0.0"


class TestVersionWorkflow:
    """Tests for complete version workflows"""

    def test_patch_then_minor_then_major(self):
        """Test incrementing patch, then minor, then major"""
        version = "1.0.0"
        version = increment_patch(version)
        assert version == "1.0.1"

        version = increment_patch(version)
        assert version == "1.0.2"

        version = increment_minor(version)
        assert version == "1.1.0"

        version = increment_major(version)
        assert version == "2.0.0"
