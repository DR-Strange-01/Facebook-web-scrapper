from fastapi import FastAPI
from facebook_page_info_scraper import FacebookPageInfoScraper
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN", "/app/.apt/usr/bin/google-chrome")

    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH", ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@app.get("/followers/{username}")
def get_followers(username: str):
    page_url = f"https://www.facebook.com/{username}"
    
    scraper = FacebookPageInfoScraper(link=page_url, custom_driver_func=setup_driver)
    followers = scraper.get_followers()
    return {"followers": followers}
