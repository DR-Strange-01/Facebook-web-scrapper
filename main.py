from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random

app = FastAPI()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')

# Setting Chrome binary location
chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN", "/app/.chrome-for-testing/chrome-linux64/chrome")
chrome_driver_path = os.getenv("CHROMEDRIVER_PATH", "/app/.chrome-for-testing/chromedriver-linux64/chromedriver")


print(f"Chrome binary location: {chrome_options.binary_location}")
print(f"ChromeDriver path: {chrome_driver_path}")

class UsernameInput(BaseModel):
    username: str

def initialize_driver():
    try:
        # Using WebDriver Manager to install ChromeDriver
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail=f"WebDriver error: {str(e)}")

def random_sleep(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def handle_popup(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Close']"))
        )
        close_button.click()
    except TimeoutException:
        pass  # if Popup may not be present

def get_subscriber_count(driver):
    try:
        subscriber_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'x193iq5w')]//a[contains(@href, '/followers/')]"))
        )
        return subscriber_element.text.split()[0]
    except TimeoutException:
        return "N/A"
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/get_subscriber_count")
async def get_subscriber_count_api(input_data: UsernameInput):
    driver = None
    try:
        driver = initialize_driver()
        url = f"https://www.facebook.com/{input_data.username}"
        driver.get(url)
        random_sleep()
        
        handle_popup(driver)
        random_sleep()
        
        subscriber_count = get_subscriber_count(driver)
        return {"subscriber_count": subscriber_count}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting info: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
