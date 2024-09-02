from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import time
import random

# Initialize the FastAPI app
app = FastAPI()

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')

# Set Chrome binary location and ChromeDriver path from the environment variables set by the buildpack
chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
chrome_driver_path = os.getenv("CHROMEDRIVER_PATH", "/app/.chromedriver/bin/chromedriver")

@app.get("/check-paths")
async def check_paths():
    # Return the paths being used
    return {
        "chrome_binary_location": chrome_options.binary_location,
        "chrome_driver_path": chrome_driver_path
    }

def initialize_driver():
    try:
        # Use the ChromeDriver path set by the buildpack environment variable
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail=f"WebDriver error: {str(e)}")

# The rest of your code remains the same...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
