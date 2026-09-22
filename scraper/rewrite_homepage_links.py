import re

with open('frontend/public/index_replica.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace exact base domain links
html = re.sub(r'href="https://www\.sharda\.ac\.in/?"', 'href="/"', html)
html = re.sub(r'href="https://sharda\.ac\.in/?"', 'href="/"', html)

# Replace all internal sharda.ac.in links
html = re.sub(r'href="https://www\.sharda\.ac\.in/([^"]*)"', r'href="/\1"', html)
html = re.sub(r'href="https://sharda\.ac\.in/([^"]*)"', r'href="/\1"', html)

# Replace internal subdomains
html = re.sub(r'href="https://suat\.sharda\.ac\.in/?([^"]*)"', r'href="/suat/\1"', html)
html = re.sub(r'href="https://alumni\.sharda\.ac\.in/?([^"]*)"', r'href="/alumni/\1"', html)
html = re.sub(r'href="https://medical\.sharda\.ac\.in/?([^"]*)"', r'href="/medical/\1"', html)
html = re.sub(r'href="https://dental\.sharda\.ac\.in/?([^"]*)"', r'href="/dental/\1"', html)
html = re.sub(r'href="https://admissions\.sharda\.ac\.in/phd/?([^"]*)"', r'href="/admissions/phd"', html)

# Clean up trailing /suat// or double slashes
html = html.replace('href="/suat/"', 'href="/suat"')
html = html.replace('href="/alumni/"', 'href="/alumni"')
html = html.replace('href="/medical/"', 'href="/medical"')
html = html.replace('href="/dental/"', 'href="/dental"')
html = html.replace('href="//', 'href="/')

with open('frontend/public/index_replica.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Rewrote index_replica.html links to internal relative URLs!")
