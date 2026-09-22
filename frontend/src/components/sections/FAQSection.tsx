"use client";

import React, { useState } from "react";
import { ChevronDown, HelpCircle, Sparkles } from "lucide-react";

interface FAQSectionProps {
  onOpenAIChat: (query: string) => void;
}

export const FAQSection: React.FC<FAQSectionProps> = ({ onOpenAIChat }) => {
  const [openIdx, setOpenIdx] = useState<number | null>(0);

  const faqs = [
    {
      question: "What is SUAT and is it mandatory for admission at Sharda University?",
      answer: "SUAT (Sharda University Admission Test) is the single entrance examination for admissions into UG and PG programs at Sharda University. Candidates who have qualified national level exams such as JEE Main (B.Tech), NEET (MBBS/BDS), CAT/MAT/XAT (MBA), CLAT (Law), or NATA (Architecture) are exempted from SUAT."
    },
    {
      question: "What scholarship criteria does Sharda University offer for academic merit?",
      answer: "Sharda University provides up to 100% tuition fee waivers based on academic merit in 10+2: 95%+ in boards gives 100% waiver, 90-94.99% gives 50% waiver, 85-89.99% gives 40% waiver, 80-84.99% gives 20% waiver, and 75-79.99% gives 10% waiver. In addition, up to 100% sports quota scholarships and 5% defense ward discounts are available."
    },
    {
      question: "What are the hostel room options and facilities available on campus?",
      answer: "Sharda University provides fully secure on-campus residential accommodation for boys and girls with AC and Non-AC options (3-seater, 2-seater, and Single Studio AC). Fees range from ₹1,16,000 to ₹2,35,000 per year including 4 daily meals, 24/7 Wi-Fi, electricity backup, laundry, housekeeping, and gymnasium access."
    },
    {
      question: "What placement opportunities and highest packages do students receive?",
      answer: "Sharda University achieved a highest international package of ₹1.00 Crore and a domestic CTC of ₹45.00 LPA. Over 600+ multinational recruiters including Microsoft, Amazon, Deloitte, KPMG, Cognizant, Wipro, TCS, and Infosys participate with a 95%+ placement rate."
    },
    {
      question: "How can I apply for admission for the 2026 academic batch?",
      answer: "You can apply online by visiting admission.sharda.ac.in or clicking the 'Apply Now' button on this portal. After filling in your academic details and paying the nominal application fee (₹1500), you will receive a slot for SUAT or direct counseling based on your national test score."
    }
  ];

  return (
    <section id="faqs" className="py-20 bg-gray-50/70">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-[#A61C24] bg-red-50 px-3.5 py-1.5 rounded-full inline-flex items-center space-x-1">
            <HelpCircle className="w-3.5 h-3.5 text-[#A61C24]" />
            <span>Admissions & Campus Queries</span>
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#1B2C39] mt-3">
            Frequently Asked Questions
          </h2>
          <p className="text-gray-500 text-sm mt-1">
            Quick answers to the most common queries from prospective students and parents.
          </p>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, idx) => {
            const isOpen = openIdx === idx;
            return (
              <div
                key={idx}
                className="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm transition"
              >
                <button
                  onClick={() => setOpenIdx(isOpen ? null : idx)}
                  className="w-full text-left px-6 py-4 flex items-center justify-between space-x-4 focus:outline-none"
                >
                  <span className="text-sm sm:text-base font-bold text-[#1B2C39]">
                    {faq.question}
                  </span>
                  <ChevronDown
                    className={`w-5 h-5 text-gray-400 transition-transform duration-200 shrink-0 ${
                      isOpen ? "transform rotate-180 text-amber-500" : ""
                    }`}
                  />
                </button>

                {isOpen && (
                  <div className="px-6 pb-5 pt-1 text-xs sm:text-sm text-gray-600 leading-relaxed border-t border-gray-100 bg-gray-50/40">
                    <p>{faq.answer}</p>
                    <div className="mt-3">
                      <button
                        onClick={() => onOpenAIChat(`Give more details on: ${faq.question}`)}
                        className="text-xs font-semibold text-amber-600 hover:text-amber-700 flex items-center space-x-1"
                      >
                        <Sparkles className="w-3 h-3 text-amber-500" />
                        <span>Ask Sharda AI more about this</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
