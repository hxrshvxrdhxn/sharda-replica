import asyncio
from playwright.async_api import async_playwright
import os

async def test_all_dropdowns():
    os.makedirs('scraper/output/dropdowns', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000', wait_until='networkidle')
        
        menu_items = ['Academic', 'Admissions', 'Campus Life', 'About', 'Connect', 'International']
        
        for name in menu_items:
            selector = f"#main-navigation > ul > li:has-text('{name}')"
            li = page.locator(selector).first
            
            # Hover over menu item
            await li.hover(force=True)
            await page.wait_for_timeout(400)
            
            # Check dropdown visibility
            dropdown = li.locator('.dropdown')
            is_visible = await dropdown.is_visible()
            box = await dropdown.bounding_box()
            links_count = await dropdown.locator('a').count()
            
            print(f"[{'PASS' if is_visible else 'FAIL'}] Menu '{name}': Visible={is_visible}, Box={box}, Links={links_count}")
            
            # Screenshot of opened menu
            clean_name = name.replace(' ', '_').lower()
            await page.screenshot(path=f"scraper/output/dropdowns/{clean_name}_dropdown.png")
            
        await browser.close()
        print("\nAll dropdown hover tests completed!")

if __name__ == '__main__':
    asyncio.run(test_all_dropdowns())
