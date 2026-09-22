"use client";

import React, { useState } from "react";
import {
  Code,
  Briefcase,
  Stethoscope,
  Scale,
  Palette,
  Pill,
  HeartPulse,
  BookOpen,
  Wheat,
  ArrowRight,
  Sparkles
} from "lucide-react";

interface SchoolsGridProps {
  onSelectSchool: (schoolSlug: string) => void;
  onOpenAIChat: (query: string) => void;
}

export const SchoolsGrid: React.FC<SchoolsGridProps> = ({ onSelectSchool, onOpenAIChat }) => {
  const [activeCategory, setActiveCategory] = useState("all");

  const schools = [
    {
      id: "set",
      name: "School of Engineering and Technology (SET)",
      slug: "engineering-and-technology",
      category: "tech",
      icon: <Code className="w-6 h-6 text-sky-500" />,
      tagline: "AI/ML, Cloud Computing, Cyber Security, Robotics",
      degrees: "B.Tech, M.Tech, BCA, MCA, Ph.D",
      accreditation: "NBA & NAAC A+ Accredited",
      popular: "B.Tech CSE (AI & ML), Cyber Security"
    },
    {
      id: "sbs",
      name: "School of Business Studies (SBS)",
      slug: "business-studies",
      category: "management",
      icon: <Briefcase className="w-6 h-6 text-amber-500" />,
      tagline: "Strategic Management, FinTech & Business Analytics",
      degrees: "MBA, BBA, B.Com (Hons), Ph.D",
      accreditation: "IACBE Member, NAAC A+",
      popular: "MBA Dual Specialization, BBA (Hons)"
    },
    {
      id: "smsr",
      name: "School of Medical Sciences & Research (SMS&R)",
      slug: "medical-sciences-and-research",
      category: "medical",
      icon: <Stethoscope className="w-6 h-6 text-emerald-500" />,
      tagline: "1200+ Bed Sharda Hospital Clinical Training",
      degrees: "MBBS, MD, MS, M.Sc Medical",
      accreditation: "NMC Approved",
      popular: "MBBS, MD General Medicine"
    },
    {
      id: "sds",
      name: "School of Dental Sciences (SDS)",
      slug: "dental-sciences",
      category: "medical",
      icon: <HeartPulse className="w-6 h-6 text-rose-500" />,
      tagline: "Advanced Maxillofacial Surgery & CAD/CAM Dental Labs",
      degrees: "BDS, MDS, Ph.D",
      accreditation: "DCI Approved",
      popular: "BDS, MDS Orthodontics"
    },
    {
      id: "sol",
      name: "School of Law (SOL)",
      slug: "law",
      category: "law",
      icon: <Scale className="w-6 h-6 text-indigo-500" />,
      tagline: "Moot Courts, Supreme Court & High Court Internships",
      degrees: "B.A. LL.B., B.B.A. LL.B., LL.M., Ph.D",
      accreditation: "Bar Council of India (BCI) Approved",
      popular: "B.A. LL.B. (5-Yr Integrated), LL.M"
    },
    {
      id: "sod",
      name: "School of Design, Architecture & Planning (SAP)",
      slug: "design",
      category: "design",
      icon: <Palette className="w-6 h-6 text-purple-500" />,
      tagline: "UI/UX, Interior Design, Fashion & Sustainable Architecture",
      degrees: "B.Arch, B.Des, M.Des, M.Arch",
      accreditation: "COA Approved",
      popular: "B.Des (UI/UX), B.Arch"
    },
    {
      id: "sop",
      name: "School of Pharmacy (SOP)",
      slug: "pharmacy",
      category: "medical",
      icon: <Pill className="w-6 h-6 text-teal-500" />,
      tagline: "Drug Discovery, Clinical Formulation & Regulatory Affairs",
      degrees: "B.Pharm, D.Pharm, M.Pharm, Ph.D",
      accreditation: "PCI Approved",
      popular: "B.Pharm, M.Pharm Pharmaceutics"
    },
    {
      id: "sahs",
      name: "School of Allied Health Sciences (SAHS)",
      slug: "allied-health-sciences",
      category: "medical",
      icon: <HeartPulse className="w-6 h-6 text-cyan-500" />,
      tagline: "Physiotherapy, Radiology, Optometry & Lab Technology",
      degrees: "BPT, BMLT, B.Sc Radiology, MPT",
      accreditation: "UP State Medical Faculty",
      popular: "BPT (Physiotherapy), B.Sc Radiology"
    },
    {
      id: "shss",
      name: "School of Humanities and Social Sciences (SHSS)",
      slug: "humanities-and-social-sciences",
      category: "humanities",
      icon: <BookOpen className="w-6 h-6 text-orange-500" />,
      tagline: "Applied Psychology, Economics, Political Science & Civil Prep",
      degrees: "B.A. (Hons), M.A., Ph.D",
      accreditation: "UGC Approved",
      popular: "B.A. Applied Psychology, B.A. Economics"
    },
    {
      id: "soag",
      name: "School of Agricultural Sciences (SOAG)",
      slug: "agricultural-sciences",
      category: "tech",
      icon: <Wheat className="w-6 h-6 text-green-600" />,
      tagline: "Precision Agriculture, Smart Polyhouses & Agribusiness",
      degrees: "B.Sc (Hons) Agriculture, M.Sc, Ph.D",
      accreditation: "ICAR Aligned Curriculum",
      popular: "B.Sc (Hons) Agriculture"
    }
  ];

  const filteredSchools =
    activeCategory === "all"
      ? schools
      : schools.filter((s) => s.category === activeCategory);

  return (
    <section id="schools" className="py-20 bg-gray-50/70">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-[#A61C24] bg-red-50 px-3 py-1 rounded-full">
            Academics of Excellence
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#1B2C39] mt-3 tracking-tight">
            14+ Schools Driving Future-Ready Education
          </h2>
          <p className="text-gray-600 text-sm sm:text-base mt-2">
            Interdisciplinary learning backed by world-class infrastructure, industry-certified faculty, and global curriculums.
          </p>

          {/* Filter Pills */}
          <div className="flex flex-wrap justify-center gap-2 mt-6">
            {[
              { id: "all", label: "All Schools" },
              { id: "tech", label: "Engineering & Tech" },
              { id: "management", label: "Management & Commerce" },
              { id: "medical", label: "Medical & Health" },
              { id: "law", label: "Law & Justice" },
              { id: "design", label: "Design & Architecture" },
              { id: "humanities", label: "Humanities & Social" }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveCategory(tab.id)}
                className={`text-xs font-semibold px-4 py-2 rounded-full transition ${
                  activeCategory === tab.id
                    ? "bg-[#1B2C39] text-amber-300 shadow-sm"
                    : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Schools Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSchools.map((school) => (
            <div
              key={school.id}
              className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all duration-300 border border-gray-100 flex flex-col justify-between group hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 bg-gray-50 rounded-xl group-hover:bg-amber-50 transition">
                    {school.icon}
                  </div>
                  <span className="text-[10px] font-bold text-gray-500 bg-gray-100 px-2.5 py-1 rounded-md">
                    {school.accreditation}
                  </span>
                </div>

                <h3 className="text-lg font-bold text-[#1B2C39] group-hover:text-[#A61C24] transition-colors leading-snug">
                  {school.name}
                </h3>

                <p className="text-xs text-gray-500 mt-2 line-clamp-2">
                  {school.tagline}
                </p>

                <div className="mt-4 pt-3 border-t border-gray-100 space-y-1.5 text-xs text-gray-700">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 font-medium">Degrees:</span>
                    <span className="font-semibold text-[#1B2C39]">{school.degrees}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 font-medium">Popular:</span>
                    <span className="font-semibold text-[#A61C24] truncate max-w-[180px]">{school.popular}</span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 pt-3 border-t border-gray-100 flex items-center justify-between">
                <a
                  href="#programs"
                  onClick={() => onSelectSchool(school.slug)}
                  className="text-xs font-bold text-[#1B2C39] hover:text-[#A61C24] flex items-center group-hover:translate-x-1 transition"
                >
                  <span>Explore Courses</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1" />
                </a>

                <button
                  onClick={() => onOpenAIChat(`Tell me about ${school.name} programs, admission criteria, and fee structure.`)}
                  className="text-[11px] font-semibold text-amber-600 hover:text-amber-700 bg-amber-50 hover:bg-amber-100 px-2.5 py-1 rounded-lg flex items-center space-x-1 transition"
                  title="Ask Sharda AI about this school"
                >
                  <Sparkles className="w-3 h-3 text-amber-500" />
                  <span>Ask AI</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
