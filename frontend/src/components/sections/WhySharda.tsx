"use client";

import React from "react";
import { Award, Globe, BookOpen, ShieldCheck, Microscope, HeartHandshake } from "lucide-react";

export const WhySharda: React.FC = () => {
  const pillars = [
    {
      icon: <Award className="w-6 h-6 text-amber-500" />,
      title: "NAAC A+ Accredited",
      description: "Recognized among top tier Indian higher education institutions with highest quality standards in academics, research, and governance."
    },
    {
      icon: <Globe className="w-6 h-6 text-sky-500" />,
      title: "130+ Global Collaborations",
      description: "Active academic partnerships with top universities across USA, UK, Canada, Australia, and Germany for semester exchanges and dual degrees."
    },
    {
      icon: <Microscope className="w-6 h-6 text-emerald-500" />,
      title: "Advanced Research & Patents",
      description: "State-of-the-art incubation centres, multidisciplinary research hubs, and 450+ patents filed by faculty and students."
    },
    {
      icon: <BookOpen className="w-6 h-6 text-purple-500" />,
      title: "Industry-Driven Curriculum",
      description: "Course curriculums continuously upgraded in consultation with industry leaders from Microsoft, Amazon, KPMG, and L&T."
    },
    {
      icon: <ShieldCheck className="w-6 h-6 text-indigo-500" />,
      title: "63+ Acre Wi-Fi Smart Campus",
      description: "Modern campus in Greater Noida with Olympic-standard sports complexes, multi-cuisine food courts, AC residential towers, and 24x7 security."
    },
    {
      icon: <HeartHandshake className="w-6 h-6 text-rose-500" />,
      title: "1200+ Bed Multi-Speciality Hospital",
      description: "Direct on-campus clinical postings and patient exposure for medical, dental, pharmacy, and allied health students at Sharda Hospital."
    }
  ];

  return (
    <section id="why-sharda" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-14">
          <span className="text-xs font-bold uppercase tracking-wider text-[#A61C24] bg-red-50 px-3.5 py-1.5 rounded-full">
            The Sharda Advantage
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#1B2C39] mt-3">
            Why Choose Sharda University?
          </h2>
          <p className="text-gray-600 text-sm sm:text-base mt-2">
            An ecosystem designed to empower students with global perspectives, experiential learning, and top placement outcomes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {pillars.map((p, idx) => (
            <div
              key={idx}
              className="p-7 rounded-2xl bg-gray-50/70 border border-gray-100 hover:border-amber-300 hover:bg-white hover:shadow-xl transition-all duration-300 flex flex-col justify-between"
            >
              <div className="p-3 bg-white shadow-sm rounded-xl w-fit mb-5">
                {p.icon}
              </div>
              <h3 className="text-lg font-bold text-[#1B2C39] mb-2">{p.title}</h3>
              <p className="text-xs text-gray-600 leading-relaxed">{p.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
