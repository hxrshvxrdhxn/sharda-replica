import httpx
import re
import sqlite3
import json
from pathlib import Path
from bs4 import BeautifulSoup
from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import HTMLResponse
import logging

router = APIRouter(prefix="", tags=["Exact Replica Engine"])
logger = logging.getLogger("ReplicaEngine")

SHARDA_ORIGIN = "https://www.sharda.ac.in"
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "backend" / "data"
DB_PATH = DATA_DIR / "sharda_pages.db"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

AI_WIDGET_INJECTION = r"""
<!-- ========================================================================= -->
<!-- TURBO BYTES CONSULTING - SHARDA AI KNOWLEDGE BRAIN & SEARCH ENGINE ENGINE -->
<!-- ========================================================================= -->
<style>
/* Font Parity & CORS Protection */
@font-face {
  font-family: 'FontAwesome';
  src: url('/assets/fonts/fontawesome-webfont.woff2?v=4.7.0') format('woff2'),
       url('/assets/fonts/fontawesome-webfont.woff?v=4.7.0') format('woff'),
       url('/assets/fonts/fontawesome-webfont.ttf?v=4.7.0') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'simple-line-icons';
  src: url('/assets/fonts/Simple-Line-Icons.woff2?v=2.4.0') format('woff2'),
       url('/assets/fonts/Simple-Line-Icons.woff?v=2.4.0') format('woff'),
       url('/assets/fonts/Simple-Line-Icons.ttf?v=2.4.0') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

/* Layout & Header 1:1 Pixel Parity Styles */
#strip {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 35px !important;
  z-index: 2002 !important;
}

header#header.fixed.dark,
header#header {
  position: fixed !important;
  top: 35px !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 2001 !important;
  height: 60px !important;
}

body:not(.home) {
  padding-top: 95px !important;
}

/* Breadcrumbs 1:1 Parity */
#breadcrumbs {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 100 !important;
  padding-top: 25px !important;
  margin-bottom: 25px !important;
  position: relative !important;
}
#breadcrumbs .container {
  display: flex !important;
  align-items: center !important;
  flex-wrap: wrap !important;
  gap: 6px !important;
}
#breadcrumbs a, 
#breadcrumbs span, 
#breadcrumbs .divider {
  display: inline-flex !important;
  align-items: center !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  line-height: 14px !important;
  font-family: Montserrat, Arial, Helvetica, sans-serif !important;
  text-decoration: none !important;
  transition: color 0.2s ease !important;
}
#breadcrumbs a:hover {
  color: #EAA914 !important;
}
#breadcrumbs .icons,
#breadcrumbs i[class*="icon-"] {
  font-family: 'simple-line-icons' !important;
  font-style: normal !important;
  font-size: 11px !important;
  display: inline-block !important;
  line-height: 1 !important;
}
/* White breadcrumbs inside banners */
#secondary-banner #breadcrumbs a,
#secondary-banner #breadcrumbs span,
#secondary-banner #breadcrumbs i,
#secondary-banner #breadcrumbs .divider,
.admission-banner #breadcrumbs a,
.admission-banner #breadcrumbs span,
.admission-banner #breadcrumbs i,
.admission-banner #breadcrumbs .divider,
.triangle-banner #breadcrumbs a,
.triangle-banner #breadcrumbs span,
.triangle-banner #breadcrumbs i,
.triangle-banner #breadcrumbs .divider,
.about-banner #breadcrumbs a,
.about-banner #breadcrumbs span,
.about-banner #breadcrumbs i,
.about-banner #breadcrumbs .divider,
.campus-banner #breadcrumbs a,
.campus-banner #breadcrumbs span,
.campus-banner #breadcrumbs i,
.campus-banner #breadcrumbs .divider,
.school-bannertop #breadcrumbs a,
.school-bannertop #breadcrumbs span,
.school-bannertop #breadcrumbs i,
.school-bannertop #breadcrumbs .divider {
  color: #ffffff !important;
}
/* Dark breadcrumbs on standard white background pages */
body:not(.home) #breadcrumbs a,
body:not(.home) #breadcrumbs span,
body:not(.home) #breadcrumbs i,
body:not(.home) #breadcrumbs .divider {
  color: #424242;
}

.logo img {
  max-height: 45px !important;
  width: auto !important;
  object-fit: contain !important;
}

.logo img.fixed-header-logo {
  display: none !important;
}

.powered-by, .powered_by, [class*="whitebird"], [id*="whitebird"] {
  display: none !important;
}

#read-faq {
  display: block !important;
  padding: 70px 0 !important;
  background: #1B2C39 url(/assets/imgs/faq-bg.png) no-repeat center center !important;
  background-size: cover !important;
}
#read-faq h4 {
  color: #ffffff !important;
  margin: 0px !important;
  text-align: center !important;
  font-weight: 500 !important;
}
#read-faq .button2 {
  background: #EAA914 !important;
  color: #1B2C39 !important;
  font-weight: 700 !important;
  border: none !important;
  min-width: 180px !important;
  margin-left: 15px !important;
  border-radius: 25px !important;
  padding: 10px 24px !important;
  display: inline-block !important;
}

.global-map {
  position: relative !important;
  display: block !important;
}
.global-map img {
  display: block !important;
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  opacity: 1 !important;
  visibility: visible !important;
}

/* ========================================================= */
/* TURBO BYTES AI SEARCH HERO & FLOATING ENGINE STYLES       */
/* ========================================================= */
.turbo-ai-search-container {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: 15px 15px 25px 15px;
  font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  box-sizing: border-box;
}

.turbo-ai-pills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 12px;
}

.turbo-ai-pill {
  background: rgba(30, 48, 65, 0.72);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e2e8f0;
  padding: 7px 16px;
  border-radius: 30px;
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  white-space: nowrap;
  outline: none;
}
.turbo-ai-pill:hover {
  background: rgba(234, 169, 20, 0.35);
  border-color: #EAA914;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(234, 169, 20, 0.25);
}

.turbo-ai-search-bar {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(20, 32, 45, 0.9);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1.5px solid rgba(234, 169, 20, 0.55);
  border-radius: 50px;
  padding: 6px 8px 6px 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.45), 0 0 18px rgba(234,169,20,0.25);
  transition: border-color 0.25s, box-shadow 0.25s;
}
.turbo-ai-search-bar:focus-within {
  border-color: #EAA914;
  box-shadow: 0 12px 35px rgba(0,0,0,0.55), 0 0 25px rgba(234,169,20,0.45);
}

.turbo-sparkle-icon {
  font-size: 18px;
  margin-right: 10px;
  display: flex;
  align-items: center;
}

.turbo-ai-main-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 14.5px;
  padding: 8px 6px;
  font-family: inherit;
}
.turbo-ai-main-input::placeholder {
  color: #94a3b8;
}

.turbo-send-plane-btn {
  background: none;
  border: none;
  color: #94a3b8;
  padding: 6px 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
  outline: none;
}
.turbo-send-plane-btn:hover {
  color: #EAA914;
}

.turbo-ai-action-btn {
  background: linear-gradient(135deg, #e58e26 0%, #EAA914 50%, #d6950b 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 13px;
  border: none;
  border-radius: 30px;
  padding: 10px 22px;
  cursor: pointer;
  transition: all 0.25s ease;
  letter-spacing: 0.3px;
  box-shadow: 0 4px 15px rgba(229, 142, 38, 0.4);
  white-space: nowrap;
}
.turbo-ai-action-btn:hover {
  transform: scale(1.04);
  box-shadow: 0 6px 20px rgba(234, 169, 20, 0.6);
  color: #111c24;
}

.turbo-ai-brand-footer {
  text-align: center;
  margin-top: 10px;
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  letter-spacing: 0.3px;
}
.turbo-brand-name {
  color: #cbd5e1;
  font-weight: 600;
}
.turbo-brand-name span {
  color: #EAA914;
  font-weight: 700;
}

/* Auto-suggest dropdown */
.turbo-suggest-box {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: #1B2C39;
  border: 1px solid rgba(234, 169, 20, 0.4);
  border-radius: 16px;
  padding: 8px 0;
  z-index: 2005;
  box-shadow: 0 15px 40px rgba(0,0,0,0.6);
  max-height: 380px;
  overflow-y: auto;
}
.turbo-suggest-item {
  padding: 10px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  text-decoration: none !important;
}
.turbo-suggest-item:hover {
  background: #23394c;
}
.turbo-suggest-title {
  color: #ffffff;
  font-size: 13.5px;
  font-weight: 600;
  display: block;
}
.turbo-suggest-sub {
  color: #94a3b8;
  font-size: 11.5px;
  margin-top: 2px;
  display: block;
}
.turbo-suggest-fee {
  background: rgba(234, 169, 20, 0.2);
  color: #EAA914;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

/* Floating AI Bar on all pages */
.turbo-ai-floating-bar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999999;
  width: 92%;
  max-width: 760px;
  background: rgba(20, 32, 45, 0.94);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(234, 169, 20, 0.6);
  border-radius: 50px;
  padding: 6px 10px 6px 16px;
  display: flex;
  align-items: center;
  box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 0 20px rgba(234,169,20,0.3);
  font-family: 'Open Sans', -apple-system, sans-serif;
}

body.home .turbo-ai-floating-bar {
  display: none !important;
}


/* Rich Modal */
.turbo-ai-modal {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.78);
  backdrop-filter: blur(12px);
  z-index: 1000000;
  align-items: center;
  justify-content: center;
  font-family: 'Open Sans', -apple-system, sans-serif;
}
.turbo-ai-modal-content {
  background: #162430;
  width: 92%;
  max-width: 720px;
  height: 620px;
  border-radius: 20px;
  border: 1px solid rgba(234, 169, 20, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 30px 70px rgba(0,0,0,0.75);
}
.turbo-ai-modal-header {
  padding: 16px 22px;
  background: #0f1922;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #fff;
}
.turbo-ai-modal-body {
  flex: 1;
  padding: 22px;
  overflow-y: auto;
  color: #f8fafc;
  font-size: 13.5px;
  line-height: 1.65;
}
.turbo-ai-modal-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0;
  font-size: 12.5px;
}
.turbo-ai-modal-body th, .turbo-ai-modal-body td {
  border: 1px solid rgba(255,255,255,0.15);
  padding: 8px 12px;
  text-align: left;
}
.turbo-ai-modal-body th {
  background: rgba(234, 169, 20, 0.2);
  color: #EAA914;
}
.turbo-ai-modal-footer {
  padding: 14px 22px;
  background: #0f1922;
  border-top: 1px solid rgba(255,255,255,0.1);
  display: flex;
  gap: 10px;
}
.turbo-powered-chip {
  background: rgba(234, 169, 20, 0.15);
  color: #EAA914;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  margin-left: 8px;
}
</style>

<!-- Floating Global AI Search Bar -->
<div class="turbo-ai-floating-bar" id="turboFloatBar">
  <span class="turbo-sparkle-icon">✨</span>
  <input type="text" id="turboFloatInput" class="turbo-ai-main-input" placeholder="Ask Sharda AI (e.g. B.Tech CSE vs MBA fees, scholarships, SUAT 2026)..." oninput="handleTurboSuggest(this.value, 'float')" onkeydown="if(event.key==='Enter'){event.preventDefault(); triggerTurboSearch(this.value);}" autocomplete="off" />
  <button class="turbo-send-plane-btn" onclick="triggerTurboSearch(document.getElementById('turboFloatInput').value)">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="#EAA914"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
  </button>
  <button class="turbo-ai-action-btn" onclick="triggerTurboSearch(document.getElementById('turboFloatInput').value)">Ask Sharda AI</button>
  <div class="turbo-suggest-box" id="turboFloatSuggest" style="display:none; bottom:calc(100% + 10px); top:auto;"></div>
</div>

<!-- Conversational AI Modal -->
<div class="turbo-ai-modal" id="turboModal">
  <div class="turbo-ai-modal-content">
    <div class="turbo-ai-modal-header">
      <div style="display: flex; align-items: center;">
        <span style="font-size: 22px; margin-right: 8px;">🎓</span>
        <div>
          <strong style="font-size: 15px;">Sharda AI Knowledge Brain</strong>
          <span class="turbo-powered-chip">⚡ Powered by Turbo Bytes Consulting (TBC)</span>
        </div>
      </div>
      <button onclick="closeTurboModal()" style="background: none; border: none; color: #cbd5e1; font-size: 26px; cursor: pointer; line-height: 1;">&times;</button>
    </div>
    <div class="turbo-ai-modal-body" id="turboChatBody">
      <div style="background: #1f3345; padding: 14px 18px; border-radius: 12px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.08);">
        Hello! I am <strong>Sharda AI</strong>, powered by <strong>Turbo Bytes Consulting (TBC)</strong> and Google Gemini. I have indexed all 2,388 pages across Sharda University (NAAC A+ Accredited). Ask me about programs, fee structures, SUAT 2026 entrance exam, up to 100% scholarships, hostels, or placement track records.
      </div>
    </div>
    <div class="turbo-ai-modal-footer">
      <input type="text" id="turboModalInput" class="turbo-ai-main-input" style="background: #162430; border: 1px solid #334155; border-radius: 10px; padding: 10px 14px;" placeholder="Ask follow-up question or explore more courses..." onkeydown="if(event.key==='Enter'){event.preventDefault(); sendTurboModalChat();}" />
      <button class="turbo-ai-action-btn" onclick="sendTurboModalChat()">Send</button>
    </div>
  </div>
</div>

<!-- Interactive Brochure & Course Guide Modal -->
<div class="turbo-ai-modal" id="turboBrochureModal">
  <div class="turbo-ai-modal-content" style="height: auto; max-width: 520px; padding: 25px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
      <div>
        <h3 style="margin: 0; color: #fff; font-size: 18px;">Download Official Brochure</h3>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 12px;">Get instant syllabus, fee matrix & scholarship breakdown</p>
      </div>
      <button onclick="document.getElementById('turboBrochureModal').style.display='none'" style="background: none; border: none; color: #cbd5e1; font-size: 24px; cursor: pointer;">&times;</button>
    </div>
    <form id="turboBrochureForm" onsubmit="handleBrochureSubmit(event)">
      <div style="margin-bottom: 12px;">
        <label style="color: #cbd5e1; font-size: 12px; display: block; margin-bottom: 4px;">Candidate Name</label>
        <input type="text" id="bmName" required style="width: 100%; padding: 10px 14px; background: #0f1922; border: 1px solid #334155; border-radius: 8px; color: #fff; box-sizing: border-box;" placeholder="Enter full name" />
      </div>
      <div style="margin-bottom: 12px;">
        <label style="color: #cbd5e1; font-size: 12px; display: block; margin-bottom: 4px;">Mobile Number</label>
        <input type="tel" id="bmPhone" required style="width: 100%; padding: 10px 14px; background: #0f1922; border: 1px solid #334155; border-radius: 8px; color: #fff; box-sizing: border-box;" placeholder="+91 98765 43210" />
      </div>
      <div style="margin-bottom: 12px;">
        <label style="color: #cbd5e1; font-size: 12px; display: block; margin-bottom: 4px;">Email Address</label>
        <input type="email" id="bmEmail" required style="width: 100%; padding: 10px 14px; background: #0f1922; border: 1px solid #334155; border-radius: 8px; color: #fff; box-sizing: border-box;" placeholder="name@example.com" />
      </div>
      <div style="margin-bottom: 18px;">
        <label style="color: #cbd5e1; font-size: 12px; display: block; margin-bottom: 4px;">Interested Programme</label>
        <select id="bmCourse" style="width: 100%; padding: 10px 14px; background: #0f1922; border: 1px solid #334155; border-radius: 8px; color: #fff; box-sizing: border-box;">
          <option value="B.Tech Computer Science & Engg">B.Tech Computer Science & Engineering (AI/ML)</option>
          <option value="MBA Dual Specialization">MBA (Dual Specialization - Marketing/Finance/HR)</option>
          <option value="MBBS Medical Sciences">MBBS (Medical Sciences & Research)</option>
          <option value="BBA Hons">BBA (Hons / International Business)</option>
          <option value="B.Sc Biotechnology">B.Sc. Biotechnology / Microbiology</option>
          <option value="BA LLB Integrated">BA LL.B. (Integrated 5-Year Law)</option>
          <option value="B.Des Interior Design">B.Des (Interior & Product Design)</option>
        </select>
      </div>
      <button type="submit" class="turbo-ai-action-btn" style="width: 100%; padding: 12px; font-size: 14px;">Instant Download & Unlock Syllabus</button>
    </form>
    <div id="bmSuccess" style="display: none; background: #1f3345; border: 1px solid #EAA914; padding: 16px; border-radius: 10px; margin-top: 14px; text-align: center; color: #fff;">
      <h4 style="color: #EAA914; margin: 0 0 6px 0;">🎉 Brochure Unlocked!</h4>
      <p style="font-size: 12px; margin: 0; color: #cbd5e1;">Your curriculum guide has been generated. An admissions counselor will also contact you with scholarship eligibility.</p>
    </div>
  </div>
</div>

<!-- Interactive Scholarship & Net Fee Calculator -->
<div class="turbo-ai-modal" id="turboScholarshipModal">
  <div class="turbo-ai-modal-content" style="height: auto; max-width: 580px; padding: 25px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <div>
        <h3 style="margin: 0; color: #fff; font-size: 18px;">🏆 Sharda Scholarship & Net Fee Calculator</h3>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 12px;">Calculate your tuition fee waiver based on academic performance</p>
      </div>
      <button onclick="document.getElementById('turboScholarshipModal').style.display='none'" style="background: none; border: none; color: #cbd5e1; font-size: 24px; cursor: pointer;">&times;</button>
    </div>
    <div style="margin-bottom: 14px;">
      <label style="color: #cbd5e1; font-size: 12px; display: block; margin-bottom: 4px;">Select Degree Programme</label>
      <select id="calcProgram" onchange="runScholarshipCalc()" style="width: 100%; padding: 10px 14px; background: #0f1922; border: 1px solid #334155; border-radius: 8px; color: #fff; box-sizing: border-box;">
        <option value="220000">B.Tech Computer Science & Engineering (Rs. 2,20,000/yr)</option>
        <option value="235000">B.Tech CSE - AI & ML (Rs. 2,35,000/yr)</option>
        <option value="385000">MBA Dual Specialization (Rs. 3,85,000/yr)</option>
        <option value="185000">BBA Hons / Research (Rs. 1,85,000/yr)</option>
        <option value="145000">B.Sc. Biotechnology (Rs. 1,45,000/yr)</option>
        <option value="195000">BA LL.B. Integrated 5-Year (Rs. 1,95,000/yr)</option>
        <option value="210000">B.Des Interior Design (Rs. 2,10,000/yr)</option>
      </select>
    </div>
    <div style="margin-bottom: 16px;">
      <label style="color: #cbd5e1; font-size: 12px; display: block; margin-bottom: 4px;">10+2 / Graduation Percentage (%): <strong id="calcPercentVal" style="color: #EAA914;">92%</strong></label>
      <input type="range" id="calcPercent" min="60" max="100" value="92" oninput="document.getElementById('calcPercentVal').innerText=this.value+'%'; runScholarshipCalc();" style="width: 100%; accent-color: #EAA914;" />
    </div>
    <div id="calcResultsBox" style="background: #0f1922; border: 1px solid rgba(234,169,20,0.3); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
        <span style="color: #94a3b8;">Eligible Scholarship Slab:</span>
        <strong id="calcSlab" style="color: #EAA914;">50% Tuition Fee Waiver</strong>
      </div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
        <span style="color: #94a3b8;">Annual Tuition Savings:</span>
        <strong id="calcSavings" style="color: #22c55e;">- Rs. 1,10,000 / yr</strong>
      </div>
      <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;" />
      <div style="display: flex; justify-content: space-between; font-size: 15px;">
        <span style="color: #fff; font-weight: 600;">Net Payable Annual Tuition:</span>
        <strong id="calcNetFee" style="color: #EAA914; font-size: 17px;">Rs. 1,10,000 / yr</strong>
      </div>
    </div>
    <button onclick="document.getElementById('turboScholarshipModal').style.display='none'; openBrochureModal();" class="turbo-ai-action-btn" style="width: 100%; padding: 12px; font-size: 14px;">Lock In Scholarship & Apply Now</button>
  </div>
</div>

<script>
var suggestDebounceTimer = null;

function renderTurboMarkdown(md) {
  if (!md) return '';
  var html = md;
  html = html.replace(/```([\s\S]*?)```/g, '<pre style="background:#0f1922; padding:10px; border-radius:8px; overflow-x:auto;"><code>$1</code></pre>');
  html = html.replace(/^### (.*$)/gim, '<h4 style="color:#EAA914; margin:10px 0 4px 0; font-size:14.5px; font-weight:700;">$1</h4>');
  html = html.replace(/^## (.*$)/gim, '<h3 style="color:#EAA914; margin:12px 0 6px 0; font-size:16px; font-weight:700;">$1</h3>');
  html = html.replace(/^# (.*$)/gim, '<h2 style="color:#EAA914; margin:14px 0 8px 0; font-size:17.5px; font-weight:700;">$1</h2>');
  html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  var lines = html.split('\n');
  var inTable = false;
  var tableHtml = '';
  var resLines = [];
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i].trim();
    if (line.startsWith('|') && line.endsWith('|')) {
      if (line.match(/^\|[\s\-:]+\|$/)) {
        continue;
      }
      if (!inTable) {
        inTable = true;
        tableHtml = '<div style="overflow-x:auto; margin:12px 0;"><table style="width:100%; border-collapse:collapse; font-size:12.5px;">';
        var cells = line.split('|').slice(1, -1);
        tableHtml += '<thead><tr style="background:rgba(234,169,20,0.25); color:#EAA914;">' + cells.map(function(c) { return '<th style="border:1px solid rgba(255,255,255,0.15); padding:8px 10px; text-align:left;">' + c.trim() + '</th>'; }).join('') + '</tr></thead><tbody>';
      } else {
        var cells = line.split('|').slice(1, -1);
        tableHtml += '<tr>' + cells.map(function(c) { return '<td style="border:1px solid rgba(255,255,255,0.12); padding:6px 10px; color:#e2e8f0;">' + c.trim() + '</td>'; }).join('') + '</tr>';
      }
    } else {
      if (inTable) {
        tableHtml += '</tbody></table></div>';
        resLines.push(tableHtml);
        inTable = false;
        tableHtml = '';
      }
      if (line.startsWith('- ') || line.startsWith('* ')) {
        resLines.push('<li style="margin-left:18px; margin-bottom:4px; color:#cbd5e1;">' + line.substring(2) + '</li>');
      } else if (line.length > 0) {
        resLines.push('<p style="margin:6px 0; line-height:1.55;">' + line + '</p>');
      }
    }
  }
  if (inTable) {
    tableHtml += '</tbody></table></div>';
    resLines.push(tableHtml);
  }
  return resLines.join('');
}

function handleTurboSuggest(val, source) {
  clearTimeout(suggestDebounceTimer);
  var targetBox = source === 'float' ? document.getElementById('turboFloatSuggest') : document.getElementById('turboHeroSuggest');
  if (!targetBox) return;

  if (!val || val.trim().length < 2) {
    targetBox.style.display = 'none';
    return;
  }

  suggestDebounceTimer = setTimeout(async function() {
    try {
      var res = await fetch('/api/v1/ai/suggest?q=' + encodeURIComponent(val.trim()));
      var data = await res.json();
      if (data.suggestions && data.suggestions.length > 0) {
        var html = '';
        data.suggestions.forEach(function(s) {
          html += '<a href="' + s.url + '" class="turbo-suggest-item">' +
            '<div><span class="turbo-suggest-title">' + s.title + '</span>' +
            '<span class="turbo-suggest-sub">' + s.school + ' &bull; ' + s.duration + '</span></div>' +
            '<span class="turbo-suggest-fee">' + s.annual_fee + '</span>' +
          '</a>';
        });
        targetBox.innerHTML = html;
        targetBox.style.display = 'block';
      } else {
        targetBox.style.display = 'none';
      }
    } catch(e) {
      targetBox.style.display = 'none';
    }
  }, 220);
}

document.addEventListener('click', function(e) {
  var floatS = document.getElementById('turboFloatSuggest');
  var heroS = document.getElementById('turboHeroSuggest');
  if (floatS && !e.target.closest('#turboFloatBar')) floatS.style.display = 'none';
  if (heroS && !e.target.closest('#turboHeroSearch')) heroS.style.display = 'none';

  // Intercept any search link clicks to open Sharda AI modal instead of external navigation
  var searchLink = e.target.closest('a[href="/search"], a[href*="sharda.ac.in/search"], a.search, a.search-box');
  if (searchLink) {
    e.preventDefault();
    e.stopPropagation();
    openTurboModal("What are the top programmes at Sharda University?");
    return false;
  }

  // Intercept brochure clicks
  var brochureBtn = e.target.closest('a[href*="brochure"], a[href*="download"]');
  if (brochureBtn && !e.target.closest('.turbo-ai-modal')) {
    e.preventDefault();
    openBrochureModal();
  }
}, true);

// Global form submission interceptor for search forms
document.addEventListener('submit', function(e) {
  var form = e.target;
  if (form && (form.id === 'turboBrochureForm')) return;
  var act = form.getAttribute('action') || '';
  if (act.includes('search') || form.querySelector('input[name*="search"], input[id*="search"]')) {
    e.preventDefault();
    e.stopPropagation();
    var inp = form.querySelector('input[type="text"]');
    var val = inp ? inp.value.trim() : '';
    openTurboModal(val || "What are the top programmes at Sharda University?");
    return false;
  }
}, true);

function openBrochureModal() {
  var modal = document.getElementById('turboBrochureModal');
  if (modal) modal.style.display = 'flex';
}

function openScholarshipModal() {
  var modal = document.getElementById('turboScholarshipModal');
  if (modal) {
    modal.style.display = 'flex';
    runScholarshipCalc();
  }
}

function runScholarshipCalc() {
  var baseFee = parseFloat(document.getElementById('calcProgram').value) || 220000;
  var pct = parseFloat(document.getElementById('calcPercent').value) || 90;
  var waiverPct = 0;
  var slabName = "Standard Merit Slab";

  if (pct >= 95) { waiverPct = 100; slabName = "100% Tuition Fee Waiver (Top Merit)"; }
  else if (pct >= 90) { waiverPct = 50; slabName = "50% Tuition Fee Waiver"; }
  else if (pct >= 85) { waiverPct = 40; slabName = "40% Tuition Fee Waiver"; }
  else if (pct >= 80) { waiverPct = 20; slabName = "20% Tuition Fee Waiver"; }
  else if (pct >= 75) { waiverPct = 10; slabName = "10% Tuition Fee Waiver"; }
  else { waiverPct = 0; slabName = "Standard Fee (No Waiver)"; }

  var savings = (baseFee * waiverPct) / 100;
  var netFee = baseFee - savings;

  document.getElementById('calcSlab').innerText = slabName;
  document.getElementById('calcSavings').innerText = "- Rs. " + savings.toLocaleString('en-IN') + " / yr";
  document.getElementById('calcNetFee').innerText = "Rs. " + netFee.toLocaleString('en-IN') + " / yr";
}

async function handleBrochureSubmit(e) {
  e.preventDefault();
  var name = document.getElementById('bmName').value;
  var phone = document.getElementById('bmPhone').value;
  var email = document.getElementById('bmEmail').value;
  var course = document.getElementById('bmCourse').value;

  try {
    await fetch('/api/v1/leads/capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        full_name: name,
        phone: phone,
        email: email,
        interested_course: course,
        source: 'Brochure Download Modal'
      })
    });
  } catch(err) {}

  document.getElementById('turboBrochureForm').style.display = 'none';
  document.getElementById('bmSuccess').style.display = 'block';
}

function openTurboModal(initialQuery) {
  var modal = document.getElementById('turboModal');
  if (modal) modal.style.display = 'flex';
  if (initialQuery && initialQuery.trim()) {
    document.getElementById('turboModalInput').value = initialQuery;
    sendTurboModalChat();
  }
}

function closeTurboModal() {
  var modal = document.getElementById('turboModal');
  if (modal) modal.style.display = 'none';
}

function triggerTurboSearch(query) {
  if (!query || !query.trim()) {
    var inp = document.getElementById('turboSearchInput') || document.getElementById('turboFloatInput');
    query = inp ? inp.value.trim() : '';
  }
  if (query === 'Scholarships & SUAT 2026') {
    openScholarshipModal();
    return;
  }
  if (!query) query = "What are the top programmes at Sharda University?";
  openTurboModal(query);
}

async function sendTurboModalChat() {
  var inp = document.getElementById('turboModalInput');
  var q = inp.value.trim();
  if (!q) return;
  inp.value = '';

  var body = document.getElementById('turboChatBody');
  body.innerHTML += '<div style="text-align: right; margin-bottom: 14px;"><span style="background: linear-gradient(135deg, #e58e26, #EAA914); color: #162430; font-weight: 700; padding: 10px 18px; border-radius: 14px; display: inline-block;">' + q + '</span></div>';
  body.innerHTML += '<div id="turboLoading" style="color: #94a3b8; font-style: italic; margin-bottom: 14px;"><span style="color:#EAA914;">⚡ Turbo Bytes Brain:</span> Searching verified Sharda knowledge base...</div>';
  body.scrollTop = body.scrollHeight;

  try {
    var res = await fetch('/api/v1/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: q })
    });
    var data = await res.json();
    var load = document.getElementById('turboLoading');
    if (load) load.remove();

    var answerHtml = renderTurboMarkdown(data.answer);
    body.innerHTML += '<div style="background: #1f3345; padding: 18px 22px; border-radius: 14px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.08);">' + answerHtml + '</div>';

    if (data.matched_programs && data.matched_programs.length > 0) {
      var progHtml = '<div style="margin-bottom: 16px;"><strong style="color:#EAA914; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Recommended Programme Portals:</strong><div style="display:flex; flex-direction:column; gap:8px; margin-top:8px;">';
      data.matched_programs.forEach(function(p) {
        progHtml += '<a href="' + p.url + '" style="background:#162430; border:1px solid rgba(234,169,20,0.3); padding:10px 14px; border-radius:10px; color:#fff; text-decoration:none; display:flex; justify-content:space-between; align-items:center;">' +
          '<div><span style="font-weight:600; font-size:13px; color:#fff;">' + p.title + '</span><div style="font-size:11px; color:#94a3b8;">' + p.school + ' &bull; ' + p.duration + '</div></div>' +
          '<span style="background:rgba(234,169,20,0.2); color:#EAA914; font-size:11px; font-weight:700; padding:4px 8px; border-radius:8px;">' + p.annual_fee + '</span>' +
        '</a>';
      });
      progHtml += '</div></div>';
      body.innerHTML += progHtml;
    }
  } catch(e) {
    var load = document.getElementById('turboLoading');
    if (load) load.remove();
    body.innerHTML += '<div style="background: #1f3345; padding: 16px; border-radius: 12px; margin-bottom: 14px;">Sharda University (NAAC A+) offers 130+ programs across 14 Schools with up to 100% scholarships. Ask about fees, admissions, or SUAT 2026.</div>';
  }
  body.scrollTop = body.scrollHeight;
}
</script>
"""

