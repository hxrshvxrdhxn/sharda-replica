import asyncio
from playwright.async_api import async_playwright
import os

ARTIFACT_DIR = r"C:\Users\user\.gemini\antigravity\brain\be29eb17-a05a-44fc-ba3f-04e8b2e04736"

async def run_visual_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        
        # 1. Homepage Top & Header Inspection
        page = await context.new_page()
        print("Testing Homepage: http://localhost:3000")
        await page.goto("http://localhost:3000", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)
        
        # Check Strip & Header geometry
        geo = await page.evaluate("""() => {
            const strip = document.querySelector('#strip');
            const header = document.querySelector('#header');
            const logo = document.querySelector('.logo img:not([style*="display: none"])');
            return {
                strip_box: strip ? strip.getBoundingClientRect() : null,
                header_box: header ? header.getBoundingClientRect() : null,
                logo_box: logo ? logo.getBoundingClientRect() : null
            };
        }""")
        print("Homepage Geometry:", geo)
        
        # Take screenshot of homepage top
        home_shot = os.path.join(ARTIFACT_DIR, "homepage_top_fixed.png")
        await page.screenshot(path=home_shot, full_page=False)
        print(f"Saved homepage screenshot to: {home_shot}")

        # 2. Subpage: Course Fee (/course-fee)
        print("\nTesting Course Fee: http://localhost:3000/course-fee")
        await page.goto("http://localhost:3000/course-fee", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)
        
        cf_geo = await page.evaluate("""() => {
            const logo = document.querySelector('.logo img:not([style*="display: none"])');
            const content = document.querySelector('#content, .blue-theme, main, body');
            return {
                logo_box: logo ? logo.getBoundingClientRect() : null,
                has_tables: document.querySelectorAll('table, .table').length,
                has_nav: !!document.querySelector('#header, header')
            };
        }""")
        print("Course-Fee Geometry & Elements:", cf_geo)
        
        cf_shot = os.path.join(ARTIFACT_DIR, "course_fee_page.png")
        await page.screenshot(path=cf_shot, full_page=False)
        print(f"Saved course-fee screenshot to: {cf_shot}")

        # 3. Subpage: Credit Transfer (/admissions/credittransfer)
        print("\nTesting Credit Transfer: http://localhost:3000/admissions/credittransfer")
        await page.goto("http://localhost:3000/admissions/credittransfer", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)
        
        ct_geo = await page.evaluate("""() => {
            const logo = document.querySelector('.logo img:not([style*="display: none"])');
            const headings = Array.from(document.querySelectorAll('h1, h2')).map(h => h.innerText.trim());
            return {
                logo_box: logo ? logo.getBoundingClientRect() : null,
                headings: headings.slice(0, 5)
            };
        }""")
        print("Credit-Transfer Elements:", ct_geo)
        
        ct_shot = os.path.join(ARTIFACT_DIR, "credit_transfer_page.png")
        await page.screenshot(path=ct_shot, full_page=False)
        print(f"Saved credit-transfer screenshot to: {ct_shot}")

        # 4. Subpage: Computer Science (/schools/computing-science-engineering)
        print("\nTesting School CSE: http://localhost:3000/schools/computing-science-engineering")
        await page.goto("http://localhost:3000/schools/computing-science-engineering", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)
        
        cse_shot = os.path.join(ARTIFACT_DIR, "cse_school_page.png")
        await page.screenshot(path=cse_shot, full_page=False)
        print(f"Saved CSE school screenshot to: {cse_shot}")

        await browser.close()
        print("\nALL VISUAL TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_visual_verification())
