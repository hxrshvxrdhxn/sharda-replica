import asyncio
from playwright.async_api import async_playwright

async def test_all_header_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        await page.goto('http://127.0.0.1:3000', wait_until='networkidle')
        
        header_links = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('#header a, #main-navigation a'));
            return links.map(a => ({
                text: a.innerText.trim(),
                href: a.getAttribute('href') || ''
            })).filter(l => l.href && !l.href.startsWith('javascript:') && !l.href.startsWith('#') && !l.href.startsWith('tel:') && !l.href.startsWith('mailto:'));
        }''')
        
        print(f"Total active links in Header & Navigation: {len(header_links)}")
        print("=" * 85)
        print(f"{'Index':<6} | {'Link Text':<30} | {'Href Target':<32} | {'Result'}")
        print("-" * 85)
        
        passed = 0
        failed = 0
        
        for i, item in enumerate(header_links):
            href = item['href']
            text = item['text'] or 'Menu Link'
            
            if href.startswith('/'):
                target_url = f"http://127.0.0.1:3000{href}"
                test_page = await browser.new_page()
                try:
                    resp = await test_page.goto(target_url, wait_until='domcontentloaded', timeout=15000)
                    status = resp.status if resp else 'No Resp'
                    if status == 200:
                        print(f"{i+1:<6} | {text[:30]:<30} | {href[:32]:<32} | [PASS 200 OK]")
                        passed += 1
                    else:
                        print(f"{i+1:<6} | {text[:30]:<30} | {href[:32]:<32} | [FAIL status {status}]")
                        failed += 1
                except Exception as e:
                    print(f"{i+1:<6} | {text[:30]:<30} | {href[:32]:<32} | [ERR {str(e)[:25]}]")
                    failed += 1
                await test_page.close()
            else:
                print(f"{i+1:<6} | {text[:30]:<30} | {href[:32]:<32} | [EXTERNAL SAFE]")
                passed += 1
                
        print("=" * 85)
        print(f"Header Navigation Summary: {passed} passed / {len(header_links)} total ({failed} failed)")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_all_header_links())
