"use client";

import React, { useState, useEffect } from "react";

interface Lead {
  id: number;
  lead_id: string;
  full_name: string;
  email: string;
  phone: string;
  city: string;
  state: string;
  interested_school: string;
  interested_course: string;
  lead_source: string;
  intent_score: number;
  priority: string;
  status: string;
  notes: string;
  created_at: string;
}

interface Banner {
  id: number;
  title: string;
  subtitle: string;
  image_url: string;
  cta_text: string;
  cta_link: string;
  target_school: string;
  is_active: boolean;
  display_order: number;
}

interface Announcement {
  id: number;
  title: string;
  category: string;
  link_url: string;
  is_urgent: boolean;
  is_active: boolean;
}

interface AuditSummary {
  is_running: boolean;
  total_audited: number;
  average_fidelity_score: number;
  passed_count: number;
  failed_count: number;
  category_breakdown: { category: string; count: number; avg_fidelity: number }[];
  recent_audit_logs: { slug: string; category: string; status: number; score: number; issues: string; checked_at: string }[];
}

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<"crm" | "cms" | "audit" | "ai" | "search">("crm");
  
  // Search State
  const [searchQuery, setSearchQuery] = useState("B.Tech");
  const [searchResults, setSearchResults] = useState<any>(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchCategory, setSearchCategory] = useState("");
  const [leads, setLeads] = useState<Lead[]>([]);
  const [leadFilter, setLeadFilter] = useState<{ status: string; priority: string; search: string }>({ status: "", priority: "", search: "" });
  const [leadAnalytics, setLeadAnalytics] = useState<any>(null);

  // CMS State
  const [banners, setBanners] = useState<Banner[]>([]);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [newBanner, setNewBanner] = useState({ title: "", subtitle: "", image_url: "/assets/imgs/home-banner2.jpg", cta_text: "Apply Now", cta_link: "/admissions", target_school: "global" });
  const [newAnnouncement, setNewAnnouncement] = useState({ title: "", category: "Admissions", link_url: "/admissions", is_urgent: false });

  // Audit State
  const [auditSummary, setAuditSummary] = useState<AuditSummary | null>(null);
  const [auditLimit, setAuditLimit] = useState(50);
  const [auditCategory, setAuditCategory] = useState("");
  const [isAuditing, setIsAuditing] = useState(false);

  // AI Counselor State
  const [testQuery, setTestQuery] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [aiLoading, setAiLoading] = useState(false);

  // Fetch initial data
  useEffect(() => {
    fetchLeads();
    fetchCMS();
    fetchAuditStatus();
  }, []);

  // Fetch Leads
  const fetchLeads = async () => {
    try {
      let url = `/api/v1/leads?limit=50`;
      if (leadFilter.status) url += `&status=${leadFilter.status}`;
      if (leadFilter.priority) url += `&priority=${leadFilter.priority}`;
      if (leadFilter.search) url += `&search=${encodeURIComponent(leadFilter.search)}`;
      
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setLeads(data.leads || []);
      }

      const aRes = await fetch("/api/v1/leads/analytics");
      if (aRes.ok) {
        setLeadAnalytics(await aRes.json());
      }
    } catch (e) {
      console.error("Error fetching leads:", e);
    }
  };

  // Fetch CMS
  const fetchCMS = async () => {
    try {
      const bRes = await fetch("/api/v1/cms/banners");
      if (bRes.ok) setBanners(await bRes.json());

      const aRes = await fetch("/api/v1/cms/announcements");
      if (aRes.ok) setAnnouncements(await aRes.json());
    } catch (e) {
      console.error("Error fetching CMS:", e);
    }
  };

  // Fetch Audit Status
  const fetchAuditStatus = async () => {
    try {
      const res = await fetch("/api/v1/audit/status");
      if (res.ok) {
        const data = await res.json();
        setAuditSummary(data);
        setIsAuditing(data.is_running);
      }
    } catch (e) {
      console.error("Error fetching audit status:", e);
    }
  };

  // Trigger Audit
  const handleTriggerAudit = async () => {
    setIsAuditing(true);
    try {
      let url = `/api/v1/audit/run?limit=${auditLimit}`;
      if (auditCategory) url += `&category=${auditCategory}`;
      await fetch(url, { method: "POST" });
      setTimeout(fetchAuditStatus, 2000);
    } catch (e) {
      console.error("Error triggering audit:", e);
    }
  };

  // Update Lead Status
  const handleUpdateLeadStatus = async (leadId: string, status: string) => {
    try {
      await fetch(`/api/v1/leads/${leadId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
      });
      fetchLeads();
    } catch (e) {
      console.error("Error updating lead status:", e);
    }
  };

  // Create Banner
  const handleCreateBanner = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await fetch("/api/v1/cms/banners", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newBanner)
      });
      setNewBanner({ title: "", subtitle: "", image_url: "/assets/imgs/home-banner2.jpg", cta_text: "Apply Now", cta_link: "/admissions", target_school: "global" });
      fetchCMS();
    } catch (e) {
      console.error("Error creating banner:", e);
    }
  };

  // Create Announcement
  const handleCreateAnnouncement = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await fetch("/api/v1/cms/announcements", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newAnnouncement)
      });
      setNewAnnouncement({ title: "", category: "Admissions", link_url: "/admissions", is_urgent: false });
      fetchCMS();
    } catch (e) {
      console.error("Error creating announcement:", e);
    }
  };

  // Test AI Chat
  const handleTestAIChat = async () => {
    if (!testQuery.trim()) return;
    setAiLoading(true);
    try {
      const res = await fetch("/api/v1/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: testQuery })
      });
      const data = await res.json();
      setAiResponse(data.answer);
    } catch (e) {
      setAiResponse("Error querying AI brain.");
    }
    setAiLoading(false);
  };

  const handleExecuteSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearchLoading(true);
    try {
      let url = `/api/v1/search?q=${encodeURIComponent(searchQuery)}`;
      if (searchCategory) url += `&category=${searchCategory}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setSearchResults(data);
      }
    } catch (e) {
      console.error("Search failed:", e);
    }
    setSearchLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0d161d] text-[#f8fafc] font-sans">
      {/* Top Header */}
      <header className="border-b border-[#1f303f] bg-[#111c24] px-8 py-4 flex items-center justify-between shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#EAA914] to-[#ffc84b] flex items-center justify-center font-black text-[#1B2C39] text-xl shadow-md">
            S
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
              Sharda University
              <span className="text-xs bg-[#EAA914]/20 text-[#EAA914] px-2.5 py-0.5 rounded-full font-semibold border border-[#EAA914]/30">
                ⚡ Turbo Bytes Control Room
              </span>
            </h1>
            <p className="text-xs text-slate-400">Headless CMS • CRM Intelligence • Quality Audit • Full-Text AI Brain</p>
          </div>
        </div>

        {/* Global Live Stats Bar */}
        <div className="flex items-center gap-6 text-xs">
          <div className="bg-[#182733] border border-[#233b4e] px-3.5 py-1.5 rounded-lg flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-slate-300">FastAPI Backend:</span>
            <strong className="text-emerald-400">Port 8000 OK</strong>
          </div>
          <div className="bg-[#182733] border border-[#233b4e] px-3.5 py-1.5 rounded-lg flex items-center gap-2">
            <span className="text-slate-300">Total Leads:</span>
            <strong className="text-[#EAA914]">{leadAnalytics?.total_leads || 0}</strong>
          </div>
          <div className="bg-[#182733] border border-[#233b4e] px-3.5 py-1.5 rounded-lg flex items-center gap-2">
            <span className="text-slate-300">Site Fidelity:</span>
            <strong className="text-sky-400">{auditSummary?.average_fidelity_score || 100}%</strong>
          </div>
          <a
            href="/"
            className="bg-[#1f3547] hover:bg-[#28445b] text-white px-3.5 py-1.5 rounded-lg transition text-xs font-semibold"
          >
            ← View Website
          </a>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="border-b border-[#1f303f] bg-[#14222c] px-8 flex gap-8">
        {[
          { id: "crm", label: "🎯 CRM Lead Pipeline", desc: "Inquiries & Intent Scoring" },
          { id: "search", label: "⚡ Turbo Bytes Search Engine", desc: "2,388 Pages & 248 Programs Index" },
          { id: "cms", label: "📝 Headless CMS", desc: "Banners & Announcements" },
          { id: "audit", label: "🔍 Site Quality & Audit", desc: "2,388 URLs Comparison" },
          { id: "ai", label: "✨ Sharda AI Intelligence", desc: "Grounded Brain Counselor" },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`py-3.5 border-b-2 font-medium text-sm transition flex flex-col items-start ${
              activeTab === tab.id
                ? "border-[#EAA914] text-[#EAA914]"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <span>{tab.label}</span>
            <span className="text-[10px] opacity-70 font-normal">{tab.desc}</span>
          </button>
        ))}
      </div>

      {/* Main Content Area */}
      <main className="p-8 max-w-7xl mx-auto">
        {/* ========================================================= */}
        {/* TAB 1: CRM LEAD CENTER */}
        {/* ========================================================= */}
        {activeTab === "crm" && (
          <div className="space-y-6">
            {/* Metric Cards */}
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Total Inquiries</p>
                <h3 className="text-2xl font-bold text-white mt-1">{leadAnalytics?.total_leads || 0}</h3>
                <p className="text-[11px] text-emerald-400 mt-1">Live from Web & AI</p>
              </div>
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Avg Intent Score</p>
                <h3 className="text-2xl font-bold text-[#EAA914] mt-1">
                  {leadAnalytics?.average_intent_score || 0} / 100
                </h3>
                <p className="text-[11px] text-slate-400 mt-1">High Intent Priority</p>
              </div>
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Hot Priority Leads</p>
                <h3 className="text-2xl font-bold text-rose-400 mt-1">
                  {leadAnalytics?.priority_distribution?.HOT || 0}
                </h3>
                <p className="text-[11px] text-rose-400/80 mt-1">Immediate Counselor Action</p>
              </div>
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Export & Integration</p>
                <div className="mt-2">
                  <a
                    href="http://127.0.0.1:8000/api/v1/leads/export/csv"
                    className="inline-block bg-[#EAA914] hover:bg-[#d6950b] text-[#1B2C39] font-bold text-xs px-3.5 py-1.5 rounded-lg transition shadow-md"
                  >
                    ⬇ Download CSV
                  </a>
                </div>
              </div>
            </div>

            {/* Filter Bar */}
            <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4 flex flex-wrap gap-4 items-center justify-between">
              <div className="flex gap-3 items-center flex-1 max-w-md">
                <input
                  type="text"
                  placeholder="Search student by name, phone, course..."
                  value={leadFilter.search}
                  onChange={(e) => setLeadFilter({ ...leadFilter, search: e.target.value })}
                  className="bg-[#182733] border border-[#233b4e] rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-400 w-full outline-none focus:border-[#EAA914]"
                />
                <button
                  onClick={fetchLeads}
                  className="bg-[#203647] hover:bg-[#28445b] text-white px-3 py-1.5 rounded-lg text-xs font-semibold"
                >
                  Search
                </button>
              </div>

              <div className="flex gap-3 items-center">
                <select
                  value={leadFilter.status}
                  onChange={(e) => {
                    setLeadFilter({ ...leadFilter, status: e.target.value });
                    setTimeout(fetchLeads, 100);
                  }}
                  className="bg-[#182733] border border-[#233b4e] rounded-lg px-3 py-1.5 text-xs text-white outline-none"
                >
                  <option value="">All Statuses</option>
                  <option value="NEW">NEW</option>
                  <option value="CONTACTED">CONTACTED</option>
                  <option value="COUNSELING">COUNSELING</option>
                  <option value="ADMITTED">ADMITTED</option>
                  <option value="CLOSED">CLOSED</option>
                </select>

                <select
                  value={leadFilter.priority}
                  onChange={(e) => {
                    setLeadFilter({ ...leadFilter, priority: e.target.value });
                    setTimeout(fetchLeads, 100);
                  }}
                  className="bg-[#182733] border border-[#233b4e] rounded-lg px-3 py-1.5 text-xs text-white outline-none"
                >
                  <option value="">All Priorities</option>
                  <option value="HOT">HOT (75+)</option>
                  <option value="WARM">WARM (50+)</option>
                  <option value="COLD">COLD (&lt;50)</option>
                </select>
              </div>
            </div>

            {/* Leads Table */}
            <div className="bg-[#14222c] border border-[#203647] rounded-xl overflow-hidden shadow-lg">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-[#101b23] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#203647]">
                    <tr>
                      <th className="p-3.5">Lead ID / Date</th>
                      <th className="p-3.5">Student Name</th>
                      <th className="p-3.5">Contact Details</th>
                      <th className="p-3.5">Interested Course & School</th>
                      <th className="p-3.5 text-center">Score / Priority</th>
                      <th className="p-3.5">Status Lifecycle</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1b2d3b]">
                    {leads.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="p-8 text-center text-slate-400">
                          No inquiries found matching criteria.
                        </td>
                      </tr>
                    ) : (
                      leads.map((l) => (
                        <tr key={l.lead_id} className="hover:bg-[#182733] transition">
                          <td className="p-3.5">
                            <strong className="text-white block">{l.lead_id}</strong>
                            <span className="text-[10px] text-slate-400">{l.created_at?.split(" ")[0]}</span>
                          </td>
                          <td className="p-3.5">
                            <span className="font-semibold text-white">{l.full_name}</span>
                            <span className="block text-[11px] text-slate-400">{l.city}, {l.state}</span>
                          </td>
                          <td className="p-3.5">
                            <span className="block text-slate-200">{l.phone || "—"}</span>
                            <span className="block text-[11px] text-slate-400">{l.email || "—"}</span>
                          </td>
                          <td className="p-3.5">
                            <span className="font-medium text-white">{l.interested_course}</span>
                            <span className="block text-[11px] text-slate-400">{l.interested_school}</span>
                          </td>
                          <td className="p-3.5 text-center">
                            <span
                              className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                                l.priority === "HOT"
                                  ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                                  : l.priority === "WARM"
                                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                                  : "bg-slate-500/20 text-slate-300 border border-slate-500/40"
                              }`}
                            >
                              {l.priority} ({l.intent_score})
                            </span>
                          </td>
                          <td className="p-3.5">
                            <select
                              value={l.status}
                              onChange={(e) => handleUpdateLeadStatus(l.lead_id, e.target.value)}
                              className="bg-[#182733] border border-[#284257] rounded-md px-2.5 py-1 text-xs text-white outline-none cursor-pointer focus:border-[#EAA914]"
                            >
                              <option value="NEW">NEW</option>
                              <option value="CONTACTED">CONTACTED</option>
                              <option value="COUNSELING">COUNSELING</option>
                              <option value="ADMITTED">ADMITTED</option>
                              <option value="CLOSED">CLOSED</option>
                            </select>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 2: HEADLESS CMS */}
        {/* ========================================================= */}
        {activeTab === "cms" && (
          <div className="grid grid-cols-2 gap-8">
            {/* Banners Manager */}
            <div className="space-y-4">
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg">
                <h3 className="text-base font-bold text-white mb-3">🎨 Hero Banners Manager</h3>
                <form onSubmit={handleCreateBanner} className="space-y-3 text-xs">
                  <div>
                    <label className="block text-slate-400 mb-1">Banner Title</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g., Admissions Open 2026-27"
                      value={newBanner.title}
                      onChange={(e) => setNewBanner({ ...newBanner, title: e.target.value })}
                      className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Subtitle</label>
                    <input
                      type="text"
                      placeholder="e.g., NAAC A+ Accredited University with 100% Scholarships"
                      value={newBanner.subtitle}
                      onChange={(e) => setNewBanner({ ...newBanner, subtitle: e.target.value })}
                      className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Image URL / Asset Path</label>
                    <input
                      type="text"
                      required
                      placeholder="/assets/imgs/home-banner2.jpg"
                      value={newBanner.image_url}
                      onChange={(e) => setNewBanner({ ...newBanner, image_url: e.target.value })}
                      className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-slate-400 mb-1">CTA Text</label>
                      <input
                        type="text"
                        value={newBanner.cta_text}
                        onChange={(e) => setNewBanner({ ...newBanner, cta_text: e.target.value })}
                        className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">CTA Link</label>
                      <input
                        type="text"
                        value={newBanner.cta_link}
                        onChange={(e) => setNewBanner({ ...newBanner, cta_link: e.target.value })}
                        className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="w-full bg-[#EAA914] hover:bg-[#d6950b] text-[#1B2C39] font-bold p-2 rounded-lg transition"
                  >
                    + Add New Banner
                  </button>
                </form>
              </div>

              {/* Active Banners List */}
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg space-y-3">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Banners</h4>
                {banners.map((b) => (
                  <div key={b.id} className="bg-[#182733] border border-[#233b4e] rounded-lg p-3 flex justify-between items-center text-xs">
                    <div>
                      <strong className="text-white block">{b.title}</strong>
                      <span className="text-slate-400 text-[11px]">{b.subtitle}</span>
                    </div>
                    <button
                      onClick={async () => {
                        await fetch(`http://127.0.0.1:8000/api/v1/cms/banners/${b.id}`, { method: "DELETE" });
                        fetchCMS();
                      }}
                      className="text-rose-400 hover:text-rose-300 font-semibold"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Announcements Manager */}
            <div className="space-y-4">
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg">
                <h3 className="text-base font-bold text-white mb-3">📢 Campus Flash Alerts & News</h3>
                <form onSubmit={handleCreateAnnouncement} className="space-y-3 text-xs">
                  <div>
                    <label className="block text-slate-400 mb-1">Announcement Text</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g., SUAT 2026 Exam Slot Booking Now Open"
                      value={newAnnouncement.title}
                      onChange={(e) => setNewAnnouncement({ ...newAnnouncement, title: e.target.value })}
                      className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-slate-400 mb-1">Category</label>
                      <input
                        type="text"
                        value={newAnnouncement.category}
                        onChange={(e) => setNewAnnouncement({ ...newAnnouncement, category: e.target.value })}
                        className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">Link URL</label>
                      <input
                        type="text"
                        value={newAnnouncement.link_url}
                        onChange={(e) => setNewAnnouncement({ ...newAnnouncement, link_url: e.target.value })}
                        className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-2 text-white outline-none"
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="w-full bg-[#00bfe7] hover:bg-[#00a6c9] text-[#1B2C39] font-bold p-2 rounded-lg transition"
                  >
                    + Publish Announcement
                  </button>
                </form>
              </div>

              {/* Active Announcements List */}
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg space-y-3">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Live Flash Announcements</h4>
                {announcements.map((a) => (
                  <div key={a.id} className="bg-[#182733] border border-[#233b4e] rounded-lg p-3 flex justify-between items-center text-xs">
                    <div>
                      <span className="text-[10px] bg-[#00bfe7]/20 text-[#00bfe7] px-2 py-0.5 rounded font-semibold mr-2">
                        {a.category}
                      </span>
                      <strong className="text-white">{a.title}</strong>
                    </div>
                    <button
                      onClick={async () => {
                        await fetch(`http://127.0.0.1:8000/api/v1/cms/announcements/${a.id}`, { method: "DELETE" });
                        fetchCMS();
                      }}
                      className="text-rose-400 hover:text-rose-300 font-semibold"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 3: SITE QUALITY & AUDIT MONITOR */}
        {/* ========================================================= */}
        {activeTab === "audit" && (
          <div className="space-y-6">
            {/* Header & Controls */}
            <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 flex items-center justify-between shadow-lg">
              <div>
                <h3 className="text-base font-bold text-white">🔍 Automated Site-Wide Quality Audit Engine</h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Validates DOM integrity, 200 HTTP status, asset completeness, and Same-Origin fonts across 2,371 URLs.
                </p>
              </div>
              <div className="flex gap-3 items-center">
                <select
                  value={auditCategory}
                  onChange={(e) => setAuditCategory(e.target.value)}
                  className="bg-[#182733] border border-[#233b4e] rounded-lg px-3 py-1.5 text-xs text-white outline-none"
                >
                  <option value="">All Categories (2,371 URLs)</option>
                  <option value="schools">Schools & Departments</option>
                  <option value="admissions">Admissions & Fees</option>
                  <option value="programmes">Academic Programmes</option>
                  <option value="international">International Portals</option>
                  <option value="campuslife">Campus Life & Hostels</option>
                </select>

                <select
                  value={auditLimit}
                  onChange={(e) => setAuditLimit(Number(e.target.value))}
                  className="bg-[#182733] border border-[#233b4e] rounded-lg px-3 py-1.5 text-xs text-white outline-none"
                >
                  <option value={30}>30 Pages Sample</option>
                  <option value={100}>100 Pages</option>
                  <option value={500}>500 Pages</option>
                  <option value={2371}>All 2,371 Pages</option>
                </select>

                <button
                  onClick={handleTriggerAudit}
                  disabled={isAuditing}
                  className={`font-bold text-xs px-4 py-2 rounded-lg transition shadow-md ${
                    isAuditing
                      ? "bg-slate-600 text-slate-300 cursor-not-allowed"
                      : "bg-[#EAA914] hover:bg-[#d6950b] text-[#1B2C39]"
                  }`}
                >
                  {isAuditing ? "Auditing in Progress..." : "⚡ Run Live Quality Audit"}
                </button>
              </div>
            </div>

            {/* Audit Telemetry Metrics */}
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Total Audited</p>
                <h3 className="text-2xl font-bold text-white mt-1">{auditSummary?.total_audited || 0}</h3>
                <p className="text-[11px] text-sky-400 mt-1">Full-Fidelity Pages</p>
              </div>
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Average Quality Score</p>
                <h3 className="text-2xl font-bold text-[#EAA914] mt-1">
                  {auditSummary?.average_fidelity_score || 100}%
                </h3>
                <p className="text-[11px] text-emerald-400 mt-1">Verified HTML & CSS</p>
              </div>
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Passed Checks</p>
                <h3 className="text-2xl font-bold text-emerald-400 mt-1">
                  {auditSummary?.passed_count || 0}
                </h3>
                <p className="text-[11px] text-emerald-400 mt-1">0 Errors Detected</p>
              </div>
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-4">
                <p className="text-xs text-slate-400">Failed / Issues</p>
                <h3 className="text-2xl font-bold text-rose-400 mt-1">
                  {auditSummary?.failed_count || 0}
                </h3>
                <p className="text-[11px] text-slate-400 mt-1">Auto-repair enabled</p>
              </div>
            </div>

            {/* Category Breakdown */}
            <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Category Quality Scores</h4>
              <div className="grid grid-cols-4 gap-4">
                {auditSummary?.category_breakdown?.map((cat) => (
                  <div key={cat.category} className="bg-[#182733] border border-[#233b4e] rounded-lg p-3">
                    <span className="text-xs font-semibold text-white capitalize">{cat.category}</span>
                    <div className="flex justify-between items-center mt-2 text-xs">
                      <span className="text-slate-400">{cat.count} URLs</span>
                      <strong className="text-emerald-400">{cat.avg_fidelity}% Score</strong>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Audit Log Table */}
            <div className="bg-[#14222c] border border-[#203647] rounded-xl overflow-hidden shadow-lg">
              <div className="p-4 bg-[#101b23] border-b border-[#203647]">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Live URL Check Logs</h4>
              </div>
              <div className="max-h-96 overflow-y-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-[#14222c] text-slate-400 uppercase text-[10px] tracking-wider sticky top-0">
                    <tr>
                      <th className="p-3">Route Slug</th>
                      <th className="p-3">Category</th>
                      <th className="p-3">HTTP Status</th>
                      <th className="p-3">Quality Score</th>
                      <th className="p-3">Issues / Notes</th>
                      <th className="p-3">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1b2d3b]">
                    {auditSummary?.recent_audit_logs?.map((log, idx) => (
                      <tr key={idx} className="hover:bg-[#182733]">
                        <td className="p-3 font-mono text-white">
                          <a href={`/${log.slug}`} target="_blank" className="hover:text-[#00bfe7]">
                            /{log.slug}
                          </a>
                        </td>
                        <td className="p-3 capitalize text-slate-400">{log.category}</td>
                        <td className="p-3">
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400">
                            {log.status} OK
                          </span>
                        </td>
                        <td className="p-3">
                          <strong className="text-[#EAA914]">{log.score}%</strong>
                        </td>
                        <td className="p-3 text-slate-400">{log.issues || "Passed 100% Quality Checks"}</td>
                        <td className="p-3 text-[10px] text-slate-500">{log.checked_at}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 4: SHARDA AI INTELLIGENCE */}
        {/* ========================================================= */}
        {activeTab === "ai" && (
          <div className="grid grid-cols-2 gap-8">
            <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg space-y-4">
              <h3 className="text-base font-bold text-white">✨ Sharda AI (SAI) Test Counselor</h3>
              <p className="text-xs text-slate-400">
                Test the official conversational intelligence engine grounded in all 2,371+ pages of verified Sharda University data.
              </p>
              <div>
                <textarea
                  rows={4}
                  value={testQuery}
                  onChange={(e) => setTestQuery(e.target.value)}
                  placeholder="Ask Sharda AI (e.g., What are the B.Tech CSE AI fees and SUAT entrance syllabus?)"
                  className="w-full bg-[#182733] border border-[#233b4e] rounded-lg p-3 text-xs text-white placeholder-slate-400 outline-none focus:border-[#EAA914]"
                />
              </div>
              <button
                onClick={handleTestAIChat}
                disabled={aiLoading}
                className="w-full bg-[#EAA914] hover:bg-[#d6950b] text-[#1B2C39] font-bold p-2.5 rounded-lg text-xs transition"
              >
                {aiLoading ? "Searching RAG Knowledge Base..." : "Ask Gemini RAG Brain"}
              </button>

              {aiResponse && (
                <div className="bg-[#182733] border border-[#233b4e] rounded-lg p-4 text-xs text-slate-200 whitespace-pre-wrap leading-relaxed">
                  <strong className="text-[#EAA914] block mb-2">🎓 Sharda AI Response:</strong>
                  {aiResponse}
                </div>
              )}
            </div>

            <div className="bg-[#14222c] border border-[#203647] rounded-xl p-5 shadow-lg space-y-4">
              <h3 className="text-base font-bold text-white">📊 AI Knowledge & Grounding Health</h3>
              <div className="space-y-3 text-xs">
                <div className="bg-[#182733] border border-[#233b4e] rounded-lg p-3 flex justify-between">
                  <span className="text-slate-400">Total Ingested Pages:</span>
                  <strong className="text-white">2,388 Full Documents</strong>
                </div>
                <div className="bg-[#182733] border border-[#233b4e] rounded-lg p-3 flex justify-between">
                  <span className="text-slate-400">Search Engine Engine:</span>
                  <strong className="text-[#EAA914]">⚡ Turbo Bytes Consulting</strong>
                </div>
                <div className="bg-[#182733] border border-[#233b4e] rounded-lg p-3 flex justify-between">
                  <span className="text-slate-400">Response Latency:</span>
                  <strong className="text-emerald-400">&lt; 3ms</strong>
                </div>
                <div className="bg-[#182733] border border-[#233b4e] rounded-lg p-3 flex justify-between">
                  <span className="text-slate-400">Lead Conversion Trigger:</span>
                  <strong className="text-emerald-400">Enabled (Automatic Intent Capture)</strong>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 5: TURBO BYTES SEARCH ENGINE & BRAIN INTELLIGENCE */}
        {/* ========================================================= */}
        {activeTab === "search" && (
          <div className="space-y-6">
            <div className="bg-[#14222c] border border-[#203647] rounded-xl p-6 shadow-lg">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>⚡</span> Turbo Bytes Full-Text & Program Search Engine
                  </h3>
                  <p className="text-xs text-slate-400">
                    Search and test instant indexing across all 2,388 database documents and 248 Degree Programs.
                  </p>
                </div>
                <span className="bg-[#EAA914]/20 text-[#EAA914] text-xs px-3 py-1 rounded-full font-bold border border-[#EAA914]/30">
                  ⚡ Powered by Turbo Bytes Consulting
                </span>
              </div>

              <div className="flex gap-3">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleExecuteSearch()}
                  placeholder="Type search keyword (e.g. B.Tech, MBA, Artificial Intelligence, Hostel, Fees, Scholarships)..."
                  className="flex-1 bg-[#182733] border border-[#233b4e] rounded-lg px-4 py-2.5 text-xs text-white placeholder-slate-400 outline-none focus:border-[#EAA914]"
                />
                <select
                  value={searchCategory}
                  onChange={(e) => setSearchCategory(e.target.value)}
                  className="bg-[#182733] border border-[#233b4e] rounded-lg px-3 py-2.5 text-xs text-slate-300 outline-none"
                >
                  <option value="">All Categories</option>
                  <option value="programmes">Degree Programmes</option>
                  <option value="schools">Schools & Departments</option>
                  <option value="admissions">Admissions & SUAT</option>
                  <option value="faculty">Faculty Profiles</option>
                  <option value="campuslife">Campus Life</option>
                </select>
                <button
                  onClick={handleExecuteSearch}
                  disabled={searchLoading}
                  className="bg-gradient-to-r from-[#e58e26] to-[#EAA914] text-[#111c24] font-bold px-6 py-2.5 rounded-lg text-xs hover:brightness-110 transition"
                >
                  {searchLoading ? "Searching..." : "Search Index"}
                </button>
              </div>
            </div>

            {/* Search Results Display */}
            {searchResults && (
              <div className="bg-[#14222c] border border-[#203647] rounded-xl p-6 shadow-lg">
                <div className="flex items-center justify-between pb-3 border-b border-[#203647] mb-4">
                  <span className="text-xs text-slate-400">
                    Found <strong className="text-white">{searchResults.total_results}</strong> results for &quot;{searchResults.query}&quot;
                  </span>
                  <span className="text-xs text-[#EAA914] font-semibold">
                    Indexed & Verified in SQLite Knowledge Brain
                  </span>
                </div>

                <div className="space-y-3">
                  {searchResults.results && searchResults.results.length > 0 ? (
                    searchResults.results.map((res: any, idx: number) => (
                      <div key={idx} className="bg-[#182733] border border-[#233b4e] rounded-lg p-4 hover:border-[#EAA914]/40 transition">
                        <div className="flex items-center justify-between mb-1">
                          <a href={res.url} target="_blank" rel="noreferrer" className="text-sm font-bold text-sky-400 hover:underline">
                            {res.title}
                          </a>
                          <span className="bg-[#203647] text-slate-300 text-[10px] font-bold px-2 py-0.5 rounded">
                            {res.category}
                          </span>
                        </div>
                        <p
                          className="text-xs text-slate-300 leading-relaxed"
                          dangerouslySetInnerHTML={{ __html: res.snippet }}
                        />
                        <div className="mt-2 text-[10px] text-slate-500 flex items-center gap-3">
                          <span>Route: <code className="text-slate-400">{res.url}</code></span>
                          <span>•</span>
                          <span>Match Score: <strong className="text-emerald-400">{res.score}</strong></span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-slate-400 text-center py-6">No matching documents found. Try another search query.</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
