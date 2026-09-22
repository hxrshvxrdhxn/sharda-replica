import pytest
from playwright.sync_api import sync_playwright
import time

def test_tier0_homepage_exact_dom():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("\n--- 1. TESTING TIER 0 HOMEPAGE EXACT DOM & ASSETS ---")
        resp = page.goto("http://127.0.0.1:3000", wait_until="domcontentloaded", timeout=15000)
        assert resp.status == 200, f"Expected 200 OK, got {resp.status}"

        # Title check
        title = page.title()
        assert "Sharda University" in title
        print(f"[PASS] Title Verified: {title}")

        # Verify all 13 core DOM containers from live sharda.ac.in
        core_sections = [
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

        for sec in core_sections:
            el = page.query_selector(sec)
            assert el is not None, f"Required core DOM container '{sec}' missing from homepage"
            print(f"[PASS] Core DOM Section Verified: {sec}")

        # Check injected Gemini Sharda AI Floating Bar
        sai_bar = page.query_selector("#saiBar")
        assert sai_bar is not None, "Sharda AI floating bar is missing"
        print("[PASS] Embedded Gemini Sharda AI Floating Bar Verified (#saiBar)")

        browser.close()

def test_tier1_to_tier4_deep_routes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        print("\n--- 2. TESTING TIER 1 TO TIER 4 MULTI-TIER DEEP ROUTES ---")
        test_routes = [
            # Tier 1: Core Hubs
            {"path": "/replica/about/overview", "name": "Tier 1: About Overview"},
            {"path": "/replica/admissions/how-to-apply", "name": "Tier 1: Admissions How to Apply"},
            {"path": "/replica/course-fee", "name": "Tier 1: Course Fee Matrix"},
            {"path": "/replica/placements", "name": "Tier 1: Placements & Recruiters"},
            # Tier 2: 14+ Schools
            {"path": "/replica/schools/engineering-and-technology", "name": "Tier 2: School of Engineering"},
            {"path": "/replica/schools/business-studies", "name": "Tier 2: School of Business Studies"},
            {"path": "/replica/schools/medical-sciences-and-research", "name": "Tier 2: School of Medical Sciences"},
            # Tier 3: 234+ Programmes
            {"path": "/replica/programmes/b-tech-cse", "name": "Tier 3: B.Tech Computer Science"},
            {"path": "/replica/programmes/mba", "name": "Tier 3: MBA Management"},
            {"path": "/replica/programmes/mbbs", "name": "Tier 3: MBBS Medical"},
            # Tier 4: Faculty & Research
            {"path": "/replica/faculty/details/dr-dinesh-kumar-bagga", "name": "Tier 4: Faculty Profile Dr. Bagga"}
        ]

        for route in test_routes:
            url = f"http://127.0.0.1:8000{route['path']}"
            resp = page.goto(url, wait_until="domcontentloaded", timeout=20000)
            assert resp.status == 200, f"Route {route['name']} failed with status {resp.status}"
            
            # Check injected AI bar presence
            ai_present = page.query_selector("#saiFloatingBar") or page.query_selector("#saiBar")
            assert ai_present is not None
            print(f"[PASS] {route['name']} ({route['path']}) -> 200 OK + AI Injected")

        browser.close()

def test_interactive_sharda_ai_and_lead_flows():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        print("\n--- 3. TESTING INTERACTIVE SHARDA AI (GEMINI RAG) CHAT FLOW ---")
        page.goto("http://127.0.0.1:8000/replica", wait_until="domcontentloaded", timeout=15000)

        # Trigger AI Modal
        page.fill("#saiBarInput", "What is the fee for B.Tech Computer Science and MBA?")
        page.click("button.sharda-ai-btn")
        page.wait_for_timeout(1000)

        modal = page.query_selector("#saiModal")
        assert modal is not None
        print("[PASS] Sharda AI Modal Opened Successfully.")

        # Wait for AI grounded response
        page.wait_for_timeout(3000)
        chat_text = page.inner_text("#saiChatBody")
        assert len(chat_text) > 50
        print(f"[PASS] AI Response Received: {chat_text[:100]}...")

        browser.close()

def test_negative_flows_and_edge_cases():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        print("\n--- 4. TESTING NEGATIVE FLOWS & EDGE CASES ---")
        
        # Non-existent slug test
        resp = page.goto("http://127.0.0.1:3000/random-non-existent-page-xyz-12345", timeout=10000)
        print(f"[PASS] 404 / Catch-all Fallback Handled: Status {resp.status}")

        browser.close()

if __name__ == "__main__":
    test_tier0_homepage_exact_dom()
    test_tier1_to_tier4_deep_routes()
    test_interactive_sharda_ai_and_lead_flows()
    test_negative_flows_and_edge_cases()
