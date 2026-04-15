"""
Unit tests for global_metadata package.
"""

from camouchat_core import Platform, StorageType


def test_platform_list():
    """Test Platform.list_platforms()."""
    platforms = Platform.list_platforms()
    assert "WhatsApp" in platforms
    assert "Arattai" in platforms
    assert len(platforms) == 2


def test_storage_type_list():
    """Test StorageType.list_types()."""
    types = StorageType.list_types()
    assert "sqlite" in types
    assert "mysql" in types
    assert "postgresql" in types
    assert len(types) == 3
