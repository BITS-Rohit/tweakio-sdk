from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

from BrowserManager.platform_manager import Platform


@dataclass
class ProfileInfo:
    """Data class for Profiles"""
    profile_id: str
    platform: Platform
    version: str
    created_at: str
    last_used: str

    profile_dir: Path
    session_path: Path
    fingerprint_path: Path
    cookies_path: Path
    cache_dir: Path
    backup_dir: Path
    media_dir: Path
    database_path: Path

    is_active: bool
    last_active_pid: Optional[int]

    encryption: Dict

    @classmethod
    def from_metadata(cls, metadata: dict, directory):
        platform = metadata["platform"]
        profile_id = metadata["profile_id"]

        profile_dir = directory.get_profile_dir(platform, profile_id)

        return cls(
            profile_id=profile_id,
            platform=platform,
            version=metadata["version"],
            created_at=metadata["created_at"],
            last_used=metadata["last_used"],

            profile_dir=profile_dir,
            session_path=profile_dir / "session.json",  # OK if not in DirectoryManager yet
            fingerprint_path=profile_dir / "fingerprint.pkl",
            cookies_path=profile_dir / "cookies.json",

            cache_dir=directory.get_cache_dir(platform, profile_id),
            backup_dir=directory.get_backup_dir(platform, profile_id),
            media_dir=directory.get_media_dir(platform, profile_id),
            database_path=directory.get_database_path(platform, profile_id),

            is_active=metadata["status"]["is_active"],
            last_active_pid=metadata["status"]["last_active_pid"],

            encryption=metadata.get("encryption", {})
        )
