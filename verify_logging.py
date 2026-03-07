import asyncio
import os
import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent))

from src.custom_logger import TweakioLogger
from src.directory import DirectoryManager
# This should now work if BrowserManager is exposed correctly
from src.BrowserManager import BrowserManager

async def verify_logging():
    dm = DirectoryManager()
    app_log = dm.get_error_trace_file()
    browser_log = dm.get_browser_log_file()
    
    # Ensure logs are fresh
    for log in [app_log, browser_log]:
        if log.exists():
            try:
                log.unlink()
            except PermissionError:
                pass # Already open
            
    try:
        # 1. Test TweakioLogger directly
        app_logger = TweakioLogger.get_logger("test.app", log_type="app")
        browser_test_logger = TweakioLogger.get_logger("test.browser", log_type="browser")
        
        app_logger.info("This is an app log message")
        browser_test_logger.info("This is a browser log message")
        
        # 2. Test via BrowserManager (optional, if we want to see it in action)
        # bm = BrowserManager(headless=True)
        # await bm.get_page()
        # await bm.close()
        
        # Wait for logs to be written
        await asyncio.sleep(1)
        
        print(f"Checking {app_log}...")
        if app_log.exists():
            content = app_log.read_text()
            if "This is an app log message" in content:
                print("✅ App log verified correctly")
            else:
                print("❌ App log verification failed - message not found")
        else:
            print(f"❌ App log file {app_log} not found")

        print(f"Checking {browser_log}...")
        if browser_log.exists():
            content = browser_log.read_text()
            if "This is a browser log message" in content:
                print("✅ Browser log verified correctly")
            else:
                print("❌ Browser log verification failed - message not found")
        else:
            print(f"❌ Browser log file {browser_log} not found")
            
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_logging())
