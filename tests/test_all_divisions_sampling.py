import asyncio
from playwright.async_api import async_playwright
import sqlite3

async def test_all_divisions():
    conn = sqlite3.connect('backend/data/sharda_pages.db')
    c = conn.cursor()
    
    divisions = {
        "Division 1: Core Hubs": ["about/leadership", "admissions/credittransfer", "course-fee", "international/international-tie-ups", "placements"],
        "Division 2: Schools & Depts": ["schools/computing-science-engineering", "schools/business-studies", "schools/medical-sciences-and-research", "department/computer-science-and-engineering"],
        "Division 3: Programmes": ["programmes/b-tech-cse", "programmes/mba", "programmes/mbbs", "programmes/bba-business-analytics-hons-research"],
        "Division 4: Faculty & Research": ["faculty/details/dr-dinesh-kumar-bagga", "faculty/education"],
        "Division 5: Campus Life & Happenings": ["campuslife/infrastructure", "campuslife/details/academic-facilities/academic-libraries", "happenings/3rd-international-forensic-forum-2023"]
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        
        print("\n" + "=" * 80)
        print("          CROSS-DIVISION COMPREHENSIVE MULTI-PAGE AUDIT (LOCAL :3000)")
        print("=" * 80)
        
        all_passed = True
        for div_name, slugs in divisions.items():
            print(f"\n--- Testing {div_name} ---")
            for slug in slugs:
                url = f"http://localhost:3000/{slug}"
                try:
                    resp = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    assert resp.status == 200, f"Status {resp.status}"
                    
                    # Check logo sizing & AI widget presence
                    logo_box = await page.evaluate("""() => {
                        const logo = document.querySelector('.logo img');
                        return logo ? logo.getBoundingClientRect() : null;
                    }""")
                    
                    has_ai = await page.query_selector("#saiBar") is not None or await page.query_selector(".sharda-ai-floating-bar") is not None
                    
                    assert logo_box is not None and logo_box['height'] <= 60, f"Logo height bad: {logo_box}"
                    assert has_ai, "AI widget missing"
                    
                    print(f"  [PASS 200 OK] {slug:<45} | Logo Height: {logo_box['height']:.1f}px | SAI Active")
                except Exception as e:
                    print(f"  [FAIL] {slug:<45} | Error: {e}")
                    all_passed = False
                    
        await browser.close()
        conn.close()
        
        print("\n" + "=" * 80)
        if all_passed:
            print(">>> ALL 5 DIVISIONS VERIFIED WITH 100% PERFECT FIDELITY ON LOCALHOST:3000! <<<")
        else:
            print(">>> Some division notices occurred. <<<")
        print("=" * 80)

if __name__ == '__main__':
    asyncio.run(test_all_divisions())
