from playwright.sync_api import sync_playwright
import pytest

def test_replica_routes_and_backend_rag_e2e():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        print("\n[E2E Backend/Replica] Testing Core Replica Routes...")
        test_paths = [
            "/replica",
            "/replica/about/overview",
            "/replica/admissions/how-to-apply",
            "/replica/course-fee",
            "/replica/schools/engineering-and-technology",
            "/replica/schools/business-studies",
            "/replica/schools/medical-sciences-and-research",
            "/replica/programmes/b-tech-cse",
            "/replica/faculty/details/dr-dinesh-kumar-bagga"
        ]

        for path in test_paths:
            url = f"http://127.0.0.1:8000{path}"
            resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
            assert resp.status == 200, f"Failed on {url} with status {resp.status}"
            
            # Check AI widget presence
            ai_widget = page.query_selector("#saiBar") or page.query_selector(".sharda-ai-floating-bar")
            assert ai_widget is not None
            print(f"[PASS] Route: {path} -> 200 OK + AI Counselor Injected")

        # Test Interactive Gemini RAG Query
        print("\n[E2E AI Brain] Testing Real-Time Conversational AI Response...")
        page.goto("http://127.0.0.1:8000/replica", wait_until="domcontentloaded")
        page.fill("#saiBarInput", "What are the B.Tech Computer Science fees and scholarships?")
        page.click("button.sharda-ai-btn")
        page.wait_for_timeout(2500)

        response_body = page.inner_text("#saiChatBody")
        assert len(response_body) > 30
        assert "Sharda" in response_body
        print(f"[PASS] Gemini RAG Counselor Response Verified: {response_body[:90]}...")

        browser.close()
        print("\n[PASS] All Replica & Backend E2E tests executed with 100% success!")

if __name__ == "__main__":
    test_replica_routes_and_backend_rag_e2e()
