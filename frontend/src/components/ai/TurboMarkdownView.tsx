"use client";

import React from "react";
import Link from "next/link";
import { ExternalLink, Sparkles, BookOpen, ArrowRight } from "lucide-react";

interface TurboMarkdownViewProps {
  content: string;
}

export const TurboMarkdownView: React.FC<TurboMarkdownViewProps> = ({ content }) => {
  if (!content) return null;

  // Split lines to parse blocks (tables, headers, lists, links, paragraphs)
  const lines = content.split("\n");
  const elements: React.ReactNode[] = [];
  
  let currentTableRows: string[][] = [];
  let inTable = false;

  const renderInline = (text: string): React.ReactNode => {
    if (!text) return null;

    // Check for link pattern: [Text](url) or 🔗 [Text](url)
    const linkRegex = /(?:🔗\s*)?\[(.*?)\]\((.*?)\)/g;
    const parts: React.ReactNode[] = [];
    let lastIndex = 0;
    let match: RegExpExecArray | null;

    while ((match = linkRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(renderFormatting(text.substring(lastIndex, match.index)));
      }
      const linkText = match[1];
      const linkUrl = match[2];
      
      parts.push(
        <Link
          key={`${match.index}-${linkUrl}`}
          href={linkUrl.startsWith("http") ? linkUrl : linkUrl}
          className="inline-flex items-center gap-1.5 bg-amber-400/15 hover:bg-amber-400/25 border border-amber-400/40 hover:border-amber-400 text-amber-300 hover:text-amber-200 px-3 py-1 rounded-lg text-xs font-semibold my-1 transition-all duration-200 shadow-sm group"
        >
          <ExternalLink className="w-3.5 h-3.5 text-amber-400 group-hover:scale-110 transition-transform" />
          <span>{linkText}</span>
          <ArrowRight className="w-3 h-3 opacity-60 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all" />
        </Link>
      );
      lastIndex = linkRegex.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push(renderFormatting(text.substring(lastIndex)));
    }

    return parts.length > 0 ? parts : renderFormatting(text);
  };

  const renderFormatting = (raw: string): React.ReactNode => {
    // Process Bold (***text***, **text**, *text*)
    const boldRegex = /\*\*(.*?)\*\*/g;
    const subParts: React.ReactNode[] = [];
    let lastIdx = 0;
    let bMatch: RegExpExecArray | null;

    while ((bMatch = boldRegex.exec(raw)) !== null) {
      if (bMatch.index > lastIdx) {
        subParts.push(raw.substring(lastIdx, bMatch.index));
      }
      subParts.push(
        <strong key={`b-${bMatch.index}`} className="text-white font-bold">
          {bMatch[1]}
        </strong>
      );
      lastIdx = boldRegex.lastIndex;
    }

    if (lastIdx < raw.length) {
      subParts.push(raw.substring(lastIdx));
    }

    return subParts.length > 0 ? subParts : raw;
  };

  const flushTable = (keyIndex: number) => {
    if (currentTableRows.length === 0) return;
    const [headerRow, ...bodyRows] = currentTableRows;
    elements.push(
      <div key={`table-${keyIndex}`} className="overflow-x-auto my-3.5 rounded-xl border border-gray-700/60 shadow-lg">
        <table className="w-full text-left text-xs text-gray-200 border-collapse">
          <thead>
            <tr className="bg-[#1e2f3d] border-b border-gray-700/80 text-amber-300 font-bold uppercase tracking-wider">
              {headerRow.map((cell, cIdx) => (
                <th key={`th-${cIdx}`} className="py-2.5 px-3 border-r border-gray-700/60 last:border-r-0">
                  {renderInline(cell.trim())}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/60 bg-[#14202b]">
            {bodyRows.map((row, rIdx) => (
              <tr key={`tr-${rIdx}`} className="hover:bg-amber-400/5 transition-colors">
                {row.map((cell, cIdx) => (
                  <td key={`td-${rIdx}-${cIdx}`} className="py-2 px-3 border-r border-gray-800/60 last:border-r-0 text-gray-300">
                    {renderInline(cell.trim())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
    currentTableRows = [];
    inTable = false;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Table line: | ... |
    if (line.startsWith("|") && line.endsWith("|")) {
      // Separator row: |:---|:---| or |---|---|
      if (/^\|[\s\-:]+\|$/.test(line)) {
        continue;
      }
      const cells = line.split("|").slice(1, -1);
      currentTableRows.push(cells);
      inTable = true;
      continue;
    } else {
      if (inTable) {
        flushTable(i);
      }
    }

    if (!line) {
      elements.push(<div key={`spacer-${i}`} className="h-2" />);
      continue;
    }

    // Headers
    if (line.startsWith("### ")) {
      elements.push(
        <h4 key={`h4-${i}`} className="text-sm font-bold text-amber-400 mt-3 mb-1.5 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5" />
          <span>{renderInline(line.replace(/^###\s+/, ""))}</span>
        </h4>
      );
    } else if (line.startsWith("## ")) {
      elements.push(
        <h3 key={`h3-${i}`} className="text-base font-bold text-amber-400 mt-3.5 mb-2">
          {renderInline(line.replace(/^##\s+/, ""))}
        </h3>
      );
    } else if (line.startsWith("# ")) {
      elements.push(
        <h2 key={`h2-${i}`} className="text-lg font-extrabold text-amber-400 mt-4 mb-2">
          {renderInline(line.replace(/^#\s+/, ""))}
        </h2>
      );
    }
    // Standalone Link line: 🔗 [Text](url)
    else if (line.startsWith("🔗") || line.startsWith("- 🔗")) {
      elements.push(
        <div key={`link-row-${i}`} className="my-1">
          {renderInline(line)}
        </div>
      );
    }
    // Bullet item: - ... or * ...
    else if (line.startsWith("- ") || line.startsWith("* ")) {
      elements.push(
        <li key={`li-${i}`} className="ml-4 mb-1 text-xs sm:text-sm leading-relaxed text-gray-300 list-disc marker:text-amber-400">
          {renderInline(line.substring(2))}
        </li>
      );
    }
    // Numbered item: 1. ...
    else if (/^\d+\.\s/.test(line)) {
      const match = line.match(/^(\d+)\.\s(.*)$/);
      if (match) {
        elements.push(
          <div key={`ol-${i}`} className="flex items-start gap-2 ml-2 mb-1.5 text-xs sm:text-sm leading-relaxed text-gray-300">
            <span className="text-amber-400 font-bold min-w-[18px]">{match[1]}.</span>
            <div>{renderInline(match[2])}</div>
          </div>
        );
      }
    }
    // Standard paragraph
    else {
      elements.push(
        <p key={`p-${i}`} className="text-xs sm:text-sm leading-relaxed text-gray-200 my-1">
          {renderInline(line)}
        </p>
      );
    }
  }

  if (inTable) {
    flushTable(lines.length);
  }

  return <div className="space-y-1">{elements}</div>;
};
