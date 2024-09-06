from fastapi import FastAPI
from facebook_page_info_scraper import FacebookPageInfoScraper

app = FastAPI()

@app.get("/followers")
def get_followers(username: str):
    page_url = f'https://www.facebook.com/{username}'

    scraper = FacebookPageInfoScraper(link=page_url)
    page_info = scraper.get_page_info()

    page_followers = page_info.get('page_followers', 'Data not available')

    return {"page_followers": page_followers}
