"use client";

import { motion } from "framer-motion";
import { useInvestigationStore } from "@/lib/store";

export default function Timeline() {
  const verdict = useInvestigationStore(state => state.verdict) as any;
  const claimedDateStored = useInvestigationStore(state => state.claimedDate);
  const chronologist = useInvestigationStore(state => state.agents.chronologist);
  const lang = useInvestigationStore(state => state.language);

  if (chronologist.status !== 'complete' && !verdict) {
    return null;
  }

  // --- Resolve actual origin date ---
  // 1. Prefer adjudicator verdict (most authoritative)
  let actualDateStr: string | null = verdict?.actual_origin_date || null;

  // 2. Fall back to a date extracted from Chronologist findings
  if (!actualDateStr) {
    const findingWithDate = chronologist.findings.find(
      (f: any) => f.type === 'earliest_archive' || f.type === 'date' || f.description?.match(/\d{4}-\d{2}-\d{2}/)
    );
    if (findingWithDate) {
      if (findingWithDate.value && String(findingWithDate.value).match(/\d{4}/)) {
        actualDateStr = findingWithDate.value;
      } else if (findingWithDate.description) {
        const m = findingWithDate.description.match(/\d{4}-\d{2}-\d{2}/);
        if (m) actualDateStr = m[0];
      }
    }
  }

  // --- Resolve claimed date ---
  // claimedDateStored is populated from the backend-parsed value (extract_claimed_date)
  // on the initial investigation fetch. Only fall back to today if we have a verdict
  // but no stored date (e.g. legacy investigation with no claimed_date in DB).
  const claimedDateStr = claimedDateStored || (verdict ? new Date().toISOString() : null);

  // Need both dates to render
  if (!actualDateStr || !claimedDateStr) return null;

  const claimedDate = new Date(claimedDateStr);
  const actualDate = new Date(actualDateStr);

  // Don't show if actual is same or later (no mismatch to visualise)
  if (actualDate >= claimedDate) return null;

  // --- Gap label ---
  const diffDays = Math.ceil(Math.abs(claimedDate.getTime() - actualDate.getTime()) / 86400000);
  const diffYears = Math.floor(diffDays / 365);
  const remainingMonths = Math.floor((diffDays % 365) / 30);

  let gapTextBn = "";
  let gapTextEn = "";
  if (diffYears > 0) {
    gapTextBn += `${diffYears} বছর `;
    gapTextEn += `${diffYears} year${diffYears > 1 ? 's' : ''} `;
  }
  if (remainingMonths > 0 || diffYears === 0) {
    gapTextBn += `${remainingMonths} মাস `;
    gapTextEn += `${remainingMonths} month${remainingMonths !== 1 ? 's' : ''} `;
  }
  const gapText = lang === 'bn' ? `${gapTextBn.trim()} আগের ভিডিও` : `${gapTextEn.trim()} older video`;

  // --- Timeline positions ---
  // Markers at 15% (actual) and 85% (claimed). The gap highlight spans between them.
  const actualPos = 15;
  const claimedPos = 85;
  const gapWidthPct = claimedPos - actualPos;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-5xl mx-auto mt-8 bg-card/30 p-8 rounded-2xl border border-gray-800"
    >
      <h3 className="text-gray-400 text-sm uppercase tracking-widest mb-12 font-sans text-center">
        {lang === 'bn' ? 'সময়কাল বিশ্লেষণ' : 'Timeline Analysis'}
      </h3>

      <div className="relative w-full h-12 flex items-center px-10">
        {/* Base Line */}
        <div className="absolute left-10 right-10 h-1 bg-gray-800 rounded-full" />

        {/* Gap Highlight — spans exactly between the two markers */}
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${gapWidthPct}%` }}
          style={{ left: `${actualPos}%` }}
          className="absolute h-1 bg-gradient-to-r from-truth to-alert rounded-full"
        />

        {/* Actual Date Marker (Green) */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring' }}
          style={{ left: `${actualPos}%` }}
          className="absolute -translate-x-1/2 flex flex-col items-center group cursor-pointer"
        >
          <div className="w-4 h-4 rounded-full bg-truth border-4 border-card shadow-[0_0_10px_rgba(0,214,126,0.5)] z-10" />
          <div className="absolute -top-10 whitespace-nowrap bg-gray-900 text-truth text-xs font-mono px-3 py-1 rounded border border-truth/30 opacity-0 group-hover:opacity-100 transition-opacity">
            {lang === 'bn' ? 'আসল সময়' : 'Actual Origin'}
          </div>
          <div className="mt-4 text-center">
            <p className="text-truth font-bold text-sm">
              {actualDate.toLocaleDateString(lang === 'bn' ? 'bn-BD' : 'en-US', { year: 'numeric', month: 'short' })}
            </p>
          </div>
        </motion.div>

        {/* Claimed Date Marker (Red) */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.4, type: 'spring' }}
          style={{ left: `${claimedPos}%` }}
          className="absolute -translate-x-1/2 flex flex-col items-center group cursor-pointer"
        >
          <div className="w-4 h-4 rounded-full bg-alert border-4 border-card shadow-[0_0_10px_rgba(255,59,92,0.5)] z-10" />
          <div className="absolute -top-10 whitespace-nowrap bg-gray-900 text-alert text-xs font-mono px-3 py-1 rounded border border-alert/30 opacity-0 group-hover:opacity-100 transition-opacity">
            {lang === 'bn' ? 'দাবিকৃত সময়' : 'Claimed Context'}
          </div>
          <div className="mt-4 text-center">
            <p className="text-alert font-bold text-sm">
              {claimedDate.toLocaleDateString(lang === 'bn' ? 'bn-BD' : 'en-US', { year: 'numeric', month: 'short' })}
            </p>
          </div>
        </motion.div>

        {/* Gap label centred between the two markers */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          style={{ left: `${(actualPos + claimedPos) / 2}%` }}
          className="absolute -translate-x-1/2 -top-10 flex flex-col items-center z-20"
        >
          <div className="bg-[#0A0E1A] text-gray-300 text-xs px-3 py-1 rounded-full font-bangla whitespace-nowrap border border-gray-700 shadow-md">
            {gapText}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
