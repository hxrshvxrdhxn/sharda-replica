from bs4 import BeautifulSoup
from urllib.parse import urlparse

with open('frontend/public/index_replica.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

footer = soup.select_one('#footer')
links = footer.find_all('a')

print(f"Total links in #footer: {len(links)}")

sharda_links = []
external_links = []

for i, a in enumerate(links):
    href = a.get('href', '').strip()
    text = a.get_text(strip=True)
    target = a.get('target', '')
    
    parsed = urlparse(href)
    netloc = parsed.netloc.lower()
    
    if 'sharda.ac.in' in netloc or netloc == '' or href.startswith('/'):
        sharda_links.append((text, href, parsed.path))
        print(f"[SHARDA] {i+1:3d}. [{text[:30]:<30}] -> {href}")
    else:
        external_links.append((text, href))
        print(f"[EXT]    {i+1:3d}. [{text[:30]:<30}] -> {href}")

print(f"\nSummary: {len(sharda_links)} Sharda links, {len(external_links)} External links in #footer.")
