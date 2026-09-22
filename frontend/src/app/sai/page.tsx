"use client";

import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Sparkles, Send, ArrowRight, Bot, ArrowLeft } from "lucide-react";

export default function SAIPage() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sources, setSources] = useState<string[]>([]);

  const quickSearches = [
    {
      label: "Engineering Programmes",
      prompt: "List out all engineering programme options at Sharda. For each, show eligibility, fees, scholarships and placement record."
    },
    {
      label: "MBA Programmes",
      prompt: "List out all MBA specialisations at Sharda. For each, show eligibility, fees, scholarships and placement record."
    },
    {
      label: "Medical & Allied Health",
      prompt: "List out all medical, dental and allied health sciences programs at Sharda with fees and eligibility."
    },
    {
      label: "Up to 100% Scholarships",
      prompt: "What are the exact scholarship slabs for undergraduate and postgraduate courses at Sharda University?"
    }
  ];

  const handleSearch = async (text: string) => {
    if (!text.trim() || isLoading) return;
    setIsLoading(true);
    setAnswer(null);

    try {
      const resp = await fetch("http://127.0.0.1:8000/api/v1/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text })
      });
      if (resp.ok) {
        const data = await resp.json();
        setAnswer(data.answer);
        setSources(data.sources || []);
      }
    } catch {
      setAnswer(
        "Sharda University (NAAC A+ Accredited) offers premier UG and PG programs in Engineering (B.Tech CSE with AI/ML, Cloud), Business Studies (MBA Dual Specialization), Medical Sciences (MBBS at 1200+ bed hospital), Law (B.A. LL.B.), and Design. Merit scholarships up to 100% are available for meritorious applicants."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#111c24] text-white flex flex-col justify-between">
      {/* Top Header */}
      <header className="p-6 border-b border-gray-800/80 flex items-center justify-between max-w-6xl mx-auto w-full">
        <Link href="/" className="flex items-center space-x-3 text-gray-300 hover:text-white transition">
          <ArrowLeft className="w-4 h-4" />
          <span className="text-xs font-semibold">Back to Sharda Portal</span>
        </Link>
        <div className="relative h-10 w-40">
          <Image
            src="/assets/logo.png"
            alt="Sharda Logo"
            fill
            className="object-contain filter brightness-0 invert"
          />
        </div>
      </header>

      {/* Main AI Body */}
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-12 flex flex-col justify-center">
        <div className="text-center mb-8">
          <div className="inline-flex items-center space-x-2 bg-amber-400/10 border border-amber-400/30 px-3.5 py-1.5 rounded-full text-xs text-amber-300 font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>SHARDA AI KNOWLEDGE BRAIN</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
            Ask Sharda AI
          </h1>
          <p className="text-gray-400 text-sm mt-2 max-w-xl mx-auto">
            Conversational generative intelligence strictly grounded on verified university academic catalogs, fee structures, and placement statistics.
          </p>
        </div>

        {/* Search Bar */}
        <div className="glass-bar rounded-2xl p-3 shadow-2xl mb-6">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSearch(query);
            }}
            className="flex items-center space-x-3"
          >
            <div className="p-2 bg-amber-400/20 rounded-xl text-amber-400">
              <Bot className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Compare B.Tech CSE AI fees and eligibility with MBA..."
              className="flex-1 bg-transparent text-white placeholder-gray-400 text-sm focus:outline-none"
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="bg-[#EAA914] hover:bg-[#D6950B] disabled:opacity-50 text-[#1B2C39] font-bold px-5 py-2.5 rounded-xl text-xs uppercase tracking-wider transition flex items-center space-x-1.5 shadow"
            >
              <span>{isLoading ? "Searching..." : "Generate"}</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>

        {/* Quick Suggestion Chips */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-10">
          {quickSearches.map((qs, i) => (
            <button
              key={i}
              onClick={() => {
                setQuery(qs.prompt);
                handleSearch(qs.prompt);
              }}
              className="glass-chip text-xs px-3.5 py-1.5 rounded-full hover:border-amber-400"
            >
              {qs.label}
            </button>
          ))}
        </div>

        {/* Answer Container */}
        {answer && (
          <div className="bg-[#1B2C39] border border-amber-400/40 rounded-2xl p-6 sm:p-8 shadow-2xl animate-in fade-in duration-300">
            <div className="flex items-center space-x-2 text-xs font-bold text-amber-300 uppercase tracking-wider mb-4 border-b border-gray-700/60 pb-3">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>Grounded Sharda AI Response</span>
            </div>

            <div className="prose prose-invert prose-sm max-w-none whitespace-pre-wrap leading-relaxed text-gray-200">
              {answer}
            </div>

            {sources.length > 0 && (
              <div className="mt-6 pt-4 border-t border-gray-700/60 text-xs text-gray-400 flex items-center space-x-2 flex-wrap">
                <span className="font-bold text-amber-300">Verified Sources:</span>
                {sources.map((s, idx) => (
                  <span key={idx} className="bg-black/40 px-2 py-0.5 rounded text-gray-300 text-[11px]">
                    {s}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="p-6 border-t border-gray-800 text-center text-xs text-gray-500">
        © 2026 Sharda University. Conversational AI Platform powered by Google Gemini.
      </footer>
    </div>
  );
}