def get_page_from_db(slug: str):
    normalized = slug.strip("/").lower()
    if not normalized or normalized in ("home", "replica"):
        home_html_path = BASE_DIR / "frontend" / "public" / "index_replica.html"
        if home_html_path.exists():
            return home_html_path.read_text(encoding="utf-8")

    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content_html FROM pages WHERE slug = ? OR slug = ? LIMIT 1", (normalized, f"/{normalized}"))
    row = cursor.fetchone()
    if not row:
        cursor.execute("SELECT content_html FROM pages WHERE slug LIKE ? LIMIT 1", (f"%{normalized}%",))
        row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return row[0]
    return None

def process_html(html: str, current_slug: str = "") -> str:
    soup = BeautifulSoup(html, "html.parser")
    subpath = current_slug.split("/")[0].lower() if current_slug else ""
    is_microsite = subpath in ["iqac", "dsw", "library", "research", "alumni", "ccdc", "iic"]
    
    # 1. Stylesheets
    for link in soup.find_all("link", href=True):
        href = link["href"]
        if "font-awesome" in href:
            link["href"] = "/assets/css/font-awesome.min.css"
        elif "bootstrap" in href:
            link["href"] = "/assets/css/bootstrap-3.3.7.min.css"
        elif "sharda_common_style" in href:
            link["href"] = "/assets/css/sharda_common_style_min.css"
        elif is_microsite and "suat_common_style" in href:
            link["href"] = f"https://www.sharda.ac.in/{subpath}/assets/css/suat_common_style.css?v=1.1.16120222"
        elif href.startswith("/assets/"):
            link["href"] = href
        elif href.startswith("assets/") or href.startswith("css/"):
            if is_microsite:
                link["href"] = f"https://www.sharda.ac.in/{subpath}/{href}"
            else:
                rel_path = href[href.index("assets/"):] if "assets/" in href else href
                if (BASE_DIR / "frontend" / "public" / rel_path).exists():
                    link["href"] = f"/{rel_path}"
                else:
                    link["href"] = f"https://www.sharda.ac.in/{href}"
        elif "assets/" in href:
            rel_path = href[href.index("assets/"):]
            if (BASE_DIR / "frontend" / "public" / rel_path).exists():
                link["href"] = f"/{rel_path}"
            else:
                link["href"] = f"https://www.sharda.ac.in/{rel_path}"
        elif "attachments/" in href:
            link["href"] = f"https://www.sharda.ac.in/{href[href.index('attachments/'):]}"
        elif href.startswith("/") and not href.startswith("//"):
            link["href"] = f"https://www.sharda.ac.in{href}"

    # 2. Scripts & Legacy Chatbot Cleanup
    for script in list(soup.find_all("script")):
        src = script.get("src", "")
        text = script.string or ""
        if any(bad in src.lower() for bad in ["superbot", "whitebird", "sai/embed.js", "responsivevoice"]) or \
           any(bad in text.lower() for bad in ["__sbt_widget_client", "superbot", "whitebird"]):
            script.decompose()
            continue

        if script.get("src"):
            src = script["src"]
            if is_microsite and (src.startswith("assets/") or src.startswith("js/")):
                script["src"] = f"https://www.sharda.ac.in/{subpath}/{src}"
            elif "assets/" in src:
                rel_path = src[src.index("assets/"):]
                if (BASE_DIR / "frontend" / "public" / rel_path).exists():
                    script["src"] = f"/{rel_path}"
                else:
                    script["src"] = f"https://www.sharda.ac.in/{rel_path}"
            elif "attachments/" in src:
                script["src"] = f"https://www.sharda.ac.in/{src[src.index('attachments/'):]}"
            elif src.startswith("/") and not src.startswith("//"):
                script["src"] = f"https://www.sharda.ac.in{src}"

    # 3. Images & Lazy Images Normalization
    for img in soup.find_all("img"):
        for attr in ["data-src", "data-original", "data-lazy", "data-image"]:
            val = img.get(attr)
            if val and (not img.get("src") or img.get("src") in ["#", "", "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"]):
                img["src"] = val
                break

        src = img.get("src")
        if src:
            if "world-map" in src:
                if "mobile" in src:
                    img["src"] = "/assets/imgs/world-map-mobile.jpg"
                else:
                    img["src"] = "/assets/imgs/world-map.jpg"
            elif "faq-bg" in src:
                img["src"] = "/assets/imgs/faq-bg.png"
            elif is_microsite and (src.startswith("assets/") or src.startswith("images/")):
                img["src"] = f"https://www.sharda.ac.in/{subpath}/{src}"
            elif "assets/" in src:
                rel_path = src[src.index("assets/"):]
                if (BASE_DIR / "frontend" / "public" / rel_path).exists():
                    img["src"] = f"/{rel_path}"
                else:
                    img["src"] = f"https://www.sharda.ac.in/{rel_path}"
            elif "attachments/" in src:
                img["src"] = f"https://www.sharda.ac.in/{src[src.index('attachments/'):]}"
            elif "uploads/" in src:
                img["src"] = f"https://www.sharda.ac.in/{src[src.index('uploads/'):]}"
            elif src.startswith("/") and not src.startswith("//"):
                if not (BASE_DIR / "frontend" / "public" / src.lstrip("/")).exists():
                    img["src"] = f"https://www.sharda.ac.in{src}"

        # Clean lazy class
        classes = img.get("class", [])
        if isinstance(classes, list) and "lazy" in classes:
            classes.remove("lazy")
            img["class"] = classes

    # 4. Anchor Links - keep in-app navigation on localhost:3000
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("https://www.sharda.ac.in/") or href.startswith("https://sharda.ac.in/"):
            path = href.split("sharda.ac.in/")[1]
            if not any(path.lower().endswith(ext) for ext in [".pdf", ".jpg", ".png", ".jpeg", ".zip", ".docx"]):
                a["href"] = f"/{path}"
        elif href.startswith("/replica/"):
            clean_path = href.replace("/replica/", "/").replace("//", "/")
            a["href"] = clean_path

    # 5. Fix logo display style
    for logo in soup.find_all("img", class_="fixed-header-logo"):
        logo["style"] = "display:none;"

    # 6. Breadcrumbs Integrity & Injection for Inner Pages
    if current_slug and current_slug not in ["", "index", "home"]:
        bc = soup.find(id="breadcrumbs") or soup.find(class_=re.compile(r"breadcrumb", re.I))
        if not bc:
            parts = [p for p in current_slug.strip("/").split("/") if p]
            if parts:
                crumbs = ['<a href="/"><i class="icon-home icons"></i></a>']
                accum_path = ""
                acronyms = {"Iqac": "IQAC", "Dsw": "DSW", "Ccdc": "CCDC", "Iic": "IIC", "Nirf": "NIRF", "Naac": "NAAC", "Btech": "B.Tech", "Mba": "MBA", "Bba": "BBA", "Bca": "BCA", "Mca": "MCA", "Phd": "Ph.D", "Suat": "SUAT", "Cse": "CSE"}
                for i, part in enumerate(parts):
                    accum_path += f"/{part}"
                    name = part.replace("-", " ").replace("_", " ").title()
                    for k, v in acronyms.items():
                        name = re.sub(rf"\b{k}\b", v, name, flags=re.IGNORECASE)
                    is_last = (i == len(parts) - 1)
                    crumbs.append('<span class="divider"><i class="icon-arrow-right icons"></i></span>')
                    if is_last:
                        page_title = soup.title.string if soup.title else name
                        if " - " in page_title:
                            page_title = page_title.split(" - ")[0].strip()
                        if len(page_title) > 40:
                            page_title = name
                        crumbs.append(f'<a>{page_title}</a>')
                    else:
                        crumbs.append(f'<a href="{accum_path}">{name}</a>')
                
                bc_html = f'<div id="breadcrumbs"><div class="container">\n{"".join(crumbs)}\n</div></div>'
                bc_soup = BeautifulSoup(bc_html, "html.parser").find("div", id="breadcrumbs")
                
                banner_container = soup.find(class_=re.compile(r"(triangle-banner|admission-banner|about-banner|school-bannertop|campus-banner)", re.I))
                if banner_container:
                    target_container = banner_container.find("div", class_="container") or banner_container
                    target_container.insert(0, bc_soup)
                else:
                    main_content = soup.find(id="main-wrapper") or soup.find("main") or soup.find("body")
                    if main_content:
                        main_content.insert(0, bc_soup)

    output_html = str(soup)

    # Clean legacy Whitebird branding and replace with Turbo Bytes Consulting (TBC)
    output_html = re.sub(r'Powered by.*?Whitebird', 'Powered by <span style="color:#EAA914;font-weight:700;">⚡ Turbo Bytes Consulting (TBC)</span>', output_html, flags=re.IGNORECASE)
    output_html = re.sub(r'Whitebird', 'Turbo Bytes Consulting', output_html, flags=re.IGNORECASE)

    # Inject Sharda AI Brain & CSS (only once)
    if "turboModal" not in output_html and "turboFloatBar" not in output_html:
        if "</body>" in output_html:
            output_html = output_html.replace("</body>", f"{AI_WIDGET_INJECTION}\n</body>")
        else:
            output_html += AI_WIDGET_INJECTION

    return output_html

