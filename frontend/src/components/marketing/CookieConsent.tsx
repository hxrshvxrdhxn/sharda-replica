"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck, X } from "lucide-react";

export const CookieConsent: React.FC = () => {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem("sharda_cookie_consent");
    if (!consent) {
      setShowBanner(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem("sharda_cookie_consent", "accepted");
    setShowBanner(false);
  };

  const handleDecline = () => {
    localStorage.setItem("sharda_cookie_consent", "declined");
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-24 left-4 right-4 sm:left-6 sm:right-auto sm:max-w-md z-40 bg-[#1B2C39] text-white p-4 sm:p-5 rounded-2xl shadow-2xl border border-amber-400/40 animate-in slide-in-from-bottom-5 duration-300">
      <div className="flex items-start space-x-3">
        <div className="p-2 bg-amber-400/20 text-amber-400 rounded-xl shrink-0 mt-0.5">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div className="flex-1 text-xs text-gray-300 space-y-2">
          <p className="font-bold text-white text-sm">Privacy & Cookie Notice</p>
          <p className="leading-relaxed">
            We use essential cookies to deliver AI counseling, enhance navigation, and analyze admissions traffic compliant with the <strong>Digital Personal Data Protection (DPDP) Act 2023</strong> and GDPR.
          </p>
          <div className="flex items-center space-x-2 pt-1">
            <button
              onClick={handleAccept}
              className="bg-[#EAA914] hover:bg-[#D6950B] text-[#1B2C39] font-bold text-xs px-3.5 py-1.5 rounded-lg transition"
            >
              Accept All
            </button>
            <button
              onClick={handleDecline}
              className="bg-white/10 hover:bg-white/20 text-gray-300 text-xs px-3 py-1.5 rounded-lg transition"
            >
              Essential Only
            </button>
          </div>
        </div>
        <button
          onClick={() => setShowBanner(false)}
          className="text-gray-400 hover:text-white p-1"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
