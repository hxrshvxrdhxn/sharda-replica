import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sharda University - Best Private University in Delhi, NCR | NAAC A+",
  description:
    "Sharda University is a NAAC A+ accredited, leading private university in Greater Noida, Delhi-NCR offering 130+ programs across Engineering, Management, Medical, Law, Design, and Pharmacy.",
  keywords: [
    "Sharda University",
    "Best Private University in Delhi NCR",
    "Top University in Greater Noida",
    "B.Tech CSE Sharda",
    "MBA Admissions 2026",
    "SUAT 2026",
    "Sharda University Scholarships"
  ],
  authors: [{ name: "Sharda University" }, { name: "Sterco Digitex" }],
  openGraph: {
    title: "Sharda University - NAAC A+ Accredited Multidisciplinary Global University",
    description:
      "Explore 130+ futuristic undergraduate, postgraduate and doctoral degrees with up to 100% merit scholarships, ₹1 Crore highest package and global exchange programs.",
    url: "https://www.sharda.ac.in",
    siteName: "Sharda University",
    images: [
      {
        url: "/assets/campus_banner.jpg",
        width: 1200,
        height: 628,
        alt: "Sharda University Campus",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  icons: {
    icon: "/assets/favi-icon.png",
    shortcut: "/assets/favi-icon.png",
    apple: "/assets/favi-icon.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "CollegeOrUniversity",
        "@id": "https://www.sharda.ac.in/#organization",
        "name": "Sharda University",
        "alternateName": "Sharda University Greater Noida",
        "url": "https://www.sharda.ac.in/",
        "description":
          "Sharda University is a NAAC A+ accredited, UGC-approved private university in Greater Noida, Delhi-NCR, offering globally recognized programs in Engineering, Management, and Medical Sciences.",
        "foundingDate": "2009",
        "award": [
          "NAAC A+ Accreditation",
          "Top Ranked Private University in NCR",
          "Best Private University in NCR for Global Exposure"
        ],
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.sharda.ac.in/attachments/site_logo/logo22.png"
        },
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Plot No. 32-34, Knowledge Park III",
          "addressLocality": "Greater Noida",
          "addressRegion": "Uttar Pradesh",
          "postalCode": "201310",
          "addressCountry": "IN"
        },
        "telephone": "+91-120-4570000"
      }
    ]
  };

  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="antialiased flex flex-col min-h-screen">
        {children}
      </body>
    </html>
  );
}
