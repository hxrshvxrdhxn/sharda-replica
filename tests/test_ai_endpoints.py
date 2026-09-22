import asyncio
import httpx
import time
import sys

sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

async def test():
    urls = ['http://127.0.0.1:8000/api/v1/ai/chat', 'http://localhost:3000/api/v1/ai/chat']
    queries = [
        'can do llm after 12th',
        'what scholarship do I get with 88% in 12th',
        'when do admissions close for 2026',
        'compare btech cse and mba fees'
    ]
    for url in urls:
        print(f"\n=== Testing {url} ===")
        for q in queries:
            t0 = time.time()
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    res = await client.post(url, json={'query': q})
                    t1 = time.time()
                    print(f"[{res.status_code}] ({t1-t0:.2f}s) Q: '{q}'")
                    if res.status_code == 200:
                        data = res.json()
                        resp = data.get('response') or data.get('answer') or ''
                        print(f"   Resp snippet: {resp[:140].strip()}...")
                        print(f"   Follow-ups: {data.get('suggested_followups', [])[:2]}")
                        print(f"   Model: {data.get('model', '')} | Powered By: {data.get('powered_by', '')}")
                    else:
                        print(f"   Error: {res.text[:200]}")
            except Exception as e:
                print(f"   Exception: {e}")

if __name__ == '__main__':
    asyncio.run(test())
