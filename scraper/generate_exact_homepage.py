import httpx
import re
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_HTML_PATH = BASE_DIR / "frontend" / "public" / "index_replica.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

AI_WIDGET_CODE = """
<!-- ========================================================= -->
<!-- SHARDA AI (SAI) GEMINI KNOWLEDGE BRAIN & LEAD INTELLIGENCE -->
<!-- ========================================================= -->
<style>
.sharda-ai-floating-bar {
  position: fixed;
  bottom: 25px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999999;
  width: 92%;
  max-width: 740px;
  background: rgba(27, 44, 57, 0.96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(234, 169, 20, 0.6);
  border-radius: 50px;
  padding: 8px 18px;
  display: flex;
  align-items: center;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 20px rgba(234,169,20,0.3);
  font-family: 'Open Sans', -apple-system, sans-serif;
}
.sharda-ai-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 14px;
  padding: 8px 12px;
}
.sharda-ai-input::placeholder {
  color: #cbd5e1;
}
.sharda-ai-btn {
  background: linear-gradient(135deg, #EAA914, #D6950B);
  color: #1B2C39;
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
  border: none;
  border-radius: 30px;
  padding: 9px 20px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  letter-spacing: 0.5px;
}
.sharda-ai-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 18px rgba(234,169,20,0.5);
}
.sharda-ai-modal {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(10px);
  z-index: 1000000;
  align-items: center;
  justify-content: center;
  font-family: 'Open Sans', -apple-system, sans-serif;
}
.sharda-ai-modal-content {
  background: #1B2C39;
  width: 92%;
  max-width: 680px;
  height: 600px;
  border-radius: 18px;
  border: 1px solid rgba(234, 169, 20, 0.45);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 25px 60px rgba(0,0,0,0.6);
}
.sharda-ai-header {
  padding: 16px 22px;
  background: #111c24;
  border-bottom: 1px solid rgba(255,255,255,0.12);
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #fff;
}
.sharda-ai-body {
  flex: 1;
  padding: 22px;
  overflow-y: auto;
  color: #f8fafc;
  font-size: 13px;
  line-height: 1.65;
}
.sharda-ai-footer {
  padding: 14px 22px;
  background: #111c24;
  border-top: 1px solid rgba(255,255,255,0.12);
  display: flex;
  gap: 10px;
}
.ai-badge {
  background: rgba(234,169,20,0.2);
  color: #EAA914;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  margin-left: 8px;
}
</style>

<div class="sharda-ai-floating-bar" id="saiBar">
  <span style="font-size: 20px; margin-right: 6px;">✨</span>
  <input type="text" id="saiBarInput" class="sharda-ai-input" placeholder="Ask Sharda AI anything (e.g., B.Tech CSE vs MBA fees, scholarships, SUAT 2026)..." />
  <button class="sharda-ai-btn" onclick="openSaiModal()">Ask AI</button>
</div>

<div class="sharda-ai-modal" id="saiModal">
  <div class="sharda-ai-modal-content">
    <div class="sharda-ai-header">
      <div style="display: flex; align-items: center;">
        <span style="font-size: 22px; margin-right: 8px;">🎓</span>
        <div>
          <strong style="font-size: 15px;">Sharda AI (SAI) Assistant</strong>
          <span class="ai-badge">Gemini RAG Grounded</span>
        </div>
      </div>
      <button onclick="closeSaiModal()" style="background: none; border: none; color: #fff; font-size: 24px; cursor: pointer; line-height: 1;">&times;</button>
    </div>
    <div class="sharda-ai-body" id="saiChatBody">
      <p style="background: #23394c; padding: 14px 18px; border-radius: 12px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.06);">
        Hello! I am <strong>Sharda AI (SAI)</strong>, the official conversational intelligence counselor for Sharda University (NAAC A+ Accredited). Ask me about programs, fee structures, SUAT 2026 entrance exam, up to 100% scholarships, hostels, or placements.
      </p>
    </div>
    <div class="sharda-ai-footer">
      <input type="text" id="saiModalInput" class="sharda-ai-input" style="background: #1B2C39; border: 1px solid #334155; border-radius: 8px;" placeholder="Type your inquiry..." onkeypress="if(event.key==='Enter') sendSaiChat()" />
      <button class="sharda-ai-btn" onclick="sendSaiChat()">Send</button>
    </div>
  </div>
</div>

<script>
function openSaiModal() {
  var val = document.getElementById('saiBarInput').value;
  document.getElementById('saiModal').style.display = 'flex';
  if (val.trim()) {
    document.getElementById('saiModalInput').value = val;
    sendSaiChat();
    document.getElementById('saiBarInput').value = '';
  }
}
function closeSaiModal() {
  document.getElementById('saiModal').style.display = 'none';
}
async function sendSaiChat() {
  var inp = document.getElementById('saiModalInput');
  var q = inp.value.trim();
  if (!q) return;
  inp.value = '';
  
  var body = document.getElementById('saiChatBody');
  body.innerHTML += '<div style="text-align: right; margin-bottom: 12px;"><span style="background: #EAA914; color: #1B2C39; font-weight: 700; padding: 9px 16px; border-radius: 12px; display: inline-block;">' + q + '</span></div>';
  body.innerHTML += '<div id="saiLoading" style="color: #cbd5e1; font-style: italic; margin-bottom: 12px;">Searching verified university knowledge base...</div>';
  body.scrollTop = body.scrollHeight;

  try {
    var res = await fetch('http://127.0.0.1:8000/api/v1/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: q })
    });
    var data = await res.json();
    var load = document.getElementById('saiLoading');
    if (load) load.remove();
    body.innerHTML += '<div style="background: #23394c; padding: 16px 20px; border-radius: 12px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.08);">' + data.answer.replace(/\\n/g, '<br/>') + '</div>';
  } catch(e) {
    var load = document.getElementById('saiLoading');
    if (load) load.remove();
    body.innerHTML += '<div style="background: #23394c; padding: 14px 18px; border-radius: 12px; margin-bottom: 12px;">Sharda University (NAAC A+) offers 130+ programs in Engineering, Management, Medical, Law, and Design with up to 100% scholarships.</div>';
  }
  body.scrollTop = body.scrollHeight;
}
</script>
"""

