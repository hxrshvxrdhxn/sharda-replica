import asyncio
from playwright.async_api import async_playwright

async def debug_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("console", lambda msg: print("BROWSER LOG:", msg.text))
        page.on("pageerror", lambda err: print("PAGE ERROR:", err))
        
        await page.goto("http://localhost:3000/sai", wait_until="networkidle")
        
        # Click on one of the starter cards directly: "B.Tech CSE & AI Specialisations"
        print("Clicking B.Tech starter card...")
        card = page.locator('button:has-text("B.Tech CSE & AI Specialisations")')
        await card.click()
        
        print("Waiting 10s for response generation...")
        await page.wait_for_timeout(10000)
        
        await page.screenshot(path="C:/Users/user/.gemini/antigravity/brain/be29eb17-a05a-44fc-ba3f-04e8b2e04736/sai_completed_counselor.png")
        print("Saved completed counselor screenshot!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_test())
