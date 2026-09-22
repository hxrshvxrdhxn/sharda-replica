"use client";

import React, { useState } from "react";
import { Search, Sparkles, CheckCircle, ArrowRight, BookOpen, Clock, IndianRupee } from "lucide-react";

interface ProgramsCatalogProps {
  onOpenLeadModal: (courseName: string) => void;
  onOpenAIChat: (query: string) => void;
}

export const ProgramsCatalog: React.FC<ProgramsCatalogProps> = ({ onOpenLeadModal, onOpenAIChat }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [degreeFilter, setDegreeFilter] = useState("all");

  const programs = [
    {
      id: "btech-cse",
      name: "B.Tech in Computer Science & Engineering",
      school: "School of Engineering & Technology",
      school_id: "set",
      degree: "UG",
      duration: "4 Years (8 Semesters)",
      annual_fee: "₹2,20,000",
      semester_fee: "₹1,10,000",
      eligibility: "10+2 with PCM/CS min 60% aggregate. Valid SUAT / JEE Main rank.",
      specializations: ["AI & ML", "Cyber Security", "Cloud Computing", "Data Science", "Full Stack"],
      top_recruiters: "Microsoft, Amazon, TCS, Cognizant, Wipro"
    },
    {
      id: "btech-cse-aiml",
      name: "B.Tech in CSE (Artificial Intelligence & ML)",
      school: "School of Engineering & Technology",
      school_id: "set",
      degree: "UG",
      duration: "4 Years (8 Semesters)",
      annual_fee: "₹2,35,000",
      semester_fee: "₹1,17,500",
      eligibility: "10+2 with PCM min 60% aggregate. SUAT / JEE Main qualified.",
      specializations: ["Generative AI", "Deep Learning", "NLP", "Robotics", "Computer Vision"],
      top_recruiters: "Google, NVIDIA, AWS, Microsoft, Intel"
    },
    {
      id: "mba-dual",
      name: "Master of Business Administration (MBA Dual Specialization)",
      school: "School of Business Studies",
      school_id: "sbs",
      degree: "PG",
      duration: "2 Years (4 Semesters)",
      annual_fee: "₹3,85,000",
      semester_fee: "₹1,92,500",
      eligibility: "Bachelor's Degree with min 50% marks + SUAT / CAT / MAT / XAT + GD & PI.",
      specializations: ["Marketing", "Finance", "HR", "Business Analytics", "International Business"],
      top_recruiters: "Deloitte, KPMG, EY, PwC, HDFC Bank, Flipkart"
    },
    {
      id: "bba-hons",
      name: "Bachelor of Business Administration (BBA - Hons / Research)",
      school: "School of Business Studies",
      school_id: "sbs",
      degree: "UG",
      duration: "3 / 4 Years (NEP Aligned)",
      annual_fee: "₹1,85,000",
      semester_fee: "₹92,500",
      eligibility: "10+2 in any stream (Commerce/Science/Arts) with min 50% marks + SUAT/CUET.",
      specializations: ["Finance", "Marketing & E-Com", "Human Resources", "Entrepreneurship"],
      top_recruiters: "Genpact, Tech Mahindra, Axis Bank, Wipro"
    },
    {
      id: "mbbs",
      name: "Bachelor of Medicine & Bachelor of Surgery (MBBS)",
      school: "School of Medical Sciences & Research",
      school_id: "smsr",
      degree: "UG",
      duration: "4.5 Years + 1 Year Internship",
      annual_fee: "₹12,69,000",
      semester_fee: "₹6,34,500",
      eligibility: "10+2 with PCB min 50% marks. Must qualify NEET-UG and UP DGME counseling.",
      specializations: ["Clinical Medicine", "General Surgery", "Pediatrics", "Radiology"],
      top_recruiters: "Sharda Hospital, Max, Fortis, Apollo, Medanta"
    },
    {
      id: "b-des",
      name: "Bachelor of Design (B.Des)",
      school: "School of Design, Architecture & Planning",
      school_id: "sod",
      degree: "UG",
      duration: "4 Years (8 Semesters)",
      annual_fee: "₹2,10,000",
      semester_fee: "₹1,05,000",
      eligibility: "10+2 in any stream min 50% marks + SUAT / UCEED / NID / NIFT score + Portfolio.",
      specializations: ["UI/UX Interaction Design", "Interior & Space", "Fashion Design", "Graphics"],
      top_recruiters: "TCS Interactive, Cognizant Design, Infosys, ZARA"
    },
    {
      id: "ba-llb-hons",
      name: "B.A. LL.B. (Integrated Honours 5-Year)",
      school: "School of Law",
      school_id: "sol",
      degree: "UG",
      duration: "5 Years (10 Semesters)",
      annual_fee: "₹1,75,000",
      semester_fee: "₹87,500",
      eligibility: "10+2 in any stream min 50% marks + SUAT / CLAT / LSAT-India.",
      specializations: ["Corporate Law", "Criminal Law", "Constitutional Law", "IPR"],
      top_recruiters: "Shardul Amarchand, Khaitan & Co, Trilegal, Courts"
    },
    {
      id: "b-pharm",
      name: "Bachelor of Pharmacy (B.Pharm)",
      school: "School of Pharmacy",
      school_id: "sop",
      degree: "UG",
      duration: "4 Years (8 Semesters)",
      annual_fee: "₹1,95,000",
      semester_fee: "₹97,500",
      eligibility: "10+2 with PCB/PCM min 50% marks + SUAT / CUET qualified.",
      specializations: ["Pharmaceutics", "Pharmacology", "Drug Discovery", "Clinical Analysis"],
      top_recruiters: "Sun Pharma, Cipla, Dr. Reddy's, Lupin, Mankind"
    }
  ];

  const filtered = programs.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.school.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.specializations.some((s) => s.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesDegree =
      degreeFilter === "all" ? true : p.degree.toLowerCase() === degreeFilter.toLowerCase();

    return matchesSearch && matchesDegree;
  });

  return (
    <section id="programs" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#A61C24] bg-red-50 px-3 py-1 rounded-full">
              Futuristic Curriculums
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#1B2C39] mt-2">
              Explore 130+ Recognized Programmes
            </h2>
            <p className="text-gray-500 text-sm mt-1">
              Find the perfect degree aligned with your career ambition and industry demand.
            </p>
          </div>

          {/* Search & Filter Controls */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative w-full sm:w-64">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by course, tech, field..."
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#EAA914]"
              />
            </div>

            <div className="flex bg-gray-100 p-1 rounded-xl">
              {["all", "ug", "pg"].map((d) => (
                <button
                  key={d}
                  onClick={() => setDegreeFilter(d)}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg capitalize transition ${
                    degreeFilter === d ? "bg-white text-[#1B2C39] shadow-sm" : "text-gray-500 hover:text-gray-900"
                  }`}
                >
                  {d === "all" ? "All Levels" : d.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Programs Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((prog) => (
            <div
              key={prog.id}
              className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group hover:border-amber-300"
            >
              <div>
                {/* School & Degree Badge */}
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[10px] font-bold text-sky-700 bg-sky-50 px-2.5 py-1 rounded-full uppercase tracking-wider">
                    {prog.school}
                  </span>
                  <span className="text-[10px] font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded">
                    {prog.degree}
                  </span>
                </div>

                {/* Course Name */}
                <h3 className="text-base font-bold text-[#1B2C39] group-hover:text-[#A61C24] transition-colors leading-snug">
                  {prog.name}
                </h3>

                {/* Meta details */}
                <div className="grid grid-cols-2 gap-2 my-4 p-3 bg-gray-50 rounded-xl text-xs">
                  <div>
                    <span className="text-gray-400 block text-[10px] flex items-center">
                      <Clock className="w-3 h-3 mr-1 text-gray-400" /> Duration
                    </span>
                    <span className="font-semibold text-gray-800">{prog.duration}</span>
                  </div>
                  <div>
                    <span className="text-gray-400 block text-[10px] flex items-center">
                      <IndianRupee className="w-3 h-3 mr-1 text-gray-400" /> Annual Tuition
                    </span>
                    <span className="font-bold text-[#A61C24]">{prog.annual_fee}</span>
                  </div>
                </div>

                {/* Eligibility */}
                <div className="mb-3">
                  <span className="text-[11px] font-semibold text-gray-700 block mb-1">Eligibility:</span>
                  <p className="text-xs text-gray-500 line-clamp-2 leading-relaxed">{prog.eligibility}</p>
                </div>

                {/* Specializations Tags */}
                <div>
                  <span className="text-[11px] font-semibold text-gray-700 block mb-1.5">Specializations:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {prog.specializations.map((spec, i) => (
                      <span
                        key={i}
                        className="text-[10px] font-medium bg-gray-100 text-gray-700 px-2 py-0.5 rounded-md"
                      >
                        {spec}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 pt-4 border-t border-gray-100 flex items-center justify-between">
                <button
                  onClick={() => onOpenLeadModal(prog.name)}
                  className="bg-[#1B2C39] hover:bg-[#23394c] text-white font-bold text-xs px-4 py-2.5 rounded-lg transition flex items-center space-x-1"
                >
                  <span>Apply Now</span>
                  <ArrowRight className="w-3 h-3" />
                </button>

                <button
                  onClick={() =>
                    onOpenAIChat(
                      `Provide full breakdown for ${prog.name}: eligibility, exact syllabus highlights, career outcomes, scholarships, and placement stats.`
                    )
                  }
                  className="text-xs font-semibold text-amber-600 hover:text-amber-700 bg-amber-50 hover:bg-amber-100 px-3 py-2 rounded-lg flex items-center space-x-1.5 transition"
                >
                  <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                  <span>Ask AI Details</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
