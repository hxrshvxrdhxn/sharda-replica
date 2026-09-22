"use client";

import React, { useState } from "react";
import Image from "next/image";
import {
  Menu,
  X,
  ChevronDown,
  Sparkles,
  Search,
  ArrowRight,
  GraduationCap,
  Building2,
  Trophy,
  HelpCircle
} from "lucide-react";

interface NavbarProps {
  onOpenLeadModal: (course?: string) => void;
  onOpenAIChat: (prompt?: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenLeadModal, onOpenAIChat }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

  const schools = [
    { name: "Engineering & Technology (SET)", slug: "engineering-and-technology" },
    { name: "Business Studies (SBS)", slug: "business-studies" },
    { name: "Medical Sciences & Research (SMS&R)", slug: "medical-sciences-and-research" },
    { name: "Dental Sciences (SDS)", slug: "dental-sciences" },
    { name: "Law & Legal Studies (SOL)", slug: "law" },
    { name: "Design & Architecture (SAP)", slug: "design" },
    { name: "Pharmacy (SOP)", slug: "pharmacy" },
    { name: "Allied Health Sciences (SAHS)", slug: "allied-health-sciences" },
    { name: "Humanities & Social Sciences (SHSS)", slug: "humanities-and-social-sciences" },
    { name: "Agricultural Sciences (SOAG)", slug: "agricultural-sciences" }
  ];

  return (
    <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Brand Logo */}
          <a href="#" className="flex items-center space-x-3 group">
            <div className="relative h-12 w-48 sm:w-56">
              <Image
                src="/assets/logo.png"
                alt="Sharda University Logo"
                fill
                priority
                className="object-contain"
                sizes="(max-width: 768px) 190px, 220px"
              />
            </div>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-7 text-sm font-medium text-gray-700">
            {/* About */}
            <div
              className="relative group py-6 cursor-pointer"
              onMouseEnter={() => setActiveDropdown("about")}
              onMouseLeave={() => setActiveDropdown(null)}
            >
              <button className="flex items-center space-x-1 hover:text-[#A61C24] transition-colors">
                <span>About Sharda</span>
                <ChevronDown className="w-3.5 h-3.5" />
              </button>

              {activeDropdown === "about" && (
                <div className="absolute top-full left-0 w-64 bg-white rounded-lg shadow-xl border border-gray-100 py-3 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                  <a href="#about" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Overview & Accreditations (NAAC A+)
                  </a>
                  <a href="#about" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Chancellor & Leadership
                  </a>
                  <a href="#stats" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Campus Infrastructure (63+ Acres)
                  </a>
                  <a href="#why-sharda" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Global University Tie-ups (130+)
                  </a>
                </div>
              )}
            </div>

            {/* Academics / Schools Mega Menu */}
            <div
              className="relative group py-6 cursor-pointer"
              onMouseEnter={() => setActiveDropdown("schools")}
              onMouseLeave={() => setActiveDropdown(null)}
            >
              <button className="flex items-center space-x-1 hover:text-[#A61C24] transition-colors">
                <span>Schools & Academics</span>
                <ChevronDown className="w-3.5 h-3.5" />
              </button>

              {activeDropdown === "schools" && (
                <div className="absolute top-full -left-20 w-[600px] bg-white rounded-xl shadow-2xl border border-gray-100 p-5 z-50 grid grid-cols-2 gap-3 animate-in fade-in slide-in-from-top-2 duration-150">
                  <div className="col-span-2 pb-2 mb-1 border-b border-gray-100 flex items-center justify-between">
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                      14+ Schools of Excellence
                    </span>
                    <a
                      href="#schools"
                      className="text-xs font-semibold text-[#A61C24] hover:underline flex items-center"
                    >
                      View All Schools <ArrowRight className="w-3 h-3 ml-1" />
                    </a>
                  </div>
                  {schools.map((school) => (
                    <a
                      key={school.slug}
                      href={`#schools`}
                      className="p-2 rounded-lg hover:bg-amber-50/50 hover:text-[#1B2C39] text-gray-700 transition flex items-center space-x-2 text-xs font-medium"
                    >
                      <GraduationCap className="w-4 h-4 text-amber-500 shrink-0" />
                      <span className="truncate">{school.name}</span>
                    </a>
                  ))}
                </div>
              )}
            </div>

