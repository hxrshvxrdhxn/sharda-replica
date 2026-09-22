import asyncio
from playwright.async_api import async_playwright
import json

async def compare_sections():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})

        live_page = await context.new_page()
        await live_page.goto("https://www.sharda.ac.in", wait_until="networkidle", timeout=35000)

        local_page = await context.new_page()
        await local_page.goto("http://127.0.0.1:3000", wait_until="networkidle", timeout=20000)

        sections = [
            "#header",
            ".jainslider",
            "#featured-list",
            "#campus-short-info",
            "#impact",
            "#global-students",
            "#featured-section",
            "#latest-news",
            "#testimonials2",
            "#company-hiring",
            "#read-faq",
            "#footer"
        ]

        print(f"{'Section Selector':<25} | {'Live Height (px)':<18} | {'Local Height (px)':<18} | {'Diff (px)':<10}")
        print("-" * 75)

        for sec in sections:
            live_el = await live_page.query_selector(sec)
            local_el = await local_page.query_selector(sec)

            live_box = await live_el.bounding_box() if live_el else None
            local_box = await local_el.bounding_box() if local_el else None

            live_h = round(live_box["height"], 1) if live_box else "MISSING"
            local_h = round(local_box["height"], 1) if local_box else "MISSING"
            
            diff = round(abs(live_h - local_h), 1) if (isinstance(live_h, (int, float)) and isinstance(local_h, (int, float))) else "N/A"

            print(f"{sec:<25} | {str(live_h):<18} | {str(local_h):<18} | {str(diff):<10}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(compare_sections())
