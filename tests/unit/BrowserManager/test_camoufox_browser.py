"""
Unit tests for CamoufoxBrowser class.
Tests browser initialization, page management, and cleanup.
"""

import logging
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

import pytest
from playwright.async_api import BrowserContext, Page

# Direct imports to avoid circular dependency
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.BrowserManager.browser_config import BrowserConfig
from src.BrowserManager.profile_info import ProfileInfo
from src.BrowserManager.platform_manager import Platform
from src.BrowserManager import camoufox_browser
from src.Exceptions import base

CamoufoxBrowser = camoufox_browser.CamoufoxBrowser
BrowserException = base.BrowserException

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_logger():
    return Mock(spec=logging.Logger)


@pytest.fixture
def mock_browserforge():
    """Mock BrowserForgeCapable implementation."""
    # Create a mock that matches the interface
    bf = Mock()
    bf.get_fg.return_value = Mock()  # Return mock fingerprint
    return bf


@pytest.fixture
def mock_profile_info(tmp_path):
    """Create a mock ProfileInfo object."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    return ProfileInfo(
        profile_id="test_user",
        platform=Platform.WHATSAPP,
        version="0.6",
        created_at="now",
        last_used="now",
        profile_dir=profile_dir,
        fingerprint_path=profile_dir / "fingerprint.pkl",
        cache_dir=profile_dir / "cache",
        media_dir=profile_dir / "media",
        media_images_dir=profile_dir / "media/img",
        media_videos_dir=profile_dir / "media/vid",
        media_voice_dir=profile_dir / "media/vc",
        media_documents_dir=profile_dir / "media/doc",
        database_path=profile_dir / "messages.db",
        is_active=False,
        last_active_pid=None,
        encryption={},
    )


@pytest.fixture
def mock_browser_config(mock_browserforge):
    """Create a mock BrowserConfig object."""
    return BrowserConfig(
        platform=Platform.WHATSAPP,
        locale="en-US",
        enable_cache=True,
        headless=True,
        fingerprint_obj=mock_browserforge,
    )


@pytest.fixture
def browser_instance(mock_browser_config, mock_profile_info, mock_logger):
    """Create CamoufoxBrowser instance with required dependencies."""
    return CamoufoxBrowser(
        config=mock_browser_config, profileInfo=mock_profile_info, log=mock_logger
    )


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================


def test_init_success(mock_browser_config, mock_profile_info, mock_logger):
    """Test CamoufoxBrowser initializes with all required params."""
    browser = CamoufoxBrowser(
        config=mock_browser_config, profileInfo=mock_profile_info, log=mock_logger
    )

    assert browser.config == mock_browser_config
    assert browser.profileInfo == mock_profile_info
    assert browser.log == mock_logger


def test_init_missing_logger(mock_browser_config, mock_profile_info):
    """Test CamoufoxBrowser raises error without logger."""
    with pytest.raises(BrowserException, match="Logger is missing"):
        CamoufoxBrowser(config=mock_browser_config, profileInfo=mock_profile_info, log=None)


def test_init_missing_config(mock_profile_info, mock_logger):
    """Test CamoufoxBrowser raises error without Config."""
    with pytest.raises(BrowserException, match="BrowserConfig is missing"):
        CamoufoxBrowser(config=None, profileInfo=mock_profile_info, log=mock_logger)


def test_init_missing_profile_info(mock_browser_config, mock_logger):
    """Test CamoufoxBrowser raises error without ProfileInfo."""
    with pytest.raises(BrowserException, match="ProfileInfo is missing"):
        CamoufoxBrowser(config=mock_browser_config, profileInfo=None, log=mock_logger)


# ============================================================================
# GET INSTANCE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_getInstance_creates_browser(browser_instance, mock_browserforge):
    """Test getInstance creates browser on first call."""
    mock_context = AsyncMock(spec=BrowserContext)
    mock_fingerprint = Mock()
    mock_browserforge.get_fg.return_value = mock_fingerprint

    # Mock AsyncCamoufox to avoid actual browser launch
    mock_camoufox = AsyncMock()
    mock_camoufox.__aenter__.return_value = mock_context

    with patch("src.BrowserManager.camoufox_browser.AsyncCamoufox", return_value=mock_camoufox):
        with patch("src.BrowserManager.camoufox_browser.launch_options", return_value={}):
            result = await browser_instance.get_instance()

            assert result == mock_context
            assert browser_instance.browser == mock_context
            mock_browserforge.get_fg.assert_called_once()


@pytest.mark.asyncio
async def test_getInstance_reuses_existing(browser_instance):
    """Test getInstance returns existing browser without recreating."""
    mock_context = AsyncMock(spec=BrowserContext)
    browser_instance.browser = mock_context

    result = await browser_instance.get_instance()

    assert result == mock_context


# ============================================================================
# GET BROWSER TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_GetBrowser_success(browser_instance, mock_browserforge):
    """Test _get_browser successfully launches Camoufox."""
    mock_context = AsyncMock(spec=BrowserContext)
    mock_fingerprint = Mock()
    mock_browserforge.get_fg.return_value = mock_fingerprint

    # Mock AsyncCamoufox
    mock_camoufox = AsyncMock()
    mock_camoufox.__aenter__.return_value = mock_context

    with patch("src.BrowserManager.camoufox_browser.AsyncCamoufox", return_value=mock_camoufox):
        with patch("src.BrowserManager.camoufox_browser.launch_options", return_value={}):
            result = await browser_instance._get_browser()

            assert result == mock_context
            mock_browserforge.get_fg.assert_called_once()


@pytest.mark.asyncio
async def test_GetBrowser_retries_on_invalid_ip(browser_instance, mock_browserforge, mock_logger):
    """Test _get_browser retries on Camoufox InvalidIP error."""
    mock_context = AsyncMock(spec=BrowserContext)
    mock_fingerprint = Mock()
    mock_browserforge.get_fg.return_value = mock_fingerprint

    # First call raises InvalidIP, second succeeds
    call_count = 0

    async def mock_aenter(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            import camoufox.exceptions

            raise camoufox.exceptions.InvalidIP("IP check failed")
        return mock_context

    mock_camoufox = AsyncMock()
    mock_camoufox.__aenter__.side_effect = mock_aenter

    with patch("src.BrowserManager.camoufox_browser.AsyncCamoufox", return_value=mock_camoufox):
        with patch("src.BrowserManager.camoufox_browser.launch_options", return_value={}):
            result = await browser_instance._get_browser()

            assert result == mock_context
            assert call_count == 2
            mock_logger.warning.assert_called()


@pytest.mark.asyncio
async def test_GetBrowser_max_retries(browser_instance, mock_browserforge):
    """Test _get_browser stops after max retries."""
    mock_browserforge.get_fg.return_value = Mock()

    async def mock_aenter(*args, **kwargs):
        import camoufox.exceptions

        raise camoufox.exceptions.InvalidIP("IP check failed")

    mock_camoufox = AsyncMock()
    mock_camoufox.__aenter__.side_effect = mock_aenter

    with patch("src.BrowserManager.camoufox_browser.AsyncCamoufox", return_value=mock_camoufox):
        with patch("src.BrowserManager.camoufox_browser.launch_options", return_value={}):
            with pytest.raises(BrowserException, match="Max Camoufox IP retry"):
                await browser_instance._get_browser(tries=5)


@pytest.mark.asyncio
async def test_GetBrowser_other_exception(browser_instance, mock_browserforge):
    """Test _get_browser raises BrowserException on other errors."""
    mock_browserforge.get_fg.return_value = Mock()

    with patch(
        "src.BrowserManager.camoufox_browser.AsyncCamoufox", side_effect=Exception("Unknown error")
    ):
        with pytest.raises(BrowserException, match="Failed to launch Camoufox"):
            await browser_instance._get_browser()


# ============================================================================
# GET PAGE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_page_reuses_blank_page(browser_instance):
    """Test get_page returns existing blank page if available."""
    mock_page = AsyncMock(spec=Page)
    mock_page.url = "about:blank"
    mock_page.is_closed.return_value = False

    mock_context = AsyncMock(spec=BrowserContext)
    mock_context.pages = [mock_page]

    browser_instance.browser = mock_context

    result = await browser_instance.get_page()

    assert result == mock_page
    mock_context.new_page.assert_not_called()


@pytest.mark.asyncio
async def test_get_page_creates_new(browser_instance):
    """Test get_page creates new page if no blank page exists."""
    mock_existing_page = AsyncMock(spec=Page)
    mock_existing_page.url = "https://example.com"

    mock_new_page = AsyncMock(spec=Page)

    mock_context = AsyncMock(spec=BrowserContext)
    mock_context.pages = [mock_existing_page]
    mock_context.new_page.return_value = mock_new_page

    browser_instance.browser = mock_context

    result = await browser_instance.get_page()

    assert result == mock_new_page
    mock_context.new_page.assert_called_once()


@pytest.mark.asyncio
async def test_get_page_initializes_browser(browser_instance):
    """Test get_page initializes browser if not already initialized."""
    mock_context = AsyncMock(spec=BrowserContext)
    mock_page = AsyncMock(spec=Page)
    mock_context.pages = []
    mock_context.new_page.return_value = mock_page

    with patch.object(browser_instance, "get_instance", return_value=mock_context):
        result = await browser_instance.get_page()

        assert result == mock_page


@pytest.mark.asyncio
async def test_get_page_error(browser_instance):
    """Test get_page raises BrowserException on failure."""
    mock_context = AsyncMock(spec=BrowserContext)
    mock_context.pages = []
    mock_context.new_page.side_effect = Exception("Page creation failed")

    browser_instance.browser = mock_context

    with pytest.raises(BrowserException, match="Could not create a new page"):
        await browser_instance.get_page()


# ============================================================================
# CLOSE BROWSER TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_close_browser_success(browser_instance):
    """Test close_browser successfully closes browser context."""
    mock_context = AsyncMock(spec=BrowserContext)
    browser_instance.browser = mock_context
    pid = 1234
    browser_instance.profileInfo.last_active_pid = pid
    CamoufoxBrowser.Map[pid] = mock_context

    with patch.object(CamoufoxBrowser, "close_browser_by_pid", return_value=True) as mock_close:
        result = await browser_instance.close_browser()

        assert result is True
        assert browser_instance.browser is None
        mock_close.assert_called_once_with(pid)


@pytest.mark.asyncio
async def test_close_browser_already_closed(browser_instance):
    """Test close_browser returns True if browser already None."""
    browser_instance.browser = None

    result = await browser_instance.close_browser()

    assert result is True


@pytest.mark.asyncio
async def test_close_browser_error(browser_instance, mock_logger):
    """Test close_browser handles exceptions gracefully."""
    mock_context = AsyncMock(spec=BrowserContext)
    browser_instance.browser = mock_context
    browser_instance.log = mock_logger

    with patch.object(
        CamoufoxBrowser, "close_browser_by_pid", side_effect=Exception("Close failed")
    ):
        result = await browser_instance.close_browser()
        assert result is False
        mock_logger.error.assert_called()


@pytest.mark.asyncio
async def test_close_browser_by_pid_success():
    """Test close_browser_by_pid class method."""
    mock_context = AsyncMock(spec=BrowserContext)
    pid = 9999
    CamoufoxBrowser.Map[pid] = mock_context

    result = await CamoufoxBrowser.close_browser_by_pid(pid)

    assert result is True
    mock_context.close.assert_called_once()
    assert pid not in CamoufoxBrowser.Map