            {/* Programs */}
            <a href="#programs" className="hover:text-[#A61C24] transition-colors">
              Programmes
            </a>

            {/* Admissions */}
            <div
              className="relative group py-6 cursor-pointer"
              onMouseEnter={() => setActiveDropdown("admissions")}
              onMouseLeave={() => setActiveDropdown(null)}
            >
              <button className="flex items-center space-x-1 hover:text-[#A61C24] transition-colors">
                <span>Admissions 2026</span>
                <ChevronDown className="w-3.5 h-3.5" />
              </button>

              {activeDropdown === "admissions" && (
                <div className="absolute top-full left-0 w-60 bg-white rounded-lg shadow-xl border border-gray-100 py-3 z-50">
                  <a href="#admissions" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Admission Process & Guidelines
                  </a>
                  <a href="#scholarship" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Up to 100% Scholarships
                  </a>
                  <a href="#calculator" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Fee & Scholarship Calculator
                  </a>
                  <a href="#admissions" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    Hostel & Accommodation
                  </a>
                  <a href="#suat" className="block px-4 py-2 hover:bg-gray-50 hover:text-[#A61C24]">
                    SUAT Online Exam Details
                  </a>
                </div>
              )}
            </div>

            {/* Placements */}
            <a href="#placements" className="hover:text-[#A61C24] transition-colors">
              Placements
            </a>

            {/* FAQs */}
            <a href="#faqs" className="hover:text-[#A61C24] transition-colors">
              FAQs
            </a>
          </div>

          {/* Right Action CTAs */}
          <div className="flex items-center space-x-3">
            {/* Ask Sharda AI Trigger Button */}
            <button
              onClick={() => onOpenAIChat()}
              className="hidden sm:flex items-center space-x-2 bg-[#1B2C39] hover:bg-[#23394c] text-amber-300 px-4 py-2.5 rounded-full text-xs font-semibold shadow-md transition transform hover:-translate-y-0.5 border border-amber-400/30"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
              <span>Ask Sharda AI</span>
            </button>

            {/* Apply Now Gold Button */}
            <button
              onClick={() => onOpenLeadModal()}
              className="bg-[#EAA914] hover:bg-[#D6950B] text-[#1B2C39] font-bold text-xs uppercase tracking-wider px-5 py-2.5 rounded-lg shadow-md transition transform hover:-translate-y-0.5"
            >
              Apply Now 2026
            </button>

            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 text-gray-600 hover:text-gray-900 focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-white border-t border-gray-100 px-4 pt-3 pb-6 space-y-3">
          <a
            href="#about"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-gray-800 font-medium border-b border-gray-100"
          >
            About Sharda (NAAC A+)
          </a>
          <a
            href="#schools"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-gray-800 font-medium border-b border-gray-100"
          >
            Schools & Academics
          </a>
          <a
            href="#programs"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-gray-800 font-medium border-b border-gray-100"
          >
            All Programmes & Fees
          </a>
          <a
            href="#scholarship"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-gray-800 font-medium border-b border-gray-100"
          >
            Scholarship Slabs
          </a>
          <a
            href="#placements"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-gray-800 font-medium border-b border-gray-100"
          >
            Placements Record
          </a>
          <div className="pt-2 flex flex-col space-y-2">
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenAIChat();
              }}
              className="w-full flex items-center justify-center space-x-2 bg-[#1B2C39] text-amber-300 py-2.5 rounded-lg text-xs font-semibold"
            >
              <Sparkles className="w-4 h-4" />
              <span>Ask Sharda AI Assistant</span>
            </button>
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenLeadModal();
              }}
              className="w-full bg-[#EAA914] text-[#1B2C39] font-bold py-2.5 rounded-lg text-xs uppercase"
            >
              Apply Online 2026
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};
