import asyncio
from playwright.async_api import async_playwright
import os

async def audit_navigation():
    os.makedirs('scraper/output/nav_audit', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page_live = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_live.goto('https://www.sharda.ac.in', wait_until='networkidle')
        
        page_local = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_local.goto('http://127.0.0.1:3000', wait_until='networkidle')
        
        # Test 1: Desktop Navigation Menu Items
        live_items = await page_live.evaluate('''() => {
            return Array.from(document.querySelectorAll('#main-navigation > ul > li')).map(li => {
                const a = li.querySelector(':scope > a');
                const sub = li.querySelector('.sub-menu, .dropdown-menu');
                return {
                    title: a ? a.innerText.trim() : '',
                    hasSubmenu: !!sub,
                    subLinksCount: sub ? sub.querySelectorAll('a').length : 0
                };
            });
        }''')
        
        local_items = await page_local.evaluate('''() => {
            return Array.from(document.querySelectorAll('#main-navigation > ul > li')).map(li => {
                const a = li.querySelector(':scope > a');
                const sub = li.querySelector('.sub-menu, .dropdown-menu');
                return {
                    title: a ? a.innerText.trim() : '',
                    hasSubmenu: !!sub,
                    subLinksCount: sub ? sub.querySelectorAll('a').length : 0
                };
            });
        }''')
        
        print("=== HEADER MAIN NAVIGATION AUDIT ===")
        print(f"{'Item Index':<10} | {'Live Nav Title (Links)':<30} | {'Local Nav Title (Links)':<30} | {'Match'}")
        print("-" * 80)
        
        for i in range(max(len(live_items), len(local_items))):
            l_item = live_items[i] if i < len(live_items) else {'title': 'N/A', 'subLinksCount': 0}
            loc_item = local_items[i] if i < len(local_items) else {'title': 'N/A', 'subLinksCount': 0}
            match = "PASS" if l_item['title'] == loc_item['title'] and l_item['subLinksCount'] == loc_item['subLinksCount'] else "DIFF"
            print(f"{i:<10} | {l_item['title'] + ' (' + str(l_item['subLinksCount']) + ')':<30} | {loc_item['title'] + ' (' + str(loc_item['subLinksCount']) + ')':<30} | {match}")
            
        # Test 2: Hover over each nav item and take screenshots
        print("\n=== HOVERING MENU ITEMS & TAKING SCREENSHOTS ===")
        for i in range(min(len(live_items), len(local_items))):
            title = live_items[i]['title'].replace(' ', '_').replace('/', '_').lower()
            if not title:
                continue
            
            # Live Hover
            live_li = page_live.locator(f'#main-navigation > ul > li:nth-child({i+1})')
            if await live_li.count() > 0:
                await live_li.hover()
                await page_live.wait_for_timeout(300)
                await page_live.screenshot(path=f'scraper/output/nav_audit/live_hover_{i}_{title}.png')
                
            # Local Hover
            local_li = page_local.locator(f'#main-navigation > ul > li:nth-child({i+1})')
            if await local_li.count() > 0:
                await local_li.hover()
                await page_local.wait_for_timeout(300)
                await page_local.screenshot(path=f'scraper/output/nav_audit/local_hover_{i}_{title}.png')
                print(f"[HOVER TEST] Menu item {i}: '{title}' hovered and screenshotted.")
                
        # Test 3: Search Bar Interaction
        print("\n=== SEARCH BAR INTERACTION TEST ===")
        search_icon_live = page_live.locator('#search-link, .search-icon, .search-btn, a[href*="search"]')
        search_icon_local = page_local.locator('#search-link, .search-icon, .search-btn, a[href*="search"]')
        
        live_search_count = await search_icon_live.count()
        local_search_count = await search_icon_local.count()
        print(f"Search icon count: Live={live_search_count}, Local={local_search_count}")
        
        # Test 4: Mobile Navigation (Viewport 375x667)
        print("\n=== MOBILE NAVIGATION DRAWER TEST ===")
        mob_context = await browser.new_context(viewport={'width': 375, 'height': 667})
        mob_live = await mob_context.new_page()
        await mob_live.goto('https://www.sharda.ac.in', wait_until='networkidle')
        await mob_live.screenshot(path='scraper/output/nav_audit/live_mobile_home.png')
        
        mob_local = await mob_context.new_page()
        await mob_local.goto('http://127.0.0.1:3000', wait_until='networkidle')
        await mob_local.screenshot(path='scraper/output/nav_audit/local_mobile_home.png')
        
        # Click mobile hamburger menu toggle
        mob_btn_live = mob_live.locator('.navbar-toggle, .menu-toggle, #sidebaropenleft, button[data-toggle="collapse"], .mobile-nav-toggle')
        mob_btn_local = mob_local.locator('.navbar-toggle, .menu-toggle, #sidebaropenleft, button[data-toggle="collapse"], .mobile-nav-toggle')
        
        if await mob_btn_local.count() > 0:
            await mob_btn_local.first.click()
            await mob_local.wait_for_timeout(500)
            await mob_local.screenshot(path='scraper/output/nav_audit/local_mobile_opened.png')
            print("[MOBILE TEST] Local mobile drawer opened and screenshotted.")
            
        if await mob_btn_live.count() > 0:
            await mob_btn_live.first.click()
            await mob_live.wait_for_timeout(500)
            await mob_live.screenshot(path='scraper/output/nav_audit/live_mobile_opened.png')
            print("[MOBILE TEST] Live mobile drawer opened and screenshotted.")
            
        await browser.close()
        print("\nAll navigation audits completed successfully!")

if __name__ == '__main__':
    asyncio.run(audit_navigation())
