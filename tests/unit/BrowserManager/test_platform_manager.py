from src.BrowserManager.platform_manager import Platform


def test_platform_enum_values():
    """Test Platform enum values match expected strings."""
    assert Platform.WHATSAPP == "WhatsApp"
    assert Platform.ARATTAI == "Arattai"


def test_list_platforms():
    """Test Platform.list_platforms returns all available platforms."""
    platforms = Platform.list_platforms()
    assert "WhatsApp" in platforms
    assert "Arattai" in platforms
    assert len(platforms) == 2
