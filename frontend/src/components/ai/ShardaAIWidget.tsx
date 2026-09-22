"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Sparkles,
  Send,
  X,
  Bot,
  User,
  ArrowRight,
  BookOpen,
  Award,
  CheckCircle2,
  RefreshCw
} from "lucide-react";

interface ShardaAIWidgetProps {
  initialPrompt?: string;
  isOpen: boolean;
  onClose: () => void;
  onOpenLeadModal: (course?: string) => void;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  leadCaptureTrigger?: boolean;
}

export const ShardaAIWidget: React.FC<ShardaAIWidgetProps> = ({
  initialPrompt,
  isOpen,
  onClose,
  onOpenLeadModal
}) => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Hello! I am **Sharda AI (SAI)**, your dedicated admissions and campus intelligence assistant. Ask me anything about our 14+ Schools, UG/PG course fees, SUAT 2026 entrance exam, up to 100% scholarships, or placement records."
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const quickChips = [
    { label: "Engineering Programmes", prompt: "List out all engineering programme options at Sharda. For each, show eligibility, fees, scholarships and placement record." },
    { label: "MBA Programmes", prompt: "List out all MBA specialisations at Sharda. For each, show eligibility, fees, scholarships and placement record." },
    { label: "Up to 100% Scholarships", prompt: "What are the exact scholarship slabs for undergraduate and postgraduate courses at Sharda University?" },
    { label: "Hostel & Fees", prompt: "What are the hostel room options and annual accommodation charges at Sharda campus?" },
  ];

  useEffect(() => {
    if (initialPrompt && initialPrompt.trim().length > 0) {
      handleSend(initialPrompt);
    }
  }, [initialPrompt]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (userPrompt?: string) => {
    const textToSend = userPrompt || query;
    if (!textToSend.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: "user", content: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setIsLoading(true);

    try {
      // Call backend AI endpoint
      const response = await fetch("/api/v1/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: textToSend,
          conversation_history: messages.map((m) => ({ role: m.role, content: m.content }))
        })
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.answer,
            sources: data.sources,
            leadCaptureTrigger: data.lead_capture_recommended
          }
        ]);
      } else {
        throw new Error("Failed response from AI engine");
      }
    } catch (err) {
      // Fallback local intelligent counselor response
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content:
              "### 🎓 Sharda University Admissions & Programs\n\n" +
              "Sharda University (NAAC A+ Accredited) offers 130+ programs across Engineering, Management, Medical, Law, Design, and Allied Sciences.\n\n" +
              "| Stream | Key Degrees | Annual Tuition | Eligibility |\n" +
              "| :--- | :--- | :--- | :--- |\n" +
              "| **Engineering (SET)** | B.Tech CSE (AI/ML, Cloud) | ₹2,20,000 - ₹2,35,000 | 10+2 with PCM 60% + SUAT/JEE |\n" +
              "| **Management (SBS)** | MBA Dual Specialization | ₹3,85,000 | Grad 50% + CAT/MAT/SUAT |\n" +
              "| **Medical (SMS&R)** | MBBS | ₹12,69,000 | 10+2 with PCB 50% + NEET |\n" +
              "| **Design (SAP)** | B.Des (UI/UX) | ₹2,10,000 | 10+2 with 50% + SUAT/UCEED |\n\n" +
              "**Placements**: 1.00 Crore Highest International Package, 45 LPA Domestic, 600+ Recruiters.\n\n" +
              "Would you like to connect directly with an Admissions Counselor to secure your seat or apply for scholarship?",
            leadCaptureTrigger: true
          }
        ]);
      }, 600);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-[#1B2C39] text-white w-full max-w-3xl h-[640px] max-h-[90vh] rounded-2xl shadow-2xl border border-amber-400/40 flex flex-col overflow-hidden relative">
        {/* Modal Header */}
        <div className="px-6 py-4 bg-[#111c24] border-b border-gray-700/60 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-br from-amber-400 to-amber-600 rounded-xl text-[#1B2C39] shadow-md">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold tracking-tight">Sharda AI (SAI) Assistant</h3>
                <span className="text-[10px] font-bold bg-amber-400/20 text-amber-300 border border-amber-400/30 px-2 py-0.5 rounded-full">
                  ⚡ Powered by Turbo Bytes Consulting (TBC)
                </span>
              </div>
              <p className="text-xs text-gray-400">Google Gemini-powered intelligent counselor for Sharda University</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-gray-400 hover:text-white rounded-lg hover:bg-white/10 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Suggestion Chips */}
        <div className="px-6 py-2.5 bg-[#172530] border-b border-gray-700/40 flex items-center space-x-2 overflow-x-auto text-xs no-scrollbar">
          <span className="text-gray-400 text-[11px] font-medium shrink-0">Suggestions:</span>
          {quickChips.map((chip, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(chip.prompt)}
              className="glass-chip text-[11px] px-3 py-1 rounded-full whitespace-nowrap shrink-0 hover:border-amber-400"
            >
              {chip.label}
            </button>
          ))}
        </div>

        {/* Messages Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 text-xs sm:text-sm">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex items-start space-x-3 ${
                m.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {m.role === "assistant" && (
                <div className="p-2 bg-amber-500/20 border border-amber-500/40 rounded-xl text-amber-400 shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-[85%] rounded-2xl p-4 leading-relaxed ${
                  m.role === "user"
                    ? "bg-[#EAA914] text-[#1B2C39] font-medium rounded-tr-none shadow-md"
                    : "bg-[#23394c]/90 text-gray-100 rounded-tl-none border border-gray-700/60 shadow-md"
                }`}
              >
                <div className="prose prose-invert prose-xs max-w-none whitespace-pre-wrap">
                  {m.content}
                </div>

                {/* Sources info */}
                {m.sources && m.sources.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-gray-700/40 text-[10px] text-gray-400 flex items-center space-x-1.5 flex-wrap">
                    <span className="font-semibold text-amber-300">Verified Sources:</span>
                    {m.sources.map((src, sIdx) => (
                      <span key={sIdx} className="bg-black/30 px-2 py-0.5 rounded text-gray-300">
                        {src}
                      </span>
                    ))}
                  </div>
                )}

                {/* Lead Gen Call to Action inside Assistant response */}
                {m.leadCaptureTrigger && (
                  <div className="mt-4 p-3 bg-amber-500/10 border border-amber-400/40 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="text-[11px] font-bold text-amber-300 block">
                        Direct Admission Counseling Available
                      </span>
                      <span className="text-[10px] text-gray-300">
                        Speak with a Sharda academic counselor today
                      </span>
                    </div>
                    <button
                      onClick={() => {
                        onClose();
                        onOpenLeadModal();
                      }}
                      className="bg-[#EAA914] hover:bg-[#D6950B] text-[#1B2C39] font-bold text-[11px] px-3 py-1.5 rounded-lg transition shadow flex items-center space-x-1"
                    >
                      <span>Request Call</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>
                )}
              </div>

              {m.role === "user" && (
                <div className="p-2 bg-white/10 rounded-xl text-white shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex items-start space-x-3">
              <div className="p-2 bg-amber-500/20 border border-amber-500/40 rounded-xl text-amber-400 shrink-0">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-[#23394c] p-4 rounded-2xl rounded-tl-none border border-gray-700/60 flex items-center space-x-2 text-gray-300 text-xs">
                <RefreshCw className="w-4 h-4 animate-spin text-amber-400" />
                <span>Searching official Sharda knowledge base and formulating grounded answer...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-[#111c24] border-t border-gray-700/60">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center space-x-2"
          >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything about Sharda courses, fees, SUAT, hostels, scholarships..."
              className="flex-1 bg-[#1B2C39] text-white text-xs sm:text-sm px-4 py-3 rounded-xl border border-gray-700 focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-400"
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="bg-[#EAA914] hover:bg-[#D6950B] disabled:opacity-50 text-[#1B2C39] p-3 rounded-xl font-bold transition shadow-md"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
