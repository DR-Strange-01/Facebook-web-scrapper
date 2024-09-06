from fastapi import FastAPI
from facebook_page_info_scraper import FacebookPageInfoScraper
import uvicorn

app = FastAPI()

@app.get("/followers")
def get_followers(username: str):
    page_url = f'https://www.facebook.com/{username}'

    scraper = FacebookPageInfoScraper(link=page_url)
    page_info = scraper.get_page_info()

    page_followers = page_info.get('page_followers', 'Data not available')

    return {"page_followers": page_followers}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
