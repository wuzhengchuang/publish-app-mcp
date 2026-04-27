"""项目版本文件管理"""
import logging
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple


logger = logging.getLogger(__name__)


class XcodeProject:
    """Xcode 项目管理"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.info_plist_path = self._find_info_plist()

    def _find_info_plist(self) -> Optional[Path]:
        """查找 Info.plist"""
        # 常见位置
        candidates = [
            self.project_path / "Info.plist",
            *list(self.project_path.glob("*/Info.plist")),
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def get_version(self) -> Optional[str]:
        """获取版本号 (CFBundleShortVersionString)"""
        if not self.info_plist_path:
            return None
        try:
            result = subprocess.run(
                ["plutil", "-extract", "CFBundleShortVersionString", "json", "-o", "-", str(self.info_plist_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                return str(data)
        except Exception as e:
            logger.warning(f"Failed to get version: {e}")
        return None

    def get_build_number(self) -> Optional[str]:
        """获取构建号 (CFBundleVersion)"""
        if not self.info_plist_path:
            return None
        try:
            result = subprocess.run(
                ["plutil", "-extract", "CFBundleVersion", "json", "-o", "-", str(self.info_plist_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                return str(data)
        except Exception as e:
            logger.warning(f"Failed to get build number: {e}")
        return None

    def set_version(self, version: str) -> bool:
        """设置版本号"""
        if not self.info_plist_path:
            return False
        try:
            subprocess.run(
                ["plutil", "-replace", "CFBundleShortVersionString", "-string", version, str(self.info_plist_path)],
                capture_output=True,
                check=True,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set version: {e}")
            return False

    def set_build_number(self, build_number: str) -> bool:
        """设置构建号"""
        if not self.info_plist_path:
            return False
        try:
            subprocess.run(
                ["plutil", "-replace", "CFBundleVersion", "-string", build_number, str(self.info_plist_path)],
                capture_output=True,
                check=True,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set build number: {e}")
            return False

    def increment_build_number(self) -> Optional[str]:
        """自动增加构建号"""
        current = self.get_build_number()
        if current is None:
            current = "1"
        try:
            new_build = str(int(current) + 1)
            if self.set_build_number(new_build):
                return new_build
        except ValueError:
            pass
        return None


class AndroidProject:
    """Android 项目管理"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.build_gradle_path = self._find_build_gradle()

    def _find_build_gradle(self) -> Optional[Path]:
        """查找 build.gradle(.kts)"""
        candidates = [
            self.project_path / "app" / "build.gradle",
            self.project_path / "app" / "build.gradle.kts",
            self.project_path / "build.gradle",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def get_version_name(self) -> Optional[str]:
        """获取 versionName"""
        if not self.build_gradle_path:
            return None
        with open(self.build_gradle_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 匹配 versionName "1.0.0" 或 versionName = "1.0.0"
        match = re.search(r'versionName\s*=?\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
        return None

    def get_version_code(self) -> Optional[int]:
        """获取 versionCode"""
        if not self.build_gradle_path:
            return None
        with open(self.build_gradle_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'versionCode\s*=?\s*(\d+)', content)
        if match:
            return int(match.group(1))
        return None

    def set_version_name(self, version_name: str) -> bool:
        """设置 versionName"""
        if not self.build_gradle_path:
            return False
        try:
            with open(self.build_gradle_path, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = re.sub(
                r'(versionName\s*=?\s*)["\'][^"\']+["\']',
                rf'\1"{version_name}"',
                content,
            )
            with open(self.build_gradle_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        except Exception as e:
            logger.error(f"Failed to set version name: {e}")
            return False

    def set_version_code(self, version_code: int) -> bool:
        """设置 versionCode"""
        if not self.build_gradle_path:
            return False
        try:
            with open(self.build_gradle_path, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = re.sub(
                r'(versionCode\s*=?\s*)\d+',
                rf'\1{version_code}',
                content,
            )
            with open(self.build_gradle_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        except Exception as e:
            logger.error(f"Failed to set version code: {e}")
            return False

    def increment_version_code(self) -> Optional[int]:
        """自动增加 versionCode"""
        current = self.get_version_code()
        if current is None:
            current = 1
        new_code = current + 1
        if self.set_version_code(new_code):
            return new_code
        return None


def detect_project_type(project_path: Path) -> Optional[str]:
    """检测项目类型"""
    # 检查 Xcode 项目
    if any(project_path.glob("*.xcodeproj")) or any(project_path.glob("*.xcworkspace")):
        return "xcode"
    # 检查 Android 项目
    if (project_path / "app" / "build.gradle").exists() or (project_path / "app" / "build.gradle.kts").exists():
        return "android"
    if (project_path / "Info.plist").exists():
        return "xcode"
    if (project_path / "build.gradle").exists():
        return "android"
    return None


def get_project_manager(project_path: Path):
    """获取项目管理器"""
    project_type = detect_project_type(project_path)
    if project_type == "xcode":
        return XcodeProject(project_path)
    elif project_type == "android":
        return AndroidProject(project_path)
    return None
