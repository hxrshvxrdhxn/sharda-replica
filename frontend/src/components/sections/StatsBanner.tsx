"use client";

import React from "react";
import { Award, Globe2, Briefcase, Trophy, Building, Users } from "lucide-react";

export const StatsBanner: React.FC = () => {
  const stats = [
    {
      value: "NAAC A+",
      label: "Accredited Grade",
      icon: <Award className="w-6 h-6 text-amber-500" />,
      highlight: "Highest Quality Assurance"
    },
    {
      value: "₹1.00 Cr",
      label: "Highest Global Package",
      icon: <Trophy className="w-6 h-6 text-amber-500" />,
      highlight: "International Placements"
    },
    {
      value: "₹45.00 LPA",
      label: "Highest Domestic Package",
      icon: <Briefcase className="w-6 h-6 text-amber-500" />,
      highlight: "600+ MNC Recruiters"
    },
    {
      value: "14+",
      label: "Schools of Excellence",
      icon: <Building className="w-6 h-6 text-amber-500" />,
      highlight: "Multidisciplinary Education"
    },
    {
      value: "130+",
      label: "Global Tie-ups",
      icon: <Globe2 className="w-6 h-6 text-amber-500" />,
      highlight: "USA, UK, Canada & Europe"
    },
    {
      value: "85,000+",
      label: "Global Alumni",
      icon: <Users className="w-6 h-6 text-amber-500" />,
      highlight: "Across 85+ Nations"
    }
  ];

  return (
    <section id="stats" className="relative -mt-8 z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6 sm:p-8 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 divide-y lg:divide-y-0 lg:divide-x divide-gray-100">
        {stats.map((item, idx) => (
          <div key={idx} className={`pt-4 lg:pt-0 ${idx > 0 ? "lg:pl-6" : ""} flex flex-col items-center text-center space-y-1`}>
            <div className="p-2.5 bg-amber-50 rounded-xl mb-1">
              {item.icon}
            </div>
            <span className="text-2xl sm:text-3xl font-extrabold text-[#1B2C39] tracking-tight">
              {item.value}
            </span>
            <span className="text-xs font-semibold text-gray-800">
              {item.label}
            </span>
            <span className="text-[10px] text-gray-400 font-medium">
              {item.highlight}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
};
