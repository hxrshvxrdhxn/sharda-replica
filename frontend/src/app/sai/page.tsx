"use client";

import React, { useState, useRef, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Sparkles,
  Send,
  ArrowRight,
  Bot,
  User,
  ArrowLeft,
  Copy,
  Check,
  RotateCcw,
  BookOpen,
  GraduationCap,
  Building2,
  Award,
  ExternalLink,
  ChevronRight,
  HelpCircle
} from "lucide-react";
import { TurboMarkdownView } from "@/components/ai/TurboMarkdownView";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  matched_programs?: Array<{
    title: string;
    school: string;
    annual_fee: string;
    duration: string;
    url: string;
  }>;
  timestamp: string;
}

export default function SAIPage() {
  const [inputQuery, setInputQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const chatBottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const starterCards = [
    {
      title: "B.Tech CSE & AI Specialisations",
      desc: "Curriculum, 4-year fee structure, eligibility & ₹1 Cr placement highlights.",
      prompt: "What are the B.Tech CSE specialisations, annual fees, eligibility, and placement records for 2026?",
      icon: GraduationCap,
      color: "from-blue-500/20 to-cyan-500/10 border-blue-500/30 text-blue-400"
    },
    {
      title: "MBA & Dual Specialisations",
      desc: "IACBE accredited management programs, GD/PI rounds, and average CTC.",
      prompt: "What are the MBA specialisations at Sharda University, fees, eligibility, and top recruiters?",
      icon: Building2,
      color: "from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400"
    },
    {
      title: "Up to 100% Merit Scholarships",
      desc: "Board score slabs, JEE rank waivers, sports, and sibling concessions.",
      prompt: "Explain the exact scholarship criteria and fee waiver slabs for 2026 admissions.",
      icon: Award,
      color: "from-amber-500/20 to-yellow-500/10 border-amber-500/30 text-amber-400"
    },
    {
      title: "SUAT 2026 & Admissions Deadlines",
      desc: "Online entrance exam format, slot booking, syllabus, and closing dates.",
      prompt: "When do 2026 admissions close at Sharda University and how do I register for SUAT?",
      icon: HelpCircle,
      color: "from-purple-500/20 to-pink-500/10 border-purple-500/30 text-purple-400"
    }
  ];

  const followUpSuggestions = [
    "What is the hostel fee structure?",
    "Tell me about MBBS & Dental admission process",
    "Calculate my scholarship for 92% in 12th",
    "What is SUAT 2026 syllabus?"
  ];

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (textToSend?: string) => {
    const query = (textToSend || inputQuery).trim();
    if (!query || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputQuery("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/v1/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          conversation_history: messages.map((m) => ({ role: m.role, content: m.content }))
        })
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage: Message = {
          id: `ai-${Date.now()}`,
          role: "assistant",
          content: data.answer || data.response || "No response received.",
          sources: data.sources || [],
          matched_programs: data.matched_programs || [],
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        };
        setMessages((prev) => [...prev, aiMessage]);
      } else {
        throw new Error("Failed AI response");
      }
    } catch {
      const fallbackAiMessage: Message = {
        id: `ai-err-${Date.now()}`,
        role: "assistant",
        content:
          "**Admissions for 2026 at Sharda University (NAAC A+ Accredited) are open.**\n\n" +
          "- **B.Tech CSE**: 4 Years | ₹2,20,000 / yr | 10+2 PCM min 60% + SUAT/JEE\n" +
          "- **MBA**: 2 Years | ₹3,85,000 / yr | Graduation 50% + MAT/CAT/SUAT\n" +
          "- **Merit Scholarships**: Up to 100% tuition waiver available\n\n" +
          "🔗 [View Admissions Portal 2026](/admissions)\n" +
          "🔗 [Explore B.Tech CSE Details](/programmes/b-tech-cse)",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      };
      setMessages((prev) => [...prev, fallbackAiMessage]);
    } finally {
      setIsLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleResetChat = () => {
    setMessages([]);
    setInputQuery("");
    inputRef.current?.focus();
  };

  return (
    <div className="min-h-screen bg-[#0d141b] text-slate-100 flex flex-col justify-between font-sans selection:bg-amber-400 selection:text-slate-900">
      {/* Sleek Top Navigation Header */}
      <header className="sticky top-0 z-30 bg-[#0d141b]/80 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-8 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3 sm:gap-6">
          <Link
            href="/"
            className="flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 px-3 py-1.5 rounded-lg transition-all"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Back to Sharda Portal</span>
            <span className="sm:hidden">Portal</span>
          </Link>

          <div className="flex items-center gap-3">
            <div className="relative w-28 h-8 sm:w-36 sm:h-9">
              <Image
                src="/assets/logo.png"
                alt="Sharda Logo"
                fill
                className="object-contain filter brightness-0 invert"
                priority
              />
            </div>
            <div className="h-5 w-[1px] bg-slate-700/60 hidden sm:block" />
            <div className="hidden sm:flex items-center gap-1.5 bg-amber-400/10 border border-amber-400/30 px-2.5 py-0.5 rounded-full text-[11px] font-bold text-amber-300">
              <Sparkles className="w-3 h-3 text-amber-400" />
              <span>Gemini 3.6 Flash</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={handleResetChat}
              className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 hover:text-white bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 px-3 py-1.5 rounded-lg transition-all"
              title="Start a new conversation"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">New Chat</span>
            </button>
          )}

          <div className="flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-full text-[11px] font-medium text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>Online</span>
          </div>
        </div>
      </header>

      {/* Main Conversation Canvas */}
      <main className="flex-1 w-full max-w-4xl mx-auto px-4 sm:px-6 py-6 flex flex-col justify-start">
        {messages.length === 0 ? (
          /* Empty State - Modern AI Tool Discovery Hero */
          <div className="my-auto py-8 sm:py-12 flex flex-col items-center text-center animate-in fade-in duration-500">
            <div className="inline-flex items-center gap-2 bg-gradient-to-r from-amber-400/15 via-orange-400/15 to-amber-400/15 border border-amber-400/40 px-4 py-1.5 rounded-full text-xs font-bold text-amber-300 shadow-sm mb-6">
              <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-spin-slow" />
              <span>SHARDA AI CONVERSATIONAL ADMISSIONS BRAIN</span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-white max-w-2xl leading-tight">
              What would you like to know about <span className="bg-gradient-to-r from-amber-300 via-amber-400 to-orange-400 bg-clip-text text-transparent">Sharda University</span>?
            </h1>
            <p className="text-slate-400 text-sm sm:text-base mt-3 max-w-xl">
              Instant, verified answers on 130+ programs, fee schedules, up to 100% scholarships, SUAT 2026 entrance exam, and global placements.
            </p>

            {/* Quick Starter Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 w-full mt-10 text-left">
              {starterCards.map((card, idx) => {
                const IconComponent = card.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => handleSend(card.prompt)}
                    className={`group p-4 sm:p-5 rounded-2xl bg-gradient-to-br ${card.color} border hover:border-amber-400/60 transition-all duration-300 shadow-lg hover:shadow-amber-400/5 flex flex-col justify-between text-left`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="p-2 rounded-xl bg-slate-900/60 text-amber-400 border border-slate-700/50">
                          <IconComponent className="w-4 h-4" />
                        </span>
                        <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition-all" />
                      </div>
                      <h3 className="font-bold text-sm text-white group-hover:text-amber-300 transition-colors">
                        {card.title}
                      </h3>
                      <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                        {card.desc}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          /* Multi-Turn Chat Stream */
          <div className="space-y-6 pb-28">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-3 sm:gap-4 animate-in fade-in duration-300 ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-slate-950 flex-shrink-0 shadow-md shadow-amber-400/20 mt-1">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div
                  className={`relative max-w-3xl rounded-2xl p-4 sm:p-6 shadow-xl ${
                    msg.role === "user"
                      ? "bg-gradient-to-r from-amber-500/20 to-orange-500/20 border border-amber-400/40 text-white ml-8"
                      : "bg-[#14202b] border border-slate-700/70 text-slate-200 mr-4 w-full"
                  }`}
                >
                  {/* Top Bar for Assistant Message */}
                  {msg.role === "assistant" && (
                    <div className="flex items-center justify-between border-b border-slate-700/60 pb-2.5 mb-3.5">
                      <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>Sharda AI Response</span>
                      </div>
                      <span className="text-[11px] text-slate-500">{msg.timestamp}</span>
                    </div>
                  )}

                  {/* Rendered Content */}
                  {msg.role === "user" ? (
                    <p className="text-sm font-medium leading-relaxed whitespace-pre-wrap">
                      {msg.content}
                    </p>
                  ) : (
                    <div>
                      <TurboMarkdownView content={msg.content} />

                      {/* Action Tools Footer */}
                      <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between flex-wrap gap-2 text-xs text-slate-400">
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => handleCopy(msg.id, msg.content)}
                            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800/60 hover:bg-slate-800 hover:text-white border border-slate-700/50 transition-colors"
                          >
                            {copiedId === msg.id ? (
                              <>
                                <Check className="w-3 h-3 text-emerald-400" />
                                <span className="text-emerald-400 font-semibold">Copied</span>
                              </>
                            ) : (
                              <>
                                <Copy className="w-3 h-3" />
                                <span>Copy</span>
                              </>
                            )}
                          </button>
                        </div>

                        {msg.sources && msg.sources.length > 0 && (
                          <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
                            <BookOpen className="w-3 h-3 text-amber-400" />
                            <span>Sources: {msg.sources.slice(0, 2).join(", ")}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 flex-shrink-0 mt-1">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex gap-3 sm:gap-4 justify-start animate-in fade-in">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-slate-950 flex-shrink-0 shadow-md shadow-amber-400/20">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="bg-[#14202b] border border-amber-400/30 rounded-2xl p-4 sm:p-5 flex items-center gap-3 shadow-xl">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-amber-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="w-2 h-2 rounded-full bg-amber-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="w-2 h-2 rounded-full bg-amber-400 animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                  <span className="text-xs text-amber-300 font-semibold">
                    Consulting Sharda Knowledge Base & Gemini 3.6 Flash...
                  </span>
                </div>
              </div>
            )}

            <div ref={chatBottomRef} />
          </div>
        )}
      </main>

      {/* Floating Bottom Prompt Bar */}
      <footer className="sticky bottom-0 z-30 bg-gradient-to-t from-[#0d141b] via-[#0d141b]/95 to-transparent pt-4 pb-4 px-4 sm:px-6">
        <div className="max-w-3xl mx-auto">
          {/* Quick Follow-up Chips when conversation active */}
          {messages.length > 0 && (
            <div className="flex items-center gap-2 overflow-x-auto pb-2.5 scrollbar-none">
              {followUpSuggestions.map((suggestion, sIdx) => (
                <button
                  key={sIdx}
                  onClick={() => handleSend(suggestion)}
                  disabled={isLoading}
                  className="whitespace-nowrap bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 hover:border-amber-400/50 text-slate-300 hover:text-white px-3 py-1 rounded-full text-xs font-medium transition-all shadow-sm flex items-center gap-1"
                >
                  <span>{suggestion}</span>
                  <ArrowRight className="w-2.5 h-2.5 opacity-60" />
                </button>
              ))}
            </div>
          )}

          {/* Main Input Box */}
          <div className="relative flex items-center bg-[#14202b] border border-slate-700/80 focus-within:border-amber-400 focus-within:ring-2 focus-within:ring-amber-400/20 rounded-2xl p-2 sm:p-2.5 shadow-2xl transition-all">
            <div className="pl-2 pr-1 text-amber-400">
              <Sparkles className="w-4 h-4" />
            </div>

            <input
              ref={inputRef}
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask anything (e.g. When do B.Tech CSE admissions close? What are the scholarship slabs?)..."
              className="flex-1 bg-transparent text-white placeholder-slate-400 text-xs sm:text-sm px-2 focus:outline-none"
              disabled={isLoading}
            />

            <button
              onClick={() => handleSend()}
              disabled={isLoading || !inputQuery.trim()}
              className="bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-400 hover:to-orange-400 disabled:opacity-40 text-slate-950 font-bold px-4 sm:px-5 py-2 rounded-xl text-xs flex items-center gap-1.5 transition-all shadow-md shadow-amber-400/20"
            >
              <span>{isLoading ? "Generating..." : "Ask"}</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="text-center mt-2">
            <p className="text-[11px] text-slate-500 font-medium">
              Powered by <span className="text-slate-400 font-semibold">⚡ Turbo Bytes Consulting (TBC)</span> &amp; Google Gemini 3.6 Flash
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
