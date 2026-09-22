"use client";

import React from "react";
import Image from "next/image";
import { Phone, Mail, MapPin, Globe, Award, Shield, HeartHandshake } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#111c24] text-gray-400 text-xs border-t border-gray-800">
      {/* Top Accreditation & Regulatory Approvals Ribbon */}
      <div className="bg-[#1B2C39] py-6 border-b border-gray-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-3 text-white">
            <Award className="w-5 h-5 text-amber-400" />
            <span className="font-bold text-sm">NAAC A+ Accredited University</span>
          </div>

          <div className="flex flex-wrap items-center gap-3 text-[11px] text-gray-300 font-medium">
            <span className="bg-white/10 px-2.5 py-1 rounded">UGC Recognized</span>
            <span className="bg-white/10 px-2.5 py-1 rounded">AICTE Approved</span>
            <span className="bg-white/10 px-2.5 py-1 rounded">NMC (Medical)</span>
            <span className="bg-white/10 px-2.5 py-1 rounded">DCI (Dental)</span>
            <span className="bg-white/10 px-2.5 py-1 rounded">BCI (Law)</span>
            <span className="bg-white/10 px-2.5 py-1 rounded">PCI (Pharmacy)</span>
            <span className="bg-white/10 px-2.5 py-1 rounded">COA (Architecture)</span>
          </div>
        </div>
      </div>

      {/* Main Footer Links */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
          {/* Column 1: University Info */}
          <div className="lg:col-span-2 space-y-4">
            <div className="relative h-12 w-48">
              <Image
                src="/assets/logo.png"
                alt="Sharda University Logo"
                fill
                className="object-contain filter brightness-0 invert"
                sizes="192px"
              />
            </div>
            <p className="text-gray-400 leading-relaxed text-xs">
              Sharda University is a NAAC A+ accredited, leading multidisciplinary global university located in Greater Noida (Delhi-NCR), offering over 130+ undergraduate, postgraduate, and doctoral degrees.
            </p>
            <div className="space-y-2 pt-2 text-gray-300 text-xs">
              <div className="flex items-start space-x-2.5">
                <MapPin className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <span>Plot No. 32-34, Knowledge Park III, Greater Noida, UP - 201310 (Delhi-NCR), India</span>
              </div>
              <div className="flex items-center space-x-2.5">
                <Phone className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Admissions Hotline: +91-120-4570000 / 1800-3000-0000</span>
              </div>
              <div className="flex items-center space-x-2.5">
                <Mail className="w-4 h-4 text-amber-400 shrink-0" />
                <span>admission@sharda.ac.in | info@sharda.ac.in</span>
              </div>
            </div>
          </div>

          {/* Column 2: Schools */}
          <div className="space-y-3">
            <h4 className="text-white font-bold text-sm tracking-wider uppercase">Schools</h4>
            <ul className="space-y-2 text-xs">
              <li><a href="#schools" className="hover:text-amber-400 transition">Engineering & Tech (SET)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">Business Studies (SBS)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">Medical Sciences (SMS&R)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">Dental Sciences (SDS)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">School of Law (SOL)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">Design & Architecture (SAP)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">School of Pharmacy (SOP)</a></li>
              <li><a href="#schools" className="hover:text-amber-400 transition">Allied Health (SAHS)</a></li>
            </ul>
          </div>

          {/* Column 3: Admissions & Aid */}
          <div className="space-y-3">
            <h4 className="text-white font-bold text-sm tracking-wider uppercase">Admissions</h4>
            <ul className="space-y-2 text-xs">
              <li><a href="#admissions" className="hover:text-amber-400 transition">SUAT Entrance Exam 2026</a></li>
              <li><a href="#scholarship" className="hover:text-amber-400 transition">Merit Scholarships (Up to 100%)</a></li>
              <li><a href="#calculator" className="hover:text-amber-400 transition">Fee & Scholarship Calculator</a></li>
              <li><a href="#admissions" className="hover:text-amber-400 transition">Hostel Accommodation & Fee</a></li>
              <li><a href="#admissions" className="hover:text-amber-400 transition">International Admissions</a></li>
              <li><a href="#placements" className="hover:text-amber-400 transition">Placement Statistics (₹1 Cr Package)</a></li>
              <li><a href="#faqs" className="hover:text-amber-400 transition">Admission FAQs</a></li>
            </ul>
          </div>

          {/* Column 4: Compliance & Governance */}
          <div className="space-y-3">
            <h4 className="text-white font-bold text-sm tracking-wider uppercase">Governance & Policies</h4>
            <ul className="space-y-2 text-xs">
              <li><a href="#" className="hover:text-amber-400 transition">Mandatory Disclosures (UGC)</a></li>
              <li><a href="#" className="hover:text-amber-400 transition">Anti-Ragging Regulations</a></li>
              <li><a href="#" className="hover:text-amber-400 transition">Internal Complaints Committee (ICC)</a></li>
              <li><a href="#" className="hover:text-amber-400 transition">Equal Opportunity Cell</a></li>
              <li><a href="#" className="hover:text-amber-400 transition">DPDP Act 2023 & Privacy Policy</a></li>
              <li><a href="#" className="hover:text-amber-400 transition">Terms & Conditions</a></li>
              <li><a href="#" className="hover:text-amber-400 transition">Student ERP Portal Login</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Copyright Strip */}
        <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-gray-400">
          <p>© 2026 Sharda University. All Rights Reserved. Managed & Rebuilt by Sterco Digitex.</p>
          <div className="flex items-center space-x-4">
            <span>DPDP Act 2023 Compliant</span>
            <span>•</span>
            <span>GDPR Ready</span>
            <span>•</span>
            <span>SOC 2 Type II Verified</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
