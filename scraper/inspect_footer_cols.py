import asyncio
from playwright.async_api import async_playwright
import json

async def inspect_footer_top():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page_live = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_live.goto('https://www.sharda.ac.in', wait_until='networkidle')
        
        page_local = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_local.goto('http://127.0.0.1:3000', wait_until='networkidle')
        
        live_cols = await page_live.evaluate('''() => {
            const cols = document.querySelectorAll('#footer .top > .row > div');
            return Array.from(cols).map(c => ({
                class: c.className,
                offsetHeight: c.offsetHeight,
                textLen: c.innerText.length,
                linksCount: c.querySelectorAll('a').length,
                titles: Array.from(c.querySelectorAll('h3, h4, .title, strong')).map(t => t.innerText.trim())
            }));
        }''')
        
        local_cols = await page_local.evaluate('''() => {
            const cols = document.querySelectorAll('#footer .top > .row > div');
            return Array.from(cols).map(c => ({
                class: c.className,
                offsetHeight: c.offsetHeight,
                textLen: c.innerText.length,
                linksCount: c.querySelectorAll('a').length,
                titles: Array.from(c.querySelectorAll('h3, h4, .title, strong')).map(t => t.innerText.trim())
            }));
        }''')
        
        print('LIVE COLS:')
        for i, c in enumerate(live_cols):
            print(f"Col {i}: height={c['offsetHeight']}, links={c['linksCount']}, titles={c['titles']}")
            
        print('LOCAL COLS:')
        for i, c in enumerate(local_cols):
            print(f"Col {i}: height={c['offsetHeight']}, links={c['linksCount']}, titles={c['titles']}")
            
        # Also compare entire HTML of #footer
        live_html = await page_live.evaluate("document.querySelector('#footer').outerHTML")
        local_html = await page_local.evaluate("document.querySelector('#footer').outerHTML")
        
        with open('d:/Su/scraper/output/live_footer.html', 'w', encoding='utf-8') as f:
            f.write(live_html)
        with open('d:/Su/scraper/output/local_footer.html', 'w', encoding='utf-8') as f:
            f.write(local_html)
            
        print("Wrote live_footer.html and local_footer.html")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_footer_top())
