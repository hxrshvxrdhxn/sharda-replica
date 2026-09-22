import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.on('console', lambda msg: print(f'CONSOLE: {msg.type}: {msg.text}'))
        page.on('pageerror', lambda err: print(f'PAGE ERROR: {err}'))
        
        print('Navigating to http://localhost:3000...')
        await page.goto('http://localhost:3000', wait_until='networkidle')
        
        # Check elements
        hero_input = page.locator('#turboSearchInput')
        print(f'#turboSearchInput count: {await hero_input.count()}')
        
        send_btns = page.locator('.turbo-ai-search-bar button')
        btn_count = await send_btns.count()
        print(f'Search bar buttons count: {btn_count}')
        for i in range(btn_count):
            btn = send_btns.nth(i)
            txt = await btn.inner_text()
            cls = await btn.get_attribute('class')
            print(f'Button {i}: text="{txt}", class="{cls}"')
            
        # Try filling input and clicking
        await hero_input.fill('When do B.Tech CSE 2026 admissions close?')
        
        # Click the action button
        btn = page.locator('.turbo-ai-action-btn').first
        await btn.click()
        
        await page.wait_for_timeout(3000)
        
        modal = page.locator('#turboModal')
        print(f'Modal visible: {await modal.is_visible()}')
        
        chat_body = page.locator('#turboChatBody')
        print(f'Chat body text:\n{await chat_body.inner_text()}')
        
        await page.screenshot(path="button_diag.png")
        await browser.close()

asyncio.run(run())
