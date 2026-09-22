from playwright.sync_api import sync_playwright
import time

def test_interactive_chat():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        print("Navigating to http://127.0.0.1:3000/...")
        page.goto("http://127.0.0.1:3000/", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        # 1. Fill input with 'hi'
        inp = page.locator("#turboSearchInput")
        inp.fill("hi")
        
        # 2. Click the 'Ask Sharda AI' button
        btn = page.locator(".turbo-ai-action-btn").first
        btn.click()
        
        page.wait_for_timeout(4000)
        
        # 3. Assert modal is visible
        modal = page.locator("#turboModal")
        is_vis = modal.is_visible()
        print(f"Modal is visible: {is_vis}")
        assert is_vis, "Modal failed to open!"
        
        # 4. Check URL has not changed or redirected
        print(f"URL: {page.url}")
        assert "sharda.ac.in" not in page.url
        
        # 5. Extract answer text
        body_text = page.locator("#turboChatBody").inner_text()
        print("--- Chat Body Snippet ---")
        print(body_text.encode("ascii", errors="replace").decode("ascii")[:400])
        
        # 6. Test follow-up question in modal
        modal_inp = page.locator("#turboModalInput")
        modal_inp.fill("What is the fee for B.Tech CSE AI/ML?")
        modal_inp.press("Enter")
        
        page.wait_for_timeout(4000)
        updated_body = page.locator("#turboChatBody").inner_text()
        print("--- Follow-up Chat Snippet ---")
        print(updated_body.encode("ascii", errors="replace").decode("ascii")[-500:])
        
        page.screenshot(path="local_verified_chat_success.png")
        print("Screenshot saved to local_verified_chat_success.png")
        browser.close()

if __name__ == "__main__":
    test_interactive_chat()
