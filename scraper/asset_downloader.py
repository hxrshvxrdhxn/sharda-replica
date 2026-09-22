import asyncio
import httpx
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "frontend" / "public" / "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

CRITICAL_ASSETS = [
    {"filename": "logo.png", "url": "https://www.sharda.ac.in/attachments/site_logo/logo22.png"},
    {"filename": "favi-icon.png", "url": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/favi-icon.png"},
    {"filename": "naac_logo.png", "url": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/naac_logo.png"},
    {"filename": "nirf_logo.png", "url": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/nirf_logo.png"},
    {"filename": "campus_banner.jpg", "url": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/virutal-tour_1200x628.jpg"},
]

async def download_asset(client, asset):
    filepath = ASSETS_DIR / asset["filename"]
    try:
        resp = await client.get(asset["url"], follow_redirects=True, timeout=15.0)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            print(f"Downloaded: {asset['filename']} ({len(resp.content)} bytes)")
        else:
            print(f"Warning: {asset['filename']} returned HTTP {resp.status_code}")
    except Exception as e:
        print(f"Failed to download {asset['filename']}: {e}")

async def main():
    print(f"Downloading critical brand assets into {ASSETS_DIR}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with httpx.AsyncClient(headers=headers, verify=False) as client:
        tasks = [download_asset(client, asset) for asset in CRITICAL_ASSETS]
        await asyncio.gather(*tasks)
    print("Asset download process completed.")

if __name__ == "__main__":
    asyncio.run(main())