STATIC_EXTENSIONS = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".css": "text/css",
    ".js": "application/javascript",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".pdf": "application/pdf",
    ".ico": "image/x-icon"
}

@router.get("/replica/{full_path:path}")
@router.get("/replica")
@router.get("/")
async def render_exact_page(full_path: str = ""):
    clean_path = full_path.lstrip("/")
    ext = Path(clean_path).suffix.lower()

    # 1. Binary Static Asset Handling
    if ext in STATIC_EXTENSIONS:
        media_type = STATIC_EXTENSIONS[ext]
        local_file = BASE_DIR / "frontend" / "public" / clean_path
        if local_file.exists():
            return Response(content=local_file.read_bytes(), media_type=media_type)
        
        # Proxy binary asset directly from origin
        target_url = f"{SHARDA_ORIGIN}/{clean_path}"
        async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=15.0, follow_redirects=True) as client:
            try:
                resp = await client.get(target_url)
                if resp.status_code == 200:
                    return Response(content=resp.content, media_type=resp.headers.get("content-type", media_type))
                return Response(status_code=404)
            except Exception as e:
                logger.error(f"Error proxying binary asset {target_url}: {e}")
                return Response(status_code=404)

    # 2. Check local master database / index_replica.html first (< 3ms)
    db_html = get_page_from_db(full_path)
    if db_html and len(db_html) > 1000:
        return HTMLResponse(content=process_html(db_html, clean_path), status_code=200)

    # 3. Live fetch fallback if page is not yet cached
    target_url = f"{SHARDA_ORIGIN}/{clean_path}"
    logger.info(f"Live Ingesting Replica Page: {target_url}")

    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=15.0, follow_redirects=True) as client:
        try:
            resp = await client.get(target_url)
            if resp.status_code == 200:
                html = resp.text
                if "<html" in html.lower():
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        cur = conn.cursor()
                        cur.execute("""
                            INSERT OR REPLACE INTO pages (url, slug, category, title, meta_description, content_text, content_html, headings, status_code)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 200)
                        """, (target_url, clean_path.lower(), clean_path.split("/")[0] if "/" in clean_path else "general", clean_path, "", "", html, "[]"))
                        conn.commit()
                        conn.close()
                    except:
                        pass

                return HTMLResponse(content=process_html(html, clean_path), status_code=200)
        except Exception as e:
            logger.error(f"Error fetching {target_url}: {e}")

    # 4. Graceful authentic Sharda University catalog fallback
    home_html_path = BASE_DIR / "frontend" / "public" / "index_replica.html"
    if home_html_path.exists():
        fallback_html = home_html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=process_html(fallback_html, clean_path), status_code=200)

    return HTMLResponse(content="<h1>Sharda University Replica Loading...</h1>", status_code=200)

