import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "scraper" / "output" / "audit_screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

async def audit_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})

        # 1. Inspect Live Sharda.ac.in
        live_page = await context.new_page()
        live_console_errors = []
        live_failed_requests = []
        live_page.on("console", lambda msg: live_console_errors.append(msg.text) if msg.type == "error" else None)
        live_page.on("requestfailed", lambda req: live_failed_requests.append(req.url))

        print("Navigating to live https://www.sharda.ac.in...")
        try:
            await live_page.goto("https://www.sharda.ac.in", wait_until="networkidle", timeout=30000)
            await live_page.screenshot(path=str(SCREENSHOTS_DIR / "live_sharda_homepage.png"), full_page=True)
            print(f"Saved live screenshot to {SCREENSHOTS_DIR / 'live_sharda_homepage.png'}")
        except Exception as e:
            print(f"Error visiting live page: {e}")

        # 2. Inspect Local Homepage (port 3000)
        local_page = await context.new_page()
        local_console_errors = []
        local_failed_requests = []
        local_page.on("console", lambda msg: local_console_errors.append(msg.text) if msg.type == "error" else None)
        local_page.on("requestfailed", lambda req: local_failed_requests.append(f"{req.url} -> {req.failure}"))

        print("Navigating to local http://127.0.0.1:3000...")
        try:
            await local_page.goto("http://127.0.0.1:3000", wait_until="networkidle", timeout=20000)
            await local_page.screenshot(path=str(SCREENSHOTS_DIR / "local_sharda_homepage.png"), full_page=True)
            print(f"Saved local screenshot to {SCREENSHOTS_DIR / 'local_sharda_homepage.png'}")
        except Exception as e:
            print(f"Error visiting local page: {e}")

        print("\n--- AUDIT FINDINGS ---")
        print(f"Local Console Errors ({len(local_console_errors)}):")
        for err in local_console_errors[:10]:
            print(f"  [Error] {err}")

        print(f"\nLocal Failed Network Requests ({len(local_failed_requests)}):")
        for req in local_failed_requests[:15]:
            print(f"  [404/Failed] {req}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit_page())
