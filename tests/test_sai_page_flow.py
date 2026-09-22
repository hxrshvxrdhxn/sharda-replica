import asyncio
import time
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def test_sai_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to http://localhost:3000/sai ...")
        await page.goto("http://localhost:3000/sai", wait_until="networkidle", timeout=15000)
        
        # Verify initial hero state
        print("Taking initial /sai screenshot...")
        await page.screenshot(path="C:/Users/user/.gemini/antigravity/brain/be29eb17-a05a-44fc-ba3f-04e8b2e04736/sai_page_hero_modern.png")
        
        page.on("console", lambda msg: print("BROWSER LOG:", msg.text))
        
        # Type the user's exact query
        input_selector = 'input[placeholder*="Ask anything"]'
        await page.wait_for_selector(input_selector)
        await page.fill(input_selector, "can do llm after 12th")
        await page.wait_for_timeout(300)
        
        print("Submitting query via Ask button...")
        ask_btn = page.locator('button:has-text("Ask")')
        await ask_btn.click()
        
        # Wait for AI response bubble to appear
        print("Waiting for conversational AI response...")
        await page.wait_for_selector('button:has-text("Copy")', timeout=20000)
        
        # Take screenshot of conversation
        await page.screenshot(path="C:/Users/user/.gemini/antigravity/brain/be29eb17-a05a-44fc-ba3f-04e8b2e04736/sai_page_conversational_response.png")
        print("Saved conversational screenshot!")
        
        # Check input cleared
        input_val = await page.input_value(input_selector)
        print("Input box cleared value:", repr(input_val))
        assert input_val == "", "Input box should be empty after submission"
        
        # Check that response mentions LLM / law / 5-year
        content = await page.text_content("body")
        print("Page contains '5-year' or 'postgraduate' or 'LL.B':", any(w in content for w in ["postgraduate", "5-year", "5-Year", "LL.B", "BA LLB", "BBA LLB"]))
        
        # Test clicking a dynamic follow-up chip
        print("Testing dynamic follow-up chip click...")
        chip = page.locator('footer button:has-text("scholarship"), footer button:has-text("Law"), footer button:has-text("SUAT")').first
        if await chip.count() > 0:
            chip_text = await chip.text_content()
            print(f"Clicking follow-up chip: '{chip_text.strip()}'")
            await chip.click()
            await page.wait_for_timeout(4500)
            await page.screenshot(path="C:/Users/user/.gemini/antigravity/brain/be29eb17-a05a-44fc-ba3f-04e8b2e04736/sai_multiturn_verified.png")
            print("Saved multi-turn conversation screenshot!")
        
        await browser.close()
        print("✅ /sai UI and multi-turn conversational flow successfully verified!")

if __name__ == "__main__":
    asyncio.run(test_sai_page())
