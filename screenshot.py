#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def take_screenshot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=options)
        
        print("Opening http://localhost:8000/...")
        driver.get("http://localhost:8000/")
        
        # Wait for the map to load (adjust selector as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Additional wait for map tiles to load
        time.sleep(3)
        
        # Take screenshot
        driver.save_screenshot("map_screenshot.png")
        print("Screenshot saved as map_screenshot.png")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False

if __name__ == "__main__":
    success = take_screenshot()
    sys.exit(0 if success else 1)