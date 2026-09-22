"use client";

import React, { useState } from "react";
import { Calculator, Award, ArrowRight, CheckCircle, Sparkles } from "lucide-react";

interface ScholarshipCalculatorProps {
  onOpenLeadModal: (course?: string) => void;
  onOpenAIChat: (query?: string) => void;
}

export const ScholarshipCalculator: React.FC<ScholarshipCalculatorProps> = ({
  onOpenLeadModal,
  onOpenAIChat
}) => {
  const [boardScore, setBoardScore] = useState<number>(88);
  const [stream, setStream] = useState<string>("ug");

  const calculateWaiver = (score: number) => {
    if (score >= 95) return { waiver: 100, label: "100% Tuition Fee Waiver (Full Academic Scholarship)" };
    if (score >= 90) return { waiver: 50, label: "50% Tuition Fee Waiver" };
    if (score >= 85) return { waiver: 40, label: "40% Tuition Fee Waiver" };
    if (score >= 80) return { waiver: 20, label: "20% Tuition Fee Waiver" };
    if (score >= 75) return { waiver: 10, label: "10% Tuition Fee Waiver" };
    return { waiver: 0, label: "Standard Fee (Eligible for Sports & Special Category Scholarships)" };
  };

  const result = calculateWaiver(boardScore);

  return (
    <section id="calculator" className="py-20 bg-gradient-to-br from-[#1B2C39] via-[#23394c] to-[#111827] text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Explanation */}
          <div className="lg:col-span-6 space-y-6">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-400 bg-amber-400/10 border border-amber-400/30 px-3.5 py-1.5 rounded-full inline-flex items-center space-x-1.5">
              <Award className="w-3.5 h-3.5 text-amber-400" />
              <span>Merit & Special Scholarships 2026</span>
            </span>

            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight">
              Calculate Your Scholarship in Seconds. Up to 100% Tuition Waiver.
            </h2>

            <p className="text-gray-300 text-sm leading-relaxed">
              Sharda University rewards academic excellence. Enter your 10+2 or Graduation percentage to instantly calculate your eligible tuition waiver. Over ₹25+ Crores worth of scholarships awarded annually.
            </p>

            <div className="space-y-3 pt-2">
              <div className="flex items-center space-x-3 text-xs text-gray-200">
                <CheckCircle className="w-4 h-4 text-amber-400 shrink-0" />
                <span>95%+ in 10+2 = 100% Free Tuition for the 1st Year</span>
              </div>
              <div className="flex items-center space-x-3 text-xs text-gray-200">
                <CheckCircle className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Sports Quota & National Champions: 80% to 100% Waiver</span>
              </div>
              <div className="flex items-center space-x-3 text-xs text-gray-200">
                <CheckCircle className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Defense Personnel Wards: 5% Direct Fee Concession</span>
              </div>
              <div className="flex items-center space-x-3 text-xs text-gray-200">
                <CheckCircle className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Sibling Benefit: 5% Waiver for Second Sibling</span>
              </div>
            </div>
          </div>

          {/* Right Interactive Calculator Widget */}
          <div className="lg:col-span-6">
            <div className="bg-white text-gray-900 rounded-2xl p-7 shadow-2xl border border-white/20">
              <div className="flex items-center space-x-3 pb-4 border-b border-gray-100">
                <div className="p-2.5 bg-amber-50 rounded-xl text-amber-600">
                  <Calculator className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-[#1B2C39]">Instant Scholarship Estimator</h3>
                  <p className="text-xs text-gray-500">Calculate academic merit eligibility</p>
                </div>
              </div>

              <div className="py-6 space-y-6">
                {/* Level selection */}
                <div>
                  <label className="text-xs font-bold text-gray-700 block mb-2">Program Level</label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      onClick={() => setStream("ug")}
                      className={`text-xs font-semibold py-2.5 rounded-lg border transition ${
                        stream === "ug"
                          ? "bg-[#1B2C39] text-white border-[#1B2C39]"
                          : "border-gray-200 text-gray-700 hover:bg-gray-50"
                      }`}
                    >
                      Undergraduate (10+2 Score)
                    </button>
                    <button
                      onClick={() => setStream("pg")}
                      className={`text-xs font-semibold py-2.5 rounded-lg border transition ${
                        stream === "pg"
                          ? "bg-[#1B2C39] text-white border-[#1B2C39]"
                          : "border-gray-200 text-gray-700 hover:bg-gray-50"
                      }`}
                    >
                      Postgraduate (Grad / CAT Score)
                    </button>
                  </div>
                </div>

                {/* Score Slider */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-xs font-bold text-gray-700">
                      Your Aggregate Marks / Percentile
                    </label>
                    <span className="text-base font-extrabold text-[#A61C24] bg-red-50 px-3 py-0.5 rounded-lg border border-red-100">
                      {boardScore}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="100"
                    step="1"
                    value={boardScore}
                    onChange={(e) => setBoardScore(Number(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#EAA914]"
                  />
                  <div className="flex justify-between text-[10px] text-gray-400 mt-1">
                    <span>50%</span>
                    <span>75%</span>
                    <span>85%</span>
                    <span>90%</span>
                    <span>100%</span>
                  </div>
                </div>

                {/* Calculation Result Card */}
                <div className="p-4 bg-amber-50/80 rounded-xl border border-amber-200/80 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-amber-800">
                      Eligible Waiver
                    </span>
                    <h4 className="text-xl font-extrabold text-[#1B2C39]">{result.label}</h4>
                  </div>
                  <div className="text-right">
                    <span className="text-3xl font-black text-[#A61C24]">{result.waiver}%</span>
                    <span className="block text-[10px] text-gray-500">Fee Off</span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                <button
                  onClick={() => onOpenLeadModal("Scholarship Claim")}
                  className="flex-1 bg-[#EAA914] hover:bg-[#D6950B] text-[#1B2C39] font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition shadow-md flex items-center justify-center space-x-1.5"
                >
                  <span>Claim Scholarship Seat</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
                <button
                  onClick={() =>
                    onOpenAIChat(
                      `I scored ${boardScore}% in 10+2. What scholarships, fee waivers, and course admission options are open for me at Sharda?`
                    )
                  }
                  className="bg-[#1B2C39] hover:bg-[#23394c] text-white p-3 rounded-xl transition"
                  title="Ask Sharda AI details"
                >
                  <Sparkles className="w-4 h-4 text-amber-400" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
