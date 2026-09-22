"use client";

import React from "react";
import { Phone, Mail, Award, BookOpen, User, Globe } from "lucide-react";

export const TopBar: React.FC = () => {
  return (
    <div className="bg-[#1B2C39] text-gray-200 text-xs py-2 border-b border-gray-700/60 hidden md:block">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        {/* Left Badges & Contacts */}
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2 text-amber-400 font-semibold">
            <Award className="w-3.5 h-3.5" />
            <span>NAAC A+ Accredited</span>
          </div>
          <div className="hidden lg:flex items-center space-x-2 text-gray-300">
            <Globe className="w-3.5 h-3.5 text-sky-400" />
            <span>Top Ranked Private University in Delhi-NCR</span>
          </div>
          <a
            href="tel:+911204570000"
            className="flex items-center space-x-1.5 hover:text-amber-400 transition-colors"
          >
            <Phone className="w-3 h-3 text-amber-400" />
            <span>+91-120-4570000</span>
          </a>
          <a
            href="mailto:admission@sharda.ac.in"
            className="hidden xl:flex items-center space-x-1.5 hover:text-amber-400 transition-colors"
          >
            <Mail className="w-3 h-3 text-amber-400" />
            <span>admission@sharda.ac.in</span>
          </a>
        </div>

        {/* Right Action Links */}
        <div className="flex items-center space-x-5">
          <a
            href="#suat"
            className="hover:text-amber-400 transition-colors flex items-center space-x-1"
          >
            <BookOpen className="w-3 h-3 text-amber-400" />
            <span>SUAT 2026</span>
          </a>
          <a
            href="#scholarship"
            className="text-amber-400 font-medium hover:underline"
          >
            Scholarship Slabs
          </a>
          <a
            href="#international"
            className="hover:text-amber-400 transition-colors"
          >
            International Admissions
          </a>
          <a
            href="https://sharda.ac.in"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1 bg-sky-900/60 hover:bg-sky-800 text-sky-200 px-2.5 py-0.5 rounded border border-sky-700/50 transition-colors"
          >
            <User className="w-3 h-3" />
            <span>Student ERP</span>
          </a>
        </div>
      </div>
    </div>
  );
};
