import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

async def get_stylesheets():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('https://www.sharda.ac.in', wait_until='networkidle')
        
        links = await page.evaluate("() => Array.from(document.querySelectorAll('link[rel=stylesheet]')).map(l => l.href)")
        print("STYLESHEETS ON LIVE:")
        for l in links:
            print(" -", l)
            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        for l in links:
            filename = l.split('/')[-1].split('?')[0]
            if filename in ['bootstrap-3.3.7.min.css', 'font-awesome.min.css', 'sharda_common_style_min.css']:
                target = os.path.join('frontend/public/assets/css', filename)
                req = urllib.request.Request(l, headers=headers)
                try:
                    content = urllib.request.urlopen(req).read()
                    with open(target, 'wb') as f:
                        f.write(content)
                    print(f"Downloaded {filename} ({len(content)} bytes)")
                except Exception as e:
                    print(f"Error downloading {l}: {e}")
                    
        await browser.close()

if __name__ == '__main__':
    asyncio.run(get_stylesheets())
