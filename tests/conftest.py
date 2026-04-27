"""Pytest configuration"""
import pytest
import asyncio
from pathlib import Path


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory"""
    return tmp_path


@pytest.fixture
def sample_ipa_path(tmp_path):
    """Create a sample IPA file"""
    ipa = tmp_path / "test.ipa"
    ipa.touch()
    return ipa


@pytest.fixture
def sample_apk_path(tmp_path):
    """Create a sample APK file"""
    apk = tmp_path / "test.apk"
    apk.touch()
    return apk


@pytest.fixture
def sample_aab_path(tmp_path):
    """Create a sample AAB file"""
    aab = tmp_path / "test.aab"
    aab.touch()
    return aab
