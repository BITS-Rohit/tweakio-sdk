import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Mock external dependencies to avoid installation requirements
sys.modules["camoufox"] = MagicMock()
sys.modules["camoufox.exceptions"] = MagicMock()
sys.modules["camoufox.async_api"] = MagicMock()
sys.modules["browserforge"] = MagicMock()
sys.modules["browserforge.fingerprints"] = MagicMock()
sys.modules["colorlog"] = MagicMock()
sys.modules["playwright"] = MagicMock()
sys.modules["playwright.async_api"] = MagicMock()

import pytest

from src.BrowserManager import BrowserManager
from src.browser_logger import browser_logger


@pytest.mark.asyncio
async def test_browser_manager_uses_browser_logger():
    """
    Verify that BrowserManager operations log to browser_logger
    and NOT the main application logger.
    """
    # 1. Setup mocks
    mock_browser_context = AsyncMock()
    mock_browser_context.pages = []
    
    # Mock AsyncCamoufox context manager
    mock_camoufox = AsyncMock()
    mock_camoufox.__aenter__.return_value = mock_browser_context
    mock_camoufox.__aexit__.return_value = None
    
    # Configure FingerprintGenerator mock to return valid integers for comparison
    # BrowserManager imports: from browserforge.fingerprints import FingerprintGenerator
    # So we configure the mocked class to return a generator that produces a fingerprint with int dims
    mock_fg = MagicMock()
    mock_fg.screen.width = 1920
    mock_fg.screen.height = 1080
    
    mock_fp_gen_class = sys.modules["browserforge.fingerprints"].FingerprintGenerator
    mock_fp_gen_class.return_value.generate.return_value = mock_fg
    
    # Mock the browser_logger to verify calls
    with patch("src.BrowserManager.browser_logger") as mock_browser_log, \
         patch("src.BrowserManager.AsyncCamoufox", return_value=mock_camoufox), \
         patch("src.BrowserManager.logger") as mock_main_log, \
         patch("src.BrowserManager.pickle") as mock_pickle, \
         patch("builtins.open", new_callable=MagicMock):  # Should NOT be called
        
        # 2. Initialize Manager (triggers fingerprint generation logs)
        manager = BrowserManager(
            headless=True,
            override_fingerprint=True  # Force logs
        )
        
        # 3. Launch Instance (triggers IP checks and fingerprint generation)
        await manager.getInstance()
        
        # Verify fingerprint logs went to browser_logger
        mock_browser_log.info.assert_any_call("♻️ Override enabled. Generating a fresh fingerprint...")
        mock_browser_log.info.assert_any_call("🧬 Generating new fingerprint...")
        
        # Ensure main logger was NOT used for these
        assert mock_main_log.info.call_count == 0
        
        # 4. Error Handling Integration
        # Simulate clean exit which logs error if exception occurs
        # or verify page creation error logging
        
        # Test getPage error logging
        manager.browser = mock_browser_context
        mock_browser_context.new_page.side_effect = Exception("Page Crash")
        
        with pytest.raises(Exception):
            await manager.getPage()
            
        # Verify error logged to browser_logger
        mock_browser_log.error.assert_called_with(
            "❌ Failed to create new page: Page Crash", 
            exc_info=True
        )
        
        # Verify main logger still untouched for browser ops
        assert mock_main_log.error.call_count == 0
