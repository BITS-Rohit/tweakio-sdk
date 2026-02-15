from pathlib import Path
from platformdirs import PlatformDirs


class DirectoryManager:
    """
    Centralized directory handler for tweakio.

    Handles:
    - Root data directory
    - Cache directory
    - Log directory
    - Platform-level directories
    - Profile-level directories

    This class is profile-aware and designed to support
    multi-account isolation.
    """

    def __init__(self, app_name: str = "tweakio"):
        self.dirs = PlatformDirs(
            appname=app_name,
            appauthor="Rohit"
        )

        self.root_dir = Path(self.dirs.user_data_dir)
        self.cache_dir = Path(self.dirs.user_cache_dir)
        self.log_dir = Path(self.dirs.user_log_dir)

        self.platforms_dir = self.root_dir / "platforms"

        self._ensure_base_dirs()

    # -------------------------------------------------
    # Base directories
    # -------------------------------------------------

    def _ensure_base_dirs(self):
        for d in [
            self.root_dir,
            self.cache_dir,
            self.log_dir,
            self.platforms_dir
        ]:
            d.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Platform-level
    # -------------------------------------------------

    def get_platform_dir(self, platform: str) -> Path:
        """
        Returns platform directory (e.g. platforms/whatsapp)
        """
        path = self.platforms_dir / platform.lower()
        path.mkdir(parents=True, exist_ok=True)
        return path

    # -------------------------------------------------
    # Profile-level
    # -------------------------------------------------

    def get_profile_dir(self, platform: str, profile_id: str) -> Path:
        """
        Returns profile directory for given platform + profile.
        """
        path = self.get_platform_dir(platform) / profile_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_database_path(self, platform: str, profile_id: str) -> Path:
        """
        Returns per-profile database path.
        """
        return self.get_profile_dir(platform, profile_id) / "messages.db"

    def get_cache_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_profile_dir(platform, profile_id) / "cache"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_backup_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_profile_dir(platform, profile_id) / "backups"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_media_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_profile_dir(platform, profile_id) / "media"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_media_images_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_media_dir(platform, profile_id) / "images"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_media_videos_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_media_dir(platform, profile_id) / "videos"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_media_voice_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_media_dir(platform, profile_id) / "voice"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_media_documents_dir(self, platform: str, profile_id: str) -> Path:
        path = self.get_media_dir(platform, profile_id) / "documents"
        path.mkdir(parents=True, exist_ok=True)
        return path

    # -------------------------------------------------
    # Global helpers
    # -------------------------------------------------

    def get_cache_root(self) -> Path:
        return self.cache_dir

    def get_log_root(self) -> Path:
        return self.log_dir


# =====================================================
# Backward Compatibility Layer (Minimal + Safe)
# =====================================================

_default_directory = DirectoryManager()

root_dir = _default_directory.root_dir
cache_dir = _default_directory.cache_dir
log_dir = _default_directory.log_dir
platforms_dir = _default_directory.platforms_dir

# ==========================================
# Minimal Backward Compatibility (Temporary)
# ==========================================

fingerprint_file = cache_dir / "fingerprint.pkl"
fingerprint_debug_json = cache_dir / "fingerprint.json"
storage_state_file = cache_dir / "storage_state.json"

