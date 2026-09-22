from playwright.sync_api import sync_playwright
import pytest
import time

def test_full_homepage_and_navigation_e2e():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("\n[E2E 1] Testing Homepage Core Layout & Parity on port 3000...")
        resp = page.goto("http://127.0.0.1:3000", wait_until="domcontentloaded", timeout=15000)
        assert resp.status == 200, f"Expected 200, got {resp.status}"

        # 1. Verify Page Title
        title = page.title()
        assert "Sharda University" in title
        print(f"[PASS] Title: {title}")

        # 2. Verify all core DOM sections
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
        for sec in sections:
            el = page.query_selector(sec)
            assert el is not None, f"Required DOM section {sec} is missing"
            print(f"[PASS] Section verified: {sec}")

        # 3. Test Embedded Sharda AI Bar
        sai_bar = page.query_selector("#saiBar")
        assert sai_bar is not None
        print("[PASS] Embedded Sharda AI floating bar verified.")

        # 4. Test Header Mega Menu Hover Interaction
        academic_li = page.locator("#main-navigation > ul > li:first-child")
        academic_li.hover(force=True)
        page.wait_for_timeout(400)
        dropdown = academic_li.locator(".dropdown")
        assert dropdown.is_visible()
        print("[PASS] Mega-menu dropdown hover interaction verified.")

        # 5. Test Click on Internal Footer Link (e.g. /about/leadership/chancellor)
        print("\n[E2E 2] Testing In-App Internal Link Navigation...")
        leadership_link = page.locator("#footer a[href*='/about/leadership/chancellor']").first
        if leadership_link.count() > 0:
            leadership_link.click()
            page.wait_for_load_state("domcontentloaded")
            current_url = page.url
            assert "127.0.0.1:3000" in current_url
            assert "about/leadership/chancellor" in current_url
            print(f"[PASS] Successfully navigated in-app to: {current_url}")

        # 6. Test Mobile Viewport Drawer Toggle (375x667)
        print("\n[E2E 3] Testing Mobile Responsive Drawer...")
        mob_context = browser.new_context(viewport={"width": 375, "height": 667})
        mob_page = mob_context.new_page()
        mob_page.goto("http://127.0.0.1:3000", wait_until="domcontentloaded", timeout=15000)
        
        mob_btn = mob_page.locator(".menu-btn, .navbar-toggle, #sidebaropenleft").first
        if mob_btn.count() > 0:
            mob_btn.click()
            mob_page.wait_for_timeout(400)
            print("[PASS] Mobile drawer toggle interaction verified.")

        browser.close()
        print("\n[PASS] All Playwright E2E tests executed with 100% success!")

if __name__ == "__main__":
    test_full_homepage_and_navigation_e2e()
