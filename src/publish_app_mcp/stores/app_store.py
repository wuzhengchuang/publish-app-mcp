import logging
import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from tempfile import NamedTemporaryFile, TemporaryDirectory

from ..config import config
from ..models import (
    AppStore,
    AppMetadata,
    VersionInfo,
    UploadResult,
    ReviewResult,
    UploadStatus,
    ReleaseTrack,
)
from .base import AppStoreBase


logger = logging.getLogger(__name__)


class AppStoreClient(AppStoreBase):
    """App Store 客户端"""

    store_type = AppStore.APP_STORE

    def __init__(self):
        super().__init__()
        self.config = config.app_store

    async def upload_app(
        self,
        file_path: Path,
        track: ReleaseTrack = ReleaseTrack.PRODUCTION,
    ) -> UploadResult:
        """上传 App 到 App Store"""
        try:
            logger.info(f"Uploading {file_path} to App Store...")

            # 验证文件
            if not file_path.exists():
                return UploadResult(
                    success=False,
                    store=AppStore.APP_STORE,
                    status=UploadStatus.FAILED,
                    message=f"File not found: {file_path}",
                )

            # 验证工具是否可用
            pilot_available = await self._check_tool_available("xcrun", "pilot")
            altool_available = await self._check_tool_available("xcrun", "altool")

            if pilot_available:
                logger.info("Using pilot for upload")
                return await self._upload_with_pilot(file_path, track)
            elif altool_available:
                logger.info("Using altool for upload")
                return await self._upload_with_altool(file_path, track)
            else:
                return UploadResult(
                    success=False,
                    store=AppStore.APP_STORE,
                    status=UploadStatus.FAILED,
                    message="Neither pilot nor altool available. Please install Xcode command line tools.",
                )

        except Exception as e:
            logger.exception(f"Upload failed: {e}")
            return UploadResult(
                success=False,
                store=AppStore.APP_STORE,
                status=UploadStatus.FAILED,
                message="Upload failed with exception",
                error=str(e),
            )

    async def _upload_with_pilot(
        self,
        file_path: Path,
        track: ReleaseTrack,
    ) -> UploadResult:
        """使用 fastlane pilot 上传"""
        cmd = [
            "xcrun", "pilot",
            "upload",
            "--ipa", str(file_path),
        ]

        if self.config.private_key_path and Path(self.config.private_key_path).exists():
            cmd.extend(["--api_key_path", str(self.config.private_key_path)])
        if self.config.key_id:
            cmd.extend(["--api_key", self.config.key_id])
        if self.config.issuer_id:
            cmd.extend(["--api_issuer", self.config.issuer_id])
        if self.config.bundle_id:
            cmd.extend(["--app_identifier", self.config.bundle_id])

        if track == ReleaseTrack.BETA:
            cmd.extend(["--changelog", "Beta release"])
        elif track == ReleaseTrack.ALPHA:
            cmd.extend(["--changelog", "Alpha release"])

        result = await self._run_command(cmd)

        if result.returncode == 0:
            return UploadResult(
                success=True,
                store=AppStore.APP_STORE,
                status=UploadStatus.SUCCESS,
                message="Upload completed successfully",
            )
        else:
            return UploadResult(
                success=False,
                store=AppStore.APP_STORE,
                status=UploadStatus.FAILED,
                message="Upload failed",
                error=result.stderr,
            )

    async def _upload_with_altool(
        self,
        file_path: Path,
        track: ReleaseTrack,
    ) -> UploadResult:
        """使用 altool 上传"""
        cmd = [
            "xcrun", "altool",
            "--upload-app",
            "--file", str(file_path),
            "--type", "ios",
        ]

        if self.config.private_key_path and Path(self.config.private_key_path).exists():
            cmd.extend([
                "--apiKey", self.config.key_id or "",
                "--apiIssuer", self.config.issuer_id or "",
            ])

        result = await self._run_command(cmd)

        if result.returncode == 0:
            return UploadResult(
                success=True,
                store=AppStore.APP_STORE,
                status=UploadStatus.SUCCESS,
                message="Upload completed successfully",
            )
        else:
            return UploadResult(
                success=False,
                store=AppStore.APP_STORE,
                status=UploadStatus.FAILED,
                message="Upload failed",
                error=result.stderr,
            )

    async def get_upload_status(self, build_id: str) -> UploadStatus:
        """获取上传状态"""
        logger.info(f"Getting status for build {build_id}")

        # 可以使用 fastlane pilot or api to get status
        if await self._check_tool_available("xcrun", "pilot"):
            cmd = [
                "xcrun", "pilot",
                "builds",
            ]
            if self.config.private_key_path and Path(self.config.private_key_path).exists():
                cmd.extend(["--api_key_path", str(self.config.private_key_path)])
            if self.config.bundle_id:
                cmd.extend(["--app_identifier", self.config.bundle_id])

            result = await self._run_command(cmd)
            if result.returncode == 0:
                # 解析输出查找 build_id 状态
                if build_id in result.stdout:
                    return UploadStatus.PROCESSING
            return UploadStatus.PROCESSING

        return UploadStatus.PROCESSING

    async def update_metadata(self, metadata: AppMetadata) -> bool:
        """更新元数据使用 fastlane deliver"""
        try:
            logger.info("Updating metadata...")

            if not await self._check_tool_available("fastlane", "deliver"):
                logger.warning("deliver not available, skipping metadata update")
                return False

            with TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                metadata_path = temp_path / "metadata"
                metadata_path.mkdir()

                # 创建元数据文件
                if metadata.release_notes:
                    en_us_path = metadata_path / "en-US"
                    en_us_path.mkdir(exist_ok=True)
                    release_notes_path = en_us_path / "release_notes.txt"
                    release_notes_path.write_text(metadata.release_notes, encoding="utf-8")

                cmd = [
                    "fastlane", "deliver",
                    "--force",
                    "--skip_binary_upload",
                    "--skip_app_version_update",
                    "--metadata_path", str(metadata_path),
                ]

                if self.config.private_key_path and Path(self.config.private_key_path).exists():
                    cmd.extend(["--api_key_path", str(self.config.private_key_path)])
                if self.config.bundle_id:
                    cmd.extend(["--app_identifier", self.config.bundle_id])

                result = await self._run_command(cmd)
                return result.returncode == 0

        except Exception as e:
            logger.exception(f"Update metadata failed: {e}")
            return False

    async def submit_review(
        self,
        build_id: Optional[str] = None,
        auto_release: bool = False,
    ) -> ReviewResult:
        """提交审核"""
        try:
            logger.info("Submitting for review...")

            cmd = [
                "fastlane", "deliver",
                "--force",
                "--skip_binary_upload",
                "--submit_for_review",
            ]

            if auto_release:
                cmd.append("--automatic_release")

            if self.config.private_key_path and Path(self.config.private_key_path).exists():
                cmd.extend(["--api_key_path", str(self.config.private_key_path)])
            if self.config.bundle_id:
                cmd.extend(["--app_identifier", self.config.bundle_id])

            result = await self._run_command(cmd)

            if result.returncode == 0:
                return ReviewResult(
                    success=True,
                    store=AppStore.APP_STORE,
                    status="submitted",
                    message="Submitted for review",
                )
            else:
                return ReviewResult(
                    success=False,
                    store=AppStore.APP_STORE,
                    status="failed",
                    message=result.stderr or "Submission failed",
                )
        except Exception as e:
            logger.exception(f"Submit review failed: {e}")
            return ReviewResult(
                success=False,
                store=AppStore.APP_STORE,
                status="failed",
                message=str(e),
            )

    async def get_version_info(self) -> Optional[VersionInfo]:
        """获取版本信息"""
        logger.info("Getting version info...")

        if await self._check_tool_available("xcrun", "pilot"):
            cmd = [
                "xcrun", "pilot",
                "builds",
                "--limit", "1",
            ]
            if self.config.private_key_path and Path(self.config.private_key_path).exists():
                cmd.extend(["--api_key_path", str(self.config.private_key_path)])
            if self.config.bundle_id:
                cmd.extend(["--app_identifier", self.config.bundle_id])

            result = await self._run_command(cmd)
            if result.returncode == 0:
                # 简单解析输出
                lines = result.stdout.splitlines()
                if len(lines) > 1:
                    return VersionInfo(
                        version="latest",
                        build_number=None,
                        store=AppStore.APP_STORE,
                        status="available",
                    )

        return None

    async def bump_version(
        self,
        version: Optional[str] = None,
        build_number: Optional[str] = None,
    ) -> VersionInfo:
        """增加版本号 (在应用商店侧不可直接修改，此功能主要用于本地管理)"""
        logger.info("Bumping version...")

        # 对于 App Store，我们不直接修改远程版本
        # 这里主要用于本地项目版本管理
        return VersionInfo(
            version=version or "1.0.0",
            build_number=build_number or "1",
            store=AppStore.APP_STORE,
        )

    async def _check_tool_available(self, *cmd: str) -> bool:
        """检查工具是否可用"""
        try:
            tool_path = shutil.which(cmd[0])
            if not tool_path:
                return False

            if len(cmd) > 1:
                # 检查子命令
                proc = await asyncio.create_subprocess_exec(
                    cmd[0], "--help",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                await proc.wait()
                return proc.returncode == 0

            return True
        except Exception:
            return False

    async def _run_command(self, cmd: list[str]) -> subprocess.CompletedProcess:
        """运行 shell 命令"""
        logger.debug(f"Running command: {' '.join(cmd)}")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        stdout_str = stdout.decode('utf-8') if stdout else ''
        stderr_str = stderr.decode('utf-8') if stderr else ''

        if stdout_str:
            logger.debug(f"stdout: {stdout_str}")
        if stderr_str and proc.returncode != 0:
            logger.error(f"stderr: {stderr_str}")

        return subprocess.CompletedProcess(
            cmd,
            proc.returncode,
            stdout_str,
            stderr_str,
        )
