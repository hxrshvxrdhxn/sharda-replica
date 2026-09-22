"use client";

import React from "react";
import { Trophy, TrendingUp, Building2, Quote, ArrowRight, CheckCircle2 } from "lucide-react";

interface PlacementHighlightsProps {
  onOpenLeadModal: () => void;
  onOpenAIChat: (query: string) => void;
}

export const PlacementHighlights: React.FC<PlacementHighlightsProps> = ({
  onOpenLeadModal,
  onOpenAIChat
}) => {
  const topRecruiters = [
    { name: "Microsoft", role: "Software & Cloud", color: "bg-blue-50 text-blue-700 border-blue-200" },
    { name: "Amazon", role: "Cloud & E-Commerce", color: "bg-amber-50 text-amber-700 border-amber-200" },
    { name: "Deloitte", role: "Management Consulting", color: "bg-emerald-50 text-emerald-700 border-emerald-200" },
    { name: "KPMG", role: "Audit & Advisory", color: "bg-indigo-50 text-indigo-700 border-indigo-200" },
    { name: "Cognizant", role: "Digital Engineering", color: "bg-cyan-50 text-cyan-700 border-cyan-200" },
    { name: "Wipro", role: "Enterprise IT", color: "bg-purple-50 text-purple-700 border-purple-200" },
    { name: "TCS", role: "Consulting & Tech", color: "bg-rose-50 text-rose-700 border-rose-200" },
    { name: "Sun Pharma", role: "Pharmaceuticals", color: "bg-teal-50 text-teal-700 border-teal-200" },
    { name: "Larsen & Toubro", role: "Core Engineering", color: "bg-yellow-50 text-yellow-800 border-yellow-200" },
    { name: "HDFC Bank", role: "Banking & Finance", color: "bg-sky-50 text-sky-800 border-sky-200" }
  ];

  const testimonials = [
    {
      name: "Aman Sharma",
      course: "B.Tech Computer Science (Batch 2024)",
      company: "Amazon Web Services",
      package: "₹44.00 LPA",
      quote: "The specialized training in Cloud & AI at SET and continuous mock interview drills by the Career Development Centre helped me clear multiple Amazon technical rounds."
    },
    {
      name: "Priya Verma",
      course: "MBA International Business (Batch 2024)",
      company: "Deloitte Consulting",
      package: "₹14.50 LPA",
      quote: "Working on corporate consulting live projects and interacting with senior industry leaders during guest lectures at SBS made all the difference in my placement journey."
    },
    {
      name: "Rohan Deshmukh",
      course: "B.Des User Experience (Batch 2024)",
      company: "TCS Interactive Design Labs",
      package: "₹12.00 LPA",
      quote: "The hands-on UI/UX prototyping labs and personalized portfolio reviews with industry design heads gave me an immense competitive advantage."
    }
  ];

  return (
    <section id="placements" className="py-20 bg-gray-50/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <span className="text-xs font-bold uppercase tracking-wider text-[#A61C24] bg-red-50 px-3.5 py-1.5 rounded-full">
            Industry Leading Placements
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#1B2C39] mt-3">
            Where Ambition Meets Opportunity
          </h2>
          <p className="text-gray-600 text-sm sm:text-base mt-2">
            Over 600+ multinational corporations and Fortune 500 giants recruit from Sharda every academic year.
          </p>
        </div>

        {/* Highlight Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-14">
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-4">
            <div className="p-3.5 bg-amber-50 rounded-xl text-amber-500">
              <Trophy className="w-8 h-8" />
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-[#1B2C39]">₹1.00 Cr</span>
              <p className="text-xs text-gray-500 font-medium">Highest Global Package</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-4">
            <div className="p-3.5 bg-red-50 rounded-xl text-[#A61C24]">
              <TrendingUp className="w-8 h-8" />
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-[#1B2C39]">₹45.00 LPA</span>
              <p className="text-xs text-gray-500 font-medium">Highest Domestic CTC</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-4">
            <div className="p-3.5 bg-sky-50 rounded-xl text-sky-600">
              <Building2 className="w-8 h-8" />
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-[#1B2C39]">600+</span>
              <p className="text-xs text-gray-500 font-medium">Top MNC Recruiters</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-4">
            <div className="p-3.5 bg-emerald-50 rounded-xl text-emerald-600">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-[#1B2C39]">95%+</span>
              <p className="text-xs text-gray-500 font-medium">Overall Placement Rate</p>
            </div>
          </div>
        </div>

        {/* Top Recruiters Pills */}
        <div className="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm mb-14">
          <div className="flex flex-col sm:flex-row justify-between items-center mb-6 pb-4 border-b border-gray-100">
            <h3 className="text-base font-bold text-[#1B2C39]">Our Prominent Hiring Partners</h3>
            <span className="text-xs text-gray-500">150+ Fortune 500 Companies</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
            {topRecruiters.map((rec, i) => (
              <div
                key={i}
                className={`p-3 rounded-xl border flex flex-col items-center text-center justify-center space-y-1 hover:scale-105 transition-transform ${rec.color}`}
              >
                <span className="font-bold text-sm">{rec.name}</span>
                <span className="text-[10px] opacity-80">{rec.role}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Student Testimonials */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((t, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col justify-between"
            >
              <div>
                <Quote className="w-8 h-8 text-amber-400/40 mb-3" />
                <p className="text-xs text-gray-600 italic leading-relaxed mb-6">
                  &quot;{t.quote}&quot;
                </p>
              </div>

              <div className="pt-4 border-t border-gray-100 flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-bold text-[#1B2C39]">{t.name}</h4>
                  <p className="text-[10px] text-gray-500">{t.course}</p>
                  <p className="text-[11px] font-semibold text-sky-700">{t.company}</p>
                </div>
                <span className="text-xs font-extrabold text-[#A61C24] bg-red-50 px-2.5 py-1 rounded-md border border-red-100">
                  {t.package}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
