import asyncio
import httpx
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_DIR = BASE_DIR / "frontend" / "public" / "assets" / "css"
JS_DIR = BASE_DIR / "frontend" / "public" / "assets" / "js"
IMGS_DIR = BASE_DIR / "frontend" / "public" / "assets" / "imgs"

CSS_DIR.mkdir(parents=True, exist_ok=True)
JS_DIR.mkdir(parents=True, exist_ok=True)
IMGS_DIR.mkdir(parents=True, exist_ok=True)

ASSETS = [
    # Stylesheets
    {"url": "https://sharda.ac.in/assets/sharda_latest_css/bootstrap-3.3.7.min.css?v=1", "dest": CSS_DIR / "bootstrap-3.3.7.min.css"},
    {"url": "https://www.sharda.ac.in/assets/sharda_latest_css/font-awesome.min.css?v1.1", "dest": CSS_DIR / "font-awesome.min.css"},
    {"url": "https://www.sharda.ac.in/assets/sharda_latest_css/sharda_common_style_min.css?v1.15.6.21.8.9.09", "dest": CSS_DIR / "sharda_common_style_min.css"},
    # Scripts
    {"url": "https://sharda.ac.in/assets/js/jquery-1.12.2.min.js", "dest": JS_DIR / "jquery-1.12.2.min.js"},
    {"url": "https://sharda.ac.in/assets/js/bootstrap-3.3.7.min.js", "dest": JS_DIR / "bootstrap-3.3.7.min.js"},
    {"url": "https://www.sharda.ac.in/assets/js/sharda_speak.js?v1.1", "dest": JS_DIR / "sharda_speak.js"},
    {"url": "https://sharda.ac.in/assets/js/easySlider1.7.js?v=101", "dest": JS_DIR / "easySlider1.7.js"},
    {"url": "https://sharda.ac.in/assets/js/jquery.group.js", "dest": JS_DIR / "jquery.group.js"},
    {"url": "https://sharda.ac.in/assets/js/carouFredSel-6.0.5-packed.js", "dest": JS_DIR / "carouFredSel-6.0.5-packed.js"},
    {"url": "https://www.sharda.ac.in/assets/js/sharda_common_revamp_min.js?v3.0.8", "dest": JS_DIR / "sharda_common_revamp_min.js"},
    # Brand Images & Logos
    {"url": "https://www.sharda.ac.in/attachments/site_logo/logo22.png", "dest": IMGS_DIR / "logo22.png"},
    {"url": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/favi-icon.png", "dest": IMGS_DIR / "favi-icon.png"},
    {"url": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/virutal-tour_1200x628.jpg", "dest": IMGS_DIR / "virutal-tour_1200x628.jpg"}
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "*/*",
}

async def download_file(client, item):
    try:
        resp = await client.get(item["url"], timeout=20.0, follow_redirects=True)
        if resp.status_code == 200:
            with open(item["dest"], "wb") as f:
                f.write(resp.content)
            print(f"Downloaded: {item['dest'].name} ({len(resp.content)} bytes)")
        else:
            print(f"Failed {item['url']}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"Error downloading {item['url']}: {e}")

async def main():
    print("Starting exact asset download...")
    async with httpx.AsyncClient(headers=HEADERS, verify=False) as client:
        tasks = [download_file(client, item) for item in ASSETS]
        await asyncio.gather(*tasks)
    print("Asset download completed.")

if __name__ == "__main__":
    asyncio.run(main())
