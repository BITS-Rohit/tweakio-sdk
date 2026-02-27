import json
import os
import shutil
import signal
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

from directory import DirectoryManager
from src.BrowserManager.camoufox_browser import CamoufoxBrowser
from src.BrowserManager.platform_manager import Platform
from src.BrowserManager.profile_info import ProfileInfo


class ProfileManager:
    """Manager/Entry point for login & profiles creation.
    """

    # p_count is runtime only & class variable
    p_count: int = 0

    def __init__(self, app_name: str = "tweakio"):
        self.app_name = app_name
        self.directory = DirectoryManager(app_name)

    def _generate_metadata(self, platform: Platform, profile_id: str) -> dict:
        now = datetime.now().isoformat()

        return {
            "profile_id": profile_id,
            "platform": platform,
            "version": "0.1.6",
            "created_at": now,
            "last_used": now,
            "paths": {
                "profile_dir": str(self.directory.get_profile_dir(platform, profile_id)),

                "session_file": "session.json",
                "fingerprint_file": "fingerprint.pkl",
                "cookies_file": "cookies.json",
                "cache_dir": "cache",
                "backup_dir": "backups",
                "media_dir": "media",
                "media_images": "media/images",
                "media_videos": "media/videos",
                "media_voice": "media/voice",
                "database_file": "messages.db",
                "media_documents": "media/documents"
            },

            "backup": {
                "enabled": True,
                "max_backups": 10
            },
            "encryption": {},

            "status": {
                "is_active": False,
                "last_active_pid": None,
                "lock_file": ".lock"
            }
        }

    @classmethod
    def __inc__(cls):
        cls.p_count += 1

    @classmethod
    def __dec__(cls):
        if cls.p_count > 0:
            cls.p_count -= 1

    @classmethod
    def __p_count__(cls):
        return cls.p_count

    def create_profile(self, platform: Platform, profile_id: str) -> ProfileInfo:
        """
        creates if not exists else return back exists one
        """
        profile_dir = self.directory.get_profile_dir(platform, profile_id)

        # If already exists → return loaded profile
        if profile_dir.exists():
            return self.get_profile(platform, profile_id)

        # Create directory structure
        profile_dir.mkdir(parents=True, exist_ok=True)

        self.directory.get_cache_dir(platform, profile_id)
        self.directory.get_backup_dir(platform, profile_id)
        self.directory.get_media_images_dir(platform, profile_id)
        self.directory.get_media_videos_dir(platform, profile_id)
        self.directory.get_media_voice_dir(platform, profile_id)
        self.directory.get_media_documents_dir(platform, profile_id)

        (profile_dir / "session.json").write_text("{}")
        (profile_dir / "cookies.json").write_text("{}")
        (profile_dir / "fingerprint.pkl").write_bytes(b"")

        metadata = self._generate_metadata(platform, profile_id)

        with open(profile_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        return ProfileInfo.from_metadata(metadata, self.directory)

    def get_profile(self, platform: Platform, profile_id: str) -> ProfileInfo:
        """Returns profile info"""
        profile_dir = self.directory.get_profile_dir(platform, profile_id)
        metadata_file = profile_dir / "metadata.json"

        if not metadata_file.exists():
            raise ValueError("Profile metadata not found.")

        with open(metadata_file) as f:  # default in read mode
            metadata = json.load(f)

        return ProfileInfo.from_metadata(metadata, self.directory)

    def is_profile_exists(self, platform: Platform, profile_id: str) -> bool:
        """Checks if profile exists or not."""
        platform_dir = self.directory.get_platform_dir(platform)

        if not platform_dir.exists():
            return False

        profile_path = platform_dir / profile_id
        return profile_path.exists() and profile_path.is_dir()

    def list_profiles(self, platform: Optional[Platform] = None) -> Dict[str, List[str]]:
        """
        If platform is provided -> returns {platform: [profiles]}
        If not provided -> returns {platform1: [...], platform2: [...]}
        """
        # converted to dict for more structured, can be used by other codebase
        results: Dict[str, List[str]] = {}

        if platform:
            platform_dir = self.directory.get_platform_dir(platform)

            if platform_dir.exists():
                results[platform] = [
                    p.name for p in platform_dir.iterdir() if p.is_dir()
                ]
        else:
            for plat in self.directory.platforms_dir.iterdir():
                if plat.is_dir():
                    results[plat.name] = [
                        profile.name
                        for profile in plat.iterdir()
                        if profile.is_dir()
                    ]

        return results

    @staticmethod
    def is_pid_alive(pid: int) -> bool:
        if not pid or pid <= 0:
            return False
        try:
            os.kill(pid, 0)  # works on Linux, macOS, Windows
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        else:
            return True


    async def close_profile(self, platform: Platform, profile_id: str, force: bool = False) -> None:
        profile_dir = self.directory.get_profile_dir(platform, profile_id)
        metadata_file = profile_dir / "metadata.json"
        lock_file = profile_dir / ".lock"

        if not metadata_file.exists():
            raise ValueError("Profile metadata not found.")

        with open(metadata_file) as f:
            data = json.load(f)

        if not data["status"]["is_active"]:
            return

        pid = data["status"].get("last_active_pid")

        # Try close via browser layer
        if pid:
            closed = await CamoufoxBrowser.close_browser_by_pid(pid)

            if not closed:
                # If still running and force enabled → kill
                if force and ProfileManager.is_pid_alive(pid):
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                elif ProfileManager.is_pid_alive(pid):
                    raise RuntimeError(
                        f"Browser process {pid} still running. Use force=True to terminate."
                    )

        #  Mark inactive
        data["status"]["is_active"] = False
        data["status"]["last_active_pid"] = None

        with open(metadata_file, "w") as f:
            json.dump(data, f, indent=4)

        # Remove lock file
        if lock_file.exists():
            lock_file.unlink()

        ProfileManager.__dec__()

    def activate_profile(self, platform: Platform, profile_id: str, browser_obj: CamoufoxBrowser) -> None:
        """
        Activates a profile. Raises error if already active with a live PID.
        """

        profile_dir = self.directory.get_profile_dir(platform, profile_id)

        if not profile_dir.exists():
            raise ValueError(
                f"Profile '{profile_id}' does not exist for platform '{platform}'"
            )

        metadata_file = profile_dir / "metadata.json"

        with open(metadata_file) as f:
            metadata = json.load(f)

        if not metadata.get("paths"):
            raise ValueError("Corrupted metadata file.")

        lock_file = profile_dir / ".lock"

        # ----- Active Check -----
        if metadata["status"]["is_active"]:
            pid = metadata["status"]["last_active_pid"]

            if pid and ProfileManager.is_pid_alive(pid):
                raise RuntimeError("Profile already active.")

            # Stale session cleanup
            metadata["status"]["is_active"] = False
            metadata["status"]["last_active_pid"] = None

            if lock_file.exists():
                lock_file.unlink()

        # ----- Headless override for multi-profile runtime -----
        if ProfileManager.__p_count__() > 1:
            browser_obj.config.headless = True

        ProfileManager.__inc__()

        # ----- Activate -----
        metadata["status"]["is_active"] = True
        metadata["status"]["last_active_pid"] = os.getpid()
        metadata["last_used"] = datetime.now().isoformat()

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        lock_file.write_text(str(os.getpid()))

        # TODO: Add distributed / cross-process registry validation (future enhancement)

    def delete_profile(self, platform: Platform, profile_id: str, force: bool = False) -> None:
        profile_dir = self.directory.get_profile_dir(platform, profile_id)

        if not profile_dir.exists():
            raise ValueError(f"Profile '{profile_id}' does not exist for platform '{platform}'")

        metadata_file = profile_dir / "metadata.json"

        with open(metadata_file) as f:
            metadata = json.load(f)

        # Block deletion if active
        if metadata["status"]["is_active"] and not force:
            raise ValueError(
                f"Cannot delete active profile '{profile_id}'. Deactivate first or use force=True."
            )

        # Remove directory safely
        shutil.rmtree(profile_dir)

    def create_backup(self, platform: Platform, profile_id: str) -> None:

        profile_dir = self.directory.get_profile_dir(platform, profile_id)

        if not profile_dir.exists():
            raise ValueError("Profile does not exist.")

        metadata_file = profile_dir / "metadata.json"

        with open(metadata_file) as f:
            metadata = json.load(f)

        if not metadata["backup"]["enabled"]:
            return

        backup_dir = profile_dir / "backups"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_file = backup_dir / f"session_{timestamp}.json"

        session_file = profile_dir / "session.json"

        shutil.copy2(session_file, backup_file)

        self._prune_backups(profile_dir, metadata["backup"]["max_backups"])

    def _prune_backups(self, profile_dir: Path, max_backups: int) -> None:
        backup_dir = profile_dir / "backups"

        backups = sorted(
            backup_dir.glob("session_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        for old_backup in backups[max_backups:]:
            old_backup.unlink()
