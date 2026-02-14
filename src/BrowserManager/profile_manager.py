import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional


from src.directory import DirectoryManager   

from .profile_info import ProfileInfo




class ProfileManager:
    def __init__(self, app_name: str = "tweakio"):
        self.app_name = app_name
        self.directory = DirectoryManager(app_name)


    
    
    def _generate_metadata(self, platform: str, profile_id: str) -> dict:
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
    
    def create_profile(self, platform: str, profile_id: str) -> None:
        profile_dir = self.directory.get_profile_dir(platform, profile_id)

        if profile_dir.exists():
            raise ValueError(
                f"Profile '{profile_id}' already exists for platform '{platform}'"
            )

        # NOW create the directory
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

        
    def get_profile(self, platform: str, profile_id: str):
        profile_dir = self.directory.get_profile_dir(platform, profile_id)
        metadata_file = profile_dir / "metadata.json"

        if not metadata_file.exists():
            raise ValueError("Profile metadata not found.")

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        return ProfileInfo.from_metadata(metadata, self.directory)


    def list_profiles(self, platform: Optional[str] = None) -> List[str]:
        results = []

        if platform:
            platform_dir = self.directory.get_platform_dir(platform)

            if platform_dir.exists():
                results = [p.name for p in platform_dir.iterdir() if p.is_dir()]
        else:
            for plat in self.directory.platforms_dir.iterdir():

                if plat.is_dir():
                    for profile in plat.iterdir():
                        if profile.is_dir():
                            results.append(f"{plat.name}:{profile.name}")

        return results
    
    

    def activate_profile(self, platform: str, profile_id: str) -> None:
        profile_dir = self.directory.get_profile_dir(platform, profile_id)

        if not profile_dir.exists():
            raise ValueError(
                f"Profile '{profile_id}' does not exist for platform '{platform}'"
            )

        metadata_file = profile_dir / "metadata.json"

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        if not metadata.get("paths"):
            raise ValueError("Corrupted metadata file.")

        # If already active and process still alive, do nothing
        if metadata["status"]["is_active"]:
            return

        # Activate only THIS profile
        metadata["status"]["is_active"] = True
        metadata["status"]["last_active_pid"] = os.getpid()
        metadata["last_used"] = datetime.now().isoformat()

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        lock_file = profile_dir / ".lock"
        lock_file.write_text(str(os.getpid()))


    def delete_profile(self, platform: str, profile_id: str, force: bool = False) -> None:
        profile_dir = self.directory.get_profile_dir(platform, profile_id)


        if not profile_dir.exists():
            raise ValueError(f"Profile '{profile_id}' does not exist for platform '{platform}'")

        metadata_file = profile_dir / "metadata.json"

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        # Block deletion if active
        if metadata["status"]["is_active"] and not force:
            raise ValueError(
                f"Cannot delete active profile '{profile_id}'. Deactivate first or use force=True."
            )

        # Remove directory safely
        shutil.rmtree(profile_dir)

    def create_backup(self, platform: str, profile_id: str) -> None:

        profile_dir = self.directory.get_profile_dir(platform, profile_id)


        if not profile_dir.exists():
            raise ValueError("Profile does not exist.")

        metadata_file = profile_dir / "metadata.json"

        with open(metadata_file, "r") as f:
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
