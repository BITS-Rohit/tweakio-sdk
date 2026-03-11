import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.resolve()))

from src.BrowserManager.profile_manager import ProfileManager
from src.BrowserManager.platform_manager import Platform
from src.BrowserManager.profile_info import ProfileInfo
from src.BrowserManager.camoufox_browser import CamoufoxBrowser
from src.BrowserManager.browser_config import BrowserConfig


@pytest.fixture
def temp_app_dir(tmp_path):
    app_dir = tmp_path / "CamouChat"
    app_dir.mkdir()
    return app_dir


@pytest.fixture
def profile_manager(temp_app_dir):
    with patch("src.directory.Path.home", return_value=temp_app_dir.parent):
        pm = ProfileManager(app_name="TestApp")
        # Override the directory manager's base path to use our temp dir
        pm.directory.root_dir = temp_app_dir
        pm.directory.platforms_dir = temp_app_dir / "platforms"
        pm.directory.platforms_dir.mkdir(exist_ok=True)
        pm.directory.cache_dir = temp_app_dir / "cache"
        pm.directory.cache_dir.mkdir(exist_ok=True)
        pm.directory.log_dir = temp_app_dir / "logs"
        pm.directory.log_dir.mkdir(exist_ok=True)
        return pm


def test_init(profile_manager):
    assert profile_manager.app_name == "TestApp"
    assert profile_manager.directory is not None


def test_create_profile_success(profile_manager):
    platform = Platform.WHATSAPP
    profile_id = "test_user"

    profile = profile_manager.create_profile(platform, profile_id)

    assert isinstance(profile, ProfileInfo)
    assert profile.profile_id == profile_id
    assert profile.platform == platform

    profile_dir = profile_manager.directory.get_profile_dir(platform, profile_id)
    assert profile_dir.exists()
    assert (profile_dir / "metadata.json").exists()
    assert (profile_dir / "fingerprint.pkl").exists()


def test_get_profile_success(profile_manager):
    platform = Platform.WHATSAPP
    profile_id = "test_user"
    profile_manager.create_profile(platform, profile_id)

    profile = profile_manager.get_profile(platform, profile_id)
    assert profile.profile_id == profile_id
    assert profile.platform == platform


def test_list_profiles(profile_manager):
    platform = Platform.WHATSAPP
    profile_manager.create_profile(platform, "user1")
    profile_manager.create_profile(platform, "user2")

    profiles = profile_manager.list_profiles(platform)
    assert platform in profiles
    assert "user1" in profiles[platform]
    assert "user2" in profiles[platform]


def test_delete_profile(profile_manager):
    platform = Platform.WHATSAPP
    profile_id = "to_delete"
    profile_manager.create_profile(platform, profile_id)

    profile_manager.delete_profile(platform, profile_id)

    profile_dir = profile_manager.directory.get_profile_dir(platform, profile_id)
    assert not profile_dir.exists()


def test_encryption_lifecycle(profile_manager):
    platform = Platform.WHATSAPP
    profile_id = "crypto_user"
    profile_manager.create_profile(platform, profile_id)

    # Mock KeyManager
    with patch("src.Encryption.KeyManager.generate_random_key", return_value=b"0" * 32):
        with patch("src.Encryption.KeyManager.encode_key_for_storage", return_value="encoded_key"):
            key = profile_manager.enable_encryption(platform, profile_id)
            assert key == b"0" * 32
            assert profile_manager.is_encryption_enabled(platform, profile_id) is True

    with patch("src.Encryption.KeyManager.decode_key_from_storage", return_value=b"0" * 32):
        retrieved_key = profile_manager.get_key(platform, profile_id)
        assert retrieved_key == b"0" * 32

    profile_manager.disable_encryption(platform, profile_id)
    assert profile_manager.is_encryption_enabled(platform, profile_id) is False


@pytest.mark.asyncio
async def test_activation_lifecycle(profile_manager):
    platform = Platform.WHATSAPP
    profile_id = "active_user"
    profile_manager.create_profile(platform, profile_id)

    mock_browser = Mock(spec=CamoufoxBrowser)
    mock_browser.config = Mock(spec=BrowserConfig)

    # Activate
    profile_manager.activate_profile(platform, profile_id, mock_browser)

    profile = profile_manager.get_profile(platform, profile_id)
    assert profile.is_active is True

    # Close
    with patch(
        "src.BrowserManager.camoufox_browser.CamoufoxBrowser.close_browser_by_pid",
        return_value=True,
    ):
        await profile_manager.close_profile(platform, profile_id)

    profile = profile_manager.get_profile(platform, profile_id)
    assert profile.is_active is False
