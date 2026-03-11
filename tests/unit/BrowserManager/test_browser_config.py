from src.BrowserManager.browser_config import BrowserConfig
from src.BrowserManager.platform_manager import Platform
from unittest.mock import Mock


def test_browser_config_init():
    """Test BrowserConfig dataclass initialization."""
    mock_bf = Mock()
    config = BrowserConfig(
        platform=Platform.WHATSAPP,
        locale="en-US",
        enable_cache=True,
        headless=False,
        fingerprint_obj=mock_bf,
    )
    assert config.platform == Platform.WHATSAPP
    assert config.locale == "en-US"
    assert config.enable_cache is True
    assert config.headless is False
    assert config.fingerprint_obj == mock_bf
    assert config.prefs is None
    assert config.addons == []


def test_browser_config_from_dict():
    """Test BrowserConfig.from_dict factory method."""
    mock_bf = Mock()
    data = {
        "platform": Platform.WHATSAPP,
        "locale": "fr-FR",
        "enable_cache": False,
        "headless": True,
        "prefs": {"some.pref": True},
        "addons": ["path/to/addon"],
        "fingerprint_obj": mock_bf,
    }
    config = BrowserConfig.from_dict(data)
    assert config.platform == Platform.WHATSAPP
    assert config.locale == "fr-FR"
    assert config.headless is True
    assert config.prefs == {"some.pref": True}
    assert config.addons == ["path/to/addon"]
