"use client";

import React, { useState } from "react";
import { Sparkles, Send, ArrowRight } from "lucide-react";

interface BottomAIBarProps {
  onOpenChatWithQuery: (query: string) => void;
  onOpenLeadModal: () => void;
}

export const BottomAIBar: React.FC<BottomAIBarProps> = ({
  onOpenChatWithQuery,
  onOpenLeadModal
}) => {
  const [inputVal, setInputVal] = useState("");

  const quickPrompts = [
    { label: "Engineering Programmes", query: "List out all engineering programme options at Sharda. For each, show eligibility, fees, scholarships and placement record." },
    { label: "MBA Programmes", query: "List out all MBA specialisations at Sharda. For each, show eligibility, fees, scholarships and placement record." },
    { label: "Biology & Medical", query: "List out all biology and medical programme options at Sharda with fees and eligibility." },
    { label: "Up to 100% Scholarships", query: "What are the exact scholarship slabs for undergraduate and postgraduate courses at Sharda?" },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim()) return;
    onOpenChatWithQuery(inputVal);
    setInputVal("");
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 z-30 pointer-events-none pb-4 px-4 flex flex-col items-center">
      {/* Suggestion Chips */}
      <div className="pointer-events-auto flex items-center space-x-2 overflow-x-auto max-w-4xl mb-2.5 px-2 no-scrollbar">
        {quickPrompts.map((chip, idx) => (
          <button
            key={idx}
            onClick={() => onOpenChatWithQuery(chip.query)}
            className="glass-chip text-xs px-3.5 py-1.5 rounded-full font-medium shadow-lg hover:shadow-amber-500/20 whitespace-nowrap transition transform hover:-translate-y-0.5 border border-amber-400/30"
          >
            {chip.label}
          </button>
        ))}
      </div>

      {/* Liquid Glass Input Bar */}
      <div className="pointer-events-auto w-full max-w-3xl glass-bar rounded-2xl p-2 sm:p-2.5 shadow-2xl flex items-center space-x-2 sm:space-x-3">
        {/* Left Rose/AI Mark */}
        <div className="p-2 bg-amber-400/20 border border-amber-400/40 rounded-xl text-amber-400 flex items-center justify-center shrink-0">
          <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-amber-400 animate-pulse" />
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex-1 flex items-center relative">
          <input
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onFocus={() => {
              if (!inputVal) {
                // optional auto open
              }
            }}
            placeholder="Ask Sharda AI anything (e.g. B.Tech vs MBA fee, scholarships, SUAT)..."
            className="w-full bg-transparent text-white placeholder-gray-300 text-xs sm:text-sm px-2 sm:px-3 py-2 focus:outline-none"
          />

          {inputVal && (
            <button
              type="submit"
              className="p-1.5 bg-[#EAA914] hover:bg-[#D6950B] text-[#1B2C39] rounded-lg transition"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          )}
        </form>

        {/* Action Button */}
        <button
          onClick={() => {
            if (inputVal.trim()) {
              onOpenChatWithQuery(inputVal);
              setInputVal("");
            } else {
              onOpenChatWithQuery("What are the key admissions criteria and scholarships for 2026?");
            }
          }}
          className="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-[#1B2C39] font-bold text-xs px-4 py-2.5 rounded-xl shadow-md transition transform hover:scale-105 shrink-0 flex items-center space-x-1"
        >
          <span>Ask AI</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
