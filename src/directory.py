from pathlib import Path
from platformdirs import PlatformDirs


class DirectoryManager:
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

    def _ensure_base_dirs(self):
        for d in [self.root_dir, self.cache_dir, self.log_dir, self.platforms_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def get_platform_dir(self, platform: str) -> Path:
        path = self.platforms_dir / platform.lower()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_profile_dir(self, platform: str, profile_id: str) -> Path:
        return self.get_platform_dir(platform) / profile_id
    
    def get_database_path(self, platform: str, profile_id: str) -> Path:
        return self.get_profile_dir(platform, profile_id) / "messages.db"

    def get_error_trace_file(self) -> Path:
        return self.cache_dir / "ErrorTrace.log"

    def get_message_trace_file(self) -> Path:
        return self.cache_dir / "MessageTrace.txt"



    # ----------------------------
    # Profile Subdirectories
    # ----------------------------

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

    # ----------------------------
    # Global paths
    # ----------------------------

    def get_cache_root(self) -> Path:
        return self.cache_dir

    def get_log_root(self) -> Path:
        return self.log_dir
    
# ================================
# Backward compatibility layer
# ================================

_default_directory = DirectoryManager()

# Base dirs
root_dir = _default_directory.root_dir
cache_dir = _default_directory.cache_dir
log_dir = _default_directory.log_dir
platforms_dir = _default_directory.platforms_dir

# Legacy file paths
fingerprint_file = root_dir / "BrowserManager" / "fingerprint.pkl"
fingerprint_debug_json = root_dir / "BrowserManager" / "fingerprint.json"
storage_state_file = root_dir / "BrowserManager" / "StorageState.json"

ErrorTrace_file = _default_directory.get_error_trace_file()
# MessageTrace_file = _default_directory.get_message_trace_file() # we are not using it anywhere


