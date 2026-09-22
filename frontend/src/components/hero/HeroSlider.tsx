"use client";

import React from "react";
import Image from "next/image";
import { ArrowRight, Sparkles, Award, Users, Globe, CheckCircle2 } from "lucide-react";

interface HeroSliderProps {
  onOpenLeadModal: () => void;
  onOpenAIChat: (query?: string) => void;
}

export const HeroSlider: React.FC<HeroSliderProps> = ({ onOpenLeadModal, onOpenAIChat }) => {
  return (
    <div className="relative bg-[#1B2C39] text-white overflow-hidden min-h-[580px] lg:min-h-[640px] flex items-center">
      {/* Background Hero Image with Gradient Overlay */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/assets/campus_banner.jpg"
          alt="Sharda University Campus"
          fill
          priority
          className="object-cover object-center opacity-30 scale-105 transition-transform duration-10000"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-[#1B2C39] via-[#1B2C39]/85 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#1B2C39] via-transparent to-transparent" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Hero Content */}
          <div className="lg:col-span-8 space-y-6">
            {/* Accreditation Badge */}
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-md border border-amber-400/40 px-3.5 py-1.5 rounded-full text-xs text-amber-300 font-semibold tracking-wide">
              <Award className="w-4 h-4 text-amber-400" />
              <span>NAAC A+ ACCREDITED UNIVERSITY | NIRF RANKED</span>
            </div>

            {/* Main Headline */}
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              The World is at Sharda. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500">
                Where are You?
              </span>
            </h1>

            {/* Subheading */}
            <p className="text-gray-300 text-base sm:text-lg max-w-2xl leading-relaxed">
              Experience truly global education across 14+ futuristic schools with over 130+ international university tie-ups, industry-integrated labs, and proven 95%+ placements with packages up to ₹1 Crore.
            </p>

            {/* Bullet Points */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm text-gray-200 pt-2">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Up to 100% Merit Scholarships</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-amber-400 shrink-0" />
                <span>600+ Top MNC Recruiters</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-amber-400 shrink-0" />
                <span>SUAT 2026 Admissions Now Open</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-amber-400 shrink-0" />
                <span>63+ Acres Smart Wi-Fi Campus</span>
              </div>
            </div>

            {/* Hero CTAs */}
            <div className="pt-4 flex flex-wrap gap-4 items-center">
              <button
                onClick={onOpenLeadModal}
                className="bg-[#EAA914] hover:bg-[#D6950B] text-[#1B2C39] font-bold px-7 py-3.5 rounded-xl shadow-lg transition-all transform hover:-translate-y-0.5 flex items-center space-x-2 text-sm uppercase tracking-wider"
              >
                <span>Apply for Admissions 2026</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={() => onOpenAIChat("List all engineering and management programmes with fee and eligibility")}
                className="bg-white/10 hover:bg-white/20 backdrop-blur-md text-white border border-white/20 hover:border-amber-400 px-6 py-3.5 rounded-xl transition-all text-sm font-semibold flex items-center space-x-2"
              >
                <Sparkles className="w-4 h-4 text-amber-400 animate-pulse" />
                <span>Ask Sharda AI Assistant</span>
              </button>
            </div>
          </div>

          {/* Right Quick Inquiry Form Card */}
          <div className="lg:col-span-4 hidden lg:block">
            <div className="bg-white/95 backdrop-blur-xl p-6 rounded-2xl shadow-2xl border border-white/20 text-gray-900">
              <div className="border-b border-gray-100 pb-3 mb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-[#A61C24]">Admissions 2026</span>
                <h3 className="text-lg font-bold text-[#1B2C39]">Request University Prospectus</h3>
                <p className="text-xs text-gray-500">Get instant fee details & counselor call</p>
              </div>

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  onOpenLeadModal();
                }}
                className="space-y-3"
              >
                <div>
                  <input
                    type="text"
                    required
                    placeholder="Candidate's Full Name *"
                    className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#EAA914] focus:border-transparent"
                  />
                </div>
                <div>
                  <input
                    type="tel"
                    required
                    placeholder="Mobile Number (with WhatsApp) *"
                    className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#EAA914] focus:border-transparent"
                  />
                </div>
                <div>
                  <input
                    type="email"
                    required
                    placeholder="Email Address *"
                    className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#EAA914] focus:border-transparent"
                  />
                </div>
                <div>
                  <select className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#EAA914] focus:border-transparent text-gray-700">
                    <option value="">Select Interested Discipline</option>
                    <option value="btech">Engineering & Tech (B.Tech / BCA)</option>
                    <option value="mba">Management (MBA / BBA)</option>
                    <option value="medical">Medical & Allied Health (MBBS / BPT)</option>
                    <option value="law">Law (B.A. LL.B / LL.M)</option>
                    <option value="design">Design & Architecture (B.Des / B.Arch)</option>
                    <option value="pharmacy">Pharmacy (B.Pharm)</option>
                  </select>
                </div>
                <div className="text-[10px] text-gray-500 flex items-start space-x-1.5 pt-1">
                  <input type="checkbox" defaultChecked required className="mt-0.5" />
                  <span>I agree to receive communications regarding admissions & scholarships per DPDP policy.</span>
                </div>
                <button
                  type="submit"
                  className="w-full bg-[#A61C24] hover:bg-[#8C141B] text-white font-bold py-3 rounded-lg text-xs uppercase tracking-wider transition shadow-md"
                >
                  Submit & Get Prospectus
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
