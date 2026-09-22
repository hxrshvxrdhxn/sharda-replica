import asyncio
from playwright.async_api import async_playwright
import os

async def capture_nav_elements():
    os.makedirs('scraper/output/nav_elements', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Live Header Element Screenshot
        page_live = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_live.goto('https://www.sharda.ac.in', wait_until='networkidle')
        header_live = page_live.locator('#header')
        await header_live.screenshot(path='scraper/output/nav_elements/header_live.png')
        
        # 2. Local Header Element Screenshot
        page_local = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_local.goto('http://127.0.0.1:3000', wait_until='networkidle')
        header_local = page_local.locator('#header')
        await header_local.screenshot(path='scraper/output/nav_elements/header_local.png')
        
        # 3. Live Footer Element Screenshot
        footer_live = page_live.locator('#footer')
        await footer_live.screenshot(path='scraper/output/nav_elements/footer_live.png')
        
        # 4. Local Footer Element Screenshot
        footer_local = page_local.locator('#footer')
        await footer_local.screenshot(path='scraper/output/nav_elements/footer_local.png')
        
        # 5. Live vs Local Dropdown Hover Screenshots
        menus = ['Academic', 'Admissions', 'Campus Life', 'About', 'Connect', 'International']
        for m in menus:
            m_slug = m.replace(' ', '_').lower()
            
            # Hover Live
            li_live = page_live.locator(f"#main-navigation > ul > li:has-text('{m}')").first
            await li_live.hover(force=True)
            await page_live.wait_for_timeout(300)
            await page_live.screenshot(path=f'scraper/output/nav_elements/dropdown_live_{m_slug}.png')
            
            # Hover Local
            li_local = page_local.locator(f"#main-navigation > ul > li:has-text('{m}')").first
            await li_local.hover(force=True)
            await page_local.wait_for_timeout(300)
            await page_local.screenshot(path=f'scraper/output/nav_elements/dropdown_local_{m_slug}.png')
            print(f"[CAPTURED] {m} dropdown screenshots for live and local.")
            
        await browser.close()
        print("\nAll nav element screenshots captured successfully!")

if __name__ == '__main__':
    asyncio.run(capture_nav_elements())
