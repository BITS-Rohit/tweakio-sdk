from pathlib import Path
from src.BrowserManager.profile_info import ProfileInfo
from src.BrowserManager.platform_manager import Platform
from unittest.mock import Mock


def test_profile_info_init():
    """Test ProfileInfo dataclass initialization."""
    p = ProfileInfo(
        profile_id="test",
        platform=Platform.WHATSAPP,
        version="0.6",
        created_at="now",
        last_used="now",
        profile_dir=Path("/tmp/p"),
        fingerprint_path=Path("/tmp/p/f.pkl"),
        cache_dir=Path("/tmp/p/cache"),
        media_dir=Path("/tmp/p/media"),
        media_images_dir=Path("/tmp/p/media/img"),
        media_videos_dir=Path("/tmp/p/media/vid"),
        media_voice_dir=Path("/tmp/p/media/vc"),
        media_documents_dir=Path("/tmp/p/media/doc"),
        database_path=Path("/tmp/p/db"),
        is_active=False,
        last_active_pid=None,
        encryption={},
    )
    assert p.profile_id == "test"
    assert p.platform == Platform.WHATSAPP


def test_profile_info_from_metadata():
    """Test ProfileInfo.from_metadata factory method."""
    metadata = {
        "profile_id": "meta_user",
        "platform": Platform.WHATSAPP,
        "version": "0.6",
        "created_at": "date1",
        "last_used": "date2",
        "status": {"is_active": True, "last_active_pid": 1234},
        "encryption": {"enabled": True},
    }

    mock_directory = Mock()
    mock_directory.get_profile_dir.return_value = Path("/app/meta_user")
    mock_directory.get_cache_dir.return_value = Path("/app/meta_user/cache")
    mock_directory.get_media_dir.return_value = Path("/app/meta_user/media")
    mock_directory.get_media_images_dir.return_value = Path("/app/meta_user/media/images")
    mock_directory.get_media_videos_dir.return_value = Path("/app/meta_user/media/videos")
    mock_directory.get_media_voice_dir.return_value = Path("/app/meta_user/media/voice")
    mock_directory.get_media_documents_dir.return_value = Path("/app/meta_user/media/docs")
    mock_directory.get_database_path.return_value = Path("/app/meta_user/messages.db")

    p = ProfileInfo.from_metadata(metadata, mock_directory)

    assert p.profile_id == "meta_user"
    assert p.is_active is True
    assert p.last_active_pid == 1234
    assert p.encryption["enabled"] is True
    assert p.profile_dir == Path("/app/meta_user")
    assert p.fingerprint_path == Path("/app/meta_user/fingerprint.pkl")
