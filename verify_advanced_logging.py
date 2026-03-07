import asyncio
import json
import os
import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent))

from src.custom_logger import TweakioLogger
from src.directory import DirectoryManager

async def verify_advanced_logging():
    dm = DirectoryManager()
    app_log = dm.get_error_trace_file()
    browser_log = dm.get_browser_log_file()
    
    # Ensure logs are fresh
    for log in [app_log, browser_log]:
        if log.exists():
            try:
                log.unlink()
            except PermissionError:
                pass
            
    try:
        print("--- Testing Contextual Logging (Standard Format) ---")
        profile_id = "test-profile-123"
        logger = TweakioLogger.get_logger("test.context", profile_id=profile_id)
        logger.info("Contextual log message")
        
        await asyncio.sleep(0.5)
        
        if app_log.exists():
            content = app_log.read_text()
            print(f"Log content (last line): {content.splitlines()[-1]}")
            if profile_id in content and str(os.getpid()) in content:
                print("✅ Contextual logging verified (ProfileID and PID found)")
            else:
                print("❌ Contextual logging verification failed")
        else:
            print("❌ App log file not found")

        print("\n--- Testing JSON Logging ---")
        json_logger = TweakioLogger.get_logger("test.json", use_json=True, profile_id="json-prof")
        json_logger.info("JSON log message")
        
        await asyncio.sleep(0.5)
        
        # JSON logs go to the same file (app_log in this case as it's 'app' type)
        # But wait, TweakioLogger.get_logger uses name and use_json in key.
        # Let's check the file content again.
        if app_log.exists():
            lines = app_log.read_text().splitlines()
            json_line = lines[-1]
            print(f"JSON line: {json_line}")
            try:
                data = json.loads(json_line)
                if data["message"] == "JSON log message" and data["profile_id"] == "json-prof":
                    print("✅ JSON logging verified correctly")
                else:
                    print("❌ JSON logging verification failed - data mismatch")
            except json.JSONDecodeError:
                print("❌ JSON logging verification failed - not valid JSON")
        else:
            print("❌ App log file not found for JSON test")

        print("\n--- Testing Browser Logging ---")
        b_logger = TweakioLogger.get_logger("test.browser", log_type="browser", profile_id="browser-prof")
        b_logger.info("Browser-specific log")
        
        await asyncio.sleep(0.5)
        
        if browser_log.exists():
            content = browser_log.read_text()
            print(f"Browser log content: {content.splitlines()[-1]}")
            if "browser-prof" in content:
                print("✅ Browser logging verified")
            else:
                print("❌ Browser logging verification failed")
        else:
            print("❌ Browser log file not found")

    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_advanced_logging())
