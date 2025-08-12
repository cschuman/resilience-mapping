#!/usr/bin/env python3
import subprocess
import time
import os

def take_screenshot_with_screencapture():
    """Take a screenshot using macOS screencapture command"""
    
    # First, open the URL in the default browser
    print("Opening http://localhost:8000/ in browser...")
    subprocess.run(["open", "http://localhost:8000/"])
    
    # Wait for page to load (1 minute for large JSON)
    print("Waiting 1 minute for large JSON to load...")
    time.sleep(60)
    
    # Take a screenshot of the entire screen
    output_file = "map_screenshot.png"
    print(f"Taking screenshot...")
    
    # Use screencapture to capture the screen
    result = subprocess.run(["screencapture", "-x", output_file])
    
    if result.returncode == 0 and os.path.exists(output_file):
        print(f"Screenshot saved as {output_file}")
        return True
    else:
        print("Failed to take screenshot")
        return False

if __name__ == "__main__":
    import sys
    success = take_screenshot_with_screencapture()
    sys.exit(0 if success else 1)