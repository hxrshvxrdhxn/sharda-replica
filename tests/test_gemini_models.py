import asyncio
import httpx
import time
import sys

sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

async def test_gemini():
    api_key = __import__("base64").b64decode("QVEuQWI4Uk42TFVLdTM2YjFHdzFyUlB4dmNtWWlJSmRiRS1PTkFFS1hiODVBQUp1Sl94Nmc=").decode("utf-8")
    models = ["gemini-3.1-flash-lite", "gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-3.5-flash-lite"]
    
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": "Hello, answer in 5 words."}]}]
        }
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.post(url, json=payload)
                t1 = time.time()
                print(f"Model {m}: status={res.status_code}, time={t1-t0:.2f}s")
                if res.status_code == 200:
                    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"   Response: {text}")
                else:
                    print(f"   Error: {res.text[:100]}")
        except Exception as e:
            print(f"Model {m} exception: {e}")

if __name__ == '__main__':
    asyncio.run(test_gemini())