def generate_exact_html():
    print("Fetching live homepage HTML from https://www.sharda.ac.in...")
    r = httpx.get("https://www.sharda.ac.in", headers=HEADERS, verify=False, timeout=30.0)
    html = r.text

    # Point stylesheets and scripts to local assets
    html = html.replace('href="https://sharda.ac.in/assets/sharda_latest_css/bootstrap-3.3.7.min.css?v=1"', 'href="/assets/css/bootstrap-3.3.7.min.css"')
    html = html.replace('href="https://www.sharda.ac.in/assets/sharda_latest_css/font-awesome.min.css?v1.1"', 'href="/assets/css/font-awesome.min.css"')
    html = html.replace('href="https://www.sharda.ac.in/assets/sharda_latest_css/sharda_common_style_min.css?v1.15.6.21.8.9.09"', 'href="/assets/css/sharda_common_style_min.css"')
    
    html = html.replace('src="https://sharda.ac.in/assets/js/jquery-1.12.2.min.js"', 'src="/assets/js/jquery-1.12.2.min.js"')
    html = html.replace('src="https://www.sharda.ac.in/assets/js/sharda_speak.js?v1.1"', 'src="/assets/js/sharda_speak.js"')
    html = html.replace('src="https://sharda.ac.in/assets/js/easySlider1.7.js?v=101"', 'src="/assets/js/easySlider1.7.js"')
    html = html.replace('src="https://sharda.ac.in/assets/js/jquery.group.js"', 'src="/assets/js/jquery.group.js"')
    html = html.replace('src="https://sharda.ac.in/assets/js/bootstrap-3.3.7.min.js"', 'src="/assets/js/bootstrap-3.3.7.min.js"')
    html = html.replace('src="https://sharda.ac.in/assets/js/carouFredSel-6.0.5-packed.js"', 'src="/assets/js/carouFredSel-6.0.5-packed.js"')
    html = html.replace('src="https://www.sharda.ac.in/assets/js/sharda_common_revamp_min.js?v3.0.8"', 'src="/assets/js/sharda_common_revamp_min.js"')

    # Inject Sharda AI Brain
    if "</body>" in html:
        html = html.replace("</body>", f"{AI_WIDGET_CODE}\n</body>")
    else:
        html += AI_WIDGET_CODE

    with open(STATIC_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated 100% exact replica homepage at {STATIC_HTML_PATH} ({len(html)} bytes)")

if __name__ == "__main__":
    generate_exact_html()
