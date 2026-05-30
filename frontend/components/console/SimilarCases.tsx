"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { isDemoId } from "@/lib/demo-config";
import { DEMO_INVESTIGATIONS } from "@/lib/demo-data";

interface SimilarCase {
  id: number;
  title_en: string;
  title_bn: string;
  false_claim_en: string;
  actual_origin_country: string;
  actual_origin_city: string;
  actual_origin_date: string;
  debunk_url: string;
  debunk_source: string;
}

export default function SimilarCases({ investigationId }: { investigationId: string }) {
  const [cases, setCases] = useState<SimilarCase[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!investigationId) return;
    if (isDemoId(investigationId)) {
      const demo = DEMO_INVESTIGATIONS[investigationId];
      setCases(demo?.similarCases || []);
      setLoading(false);
      return;
    }
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/investigation/${investigationId}/similar`)
      .then((r) => r.json())
      .then((data) => { setCases(data || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [investigationId]);

  if (loading || cases.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="w-full max-w-5xl mx-auto mt-8"
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="h-px flex-1 bg-white/5" />
        <div className="flex items-center gap-2">
          <span className="text-warning text-sm">⬡</span>
          <span className="text-white/40 font-mono text-xs tracking-widest uppercase">
            Similar Past Incidents
          </span>
          <span className="bg-warning/10 text-warning border border-warning/20 text-[10px] font-mono px-2 py-0.5 rounded-full">
            {cases.length} found
          </span>
        </div>
        <div className="h-px flex-1 bg-white/5" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <AnimatePresence>
          {cases.map((c, i) => (
            <motion.div
              key={c.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-card/50 backdrop-blur border border-white/5 rounded-2xl p-4 flex flex-col gap-3 hover:border-white/10 transition-all group"
            >
              {/* Origin badge */}
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono text-white/30 bg-white/5 px-2 py-1 rounded-full border border-white/5">
                  {c.actual_origin_city ? `${c.actual_origin_city}, ` : ""}{c.actual_origin_country}
                </span>
                {c.actual_origin_date && (
                  <span className="text-[10px] font-mono text-white/20">
                    {c.actual_origin_date.slice(0, 10)}
                  </span>
                )}
              </div>

              {/* Title */}
              <p className="text-white/80 text-xs leading-relaxed line-clamp-3 font-sans">
                {c.title_en}
              </p>

              {/* False claim */}
              <div className="bg-alert/5 border border-alert/15 rounded-xl px-3 py-2">
                <p className="text-[10px] text-alert/70 font-mono mb-1 uppercase tracking-wider">False claim</p>
                <p className="text-xs text-white/50 line-clamp-2">{c.false_claim_en}</p>
              </div>

              {/* Source link */}
              {c.debunk_url && (
                <a
                  href={c.debunk_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[10px] font-mono text-primary/60 hover:text-primary transition-colors flex items-center gap-1 mt-auto"
                >
                  <span>↗</span>
                  <span>{c.debunk_source || "Source"}</span>
                </a>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
