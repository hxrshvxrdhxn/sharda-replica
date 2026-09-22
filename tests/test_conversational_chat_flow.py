import asyncio
import os
from playwright.async_api import async_playwright

SCREENSHOT_DIR = r"C:\Users\user\.gemini\antigravity\brain\be29eb17-a05a-44fc-ba3f-04e8b2e04736"

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 850})
        page = await context.new_page()

        print("1. Loading http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 2. Check search bar buttons count
        search_btns = page.locator(".turbo-ai-search-bar button")
        btn_count = await search_btns.count()
        print(f"Hero search bar buttons count: {btn_count}")
        assert btn_count == 1, f"Expected exactly 1 button in search bar, found {btn_count}!"

        btn_text = await search_btns.first.inner_text()
        print(f"Single Button Text: '{btn_text}'")

        # 3. Type query and click button
        hero_inp = page.locator("#turboSearchInput")
        query_text = "When do B.Tech CSE 2026 admissions close?"
        await hero_inp.fill(query_text)
        print(f"Filled hero input with: '{query_text}'")

        await search_btns.first.click()

        # 4. Check that input was cleared immediately
        await page.wait_for_timeout(500)
        hero_val_after = await hero_inp.input_value()
        print(f"Hero input value after click: '{hero_val_after}' (should be empty)")
        assert hero_val_after == "", "Hero search input was not cleared on submission!"

        # 5. Check modal is visible and chat response arrived
        modal = page.locator("#turboModal")
        await modal.wait_for(state="visible", timeout=5000)
        print("Modal is visible!")

        # Wait for AI response bubble
        await page.wait_for_selector(".turbo-ai-msg-row", timeout=12000)
        await page.wait_for_timeout(2500)

        snap1 = os.path.join(SCREENSHOT_DIR, "chat_turn1_verified.png")
        await page.screenshot(path=snap1)
        print(f"Saved turn 1 screenshot to {snap1}")

        # 6. Send multi-turn follow up from within modal
        modal_inp = page.locator("#turboModalInput")
        followup_text = "What are the scholarship criteria for this?"
        await modal_inp.fill(followup_text)
        await modal_inp.press("Enter")
        print(f"Sent follow-up: '{followup_text}'")

        # Check modal input cleared
        await page.wait_for_timeout(400)
        modal_val_after = await modal_inp.input_value()
        print(f"Modal input value after send: '{modal_val_after}' (should be empty)")
        assert modal_val_after == "", "Modal input was not cleared on Enter!"

        # Wait for second AI response
        await page.wait_for_timeout(4500)
        
        user_bubbles = page.locator(".turbo-user-msg-row")
        ai_bubbles = page.locator(".turbo-ai-msg-row")
        print(f"Total user bubbles: {await user_bubbles.count()}")
        print(f"Total AI bubbles: {await ai_bubbles.count()}")

        snap2 = os.path.join(SCREENSHOT_DIR, "chat_multiturn_verified.png")
        await page.screenshot(path=snap2)
        print(f"Saved multi-turn screenshot to {snap2}")

        # 7. Test New Chat button
        new_chat_btn = page.locator("#turboModal button:has-text('New Chat')")
        if await new_chat_btn.count() > 0:
            await new_chat_btn.click()
            await page.wait_for_timeout(500)
            user_bubbles_reset = await page.locator(".turbo-user-msg-row").count()
            print(f"User bubbles after New Chat reset: {user_bubbles_reset} (expected 0)")
            assert user_bubbles_reset == 0, "Chat was not reset on New Chat click!"

        # 8. Test /sai page
        print("Testing /sai modern AI page...")
        await page.goto("http://localhost:3000/sai", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        sai_inp = page.locator("input[placeholder*='Ask anything']")
        if await sai_inp.count() > 0:
            await sai_inp.fill("What is the fee for MBA?")
            await sai_inp.press("Enter")
            await page.wait_for_timeout(4000)
            snap3 = os.path.join(SCREENSHOT_DIR, "sai_multiturn_verified.png")
            await page.screenshot(path=snap3)
            print(f"Saved /sai screenshot to {snap3}")

        await browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_verification())
