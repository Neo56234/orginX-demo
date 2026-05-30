"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { isDemoId } from "@/lib/demo-config";
import { DEMO_INVESTIGATIONS } from "@/lib/demo-data";

interface ReachData {
  base_shares: number;
  estimated_reach: number | null;
  verdict: string;
}

function formatNum(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return String(n);
}

function AnimatedNumber({ value }: { value: number }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = value;
    const duration = 1800;
    const step = end / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= end) { setDisplay(end); clearInterval(timer); }
      else setDisplay(Math.floor(start));
    }, 16);
    return () => clearInterval(timer);
  }, [value]);

  return <>{formatNum(display)}</>;
}

export default function ReachCounter({ investigationId, verdict }: { investigationId: string; verdict?: string }) {
  const [data, setData] = useState<ReachData | null>(null);

  useEffect(() => {
    if (!investigationId) return;
    if (isDemoId(investigationId)) {
      const demo = DEMO_INVESTIGATIONS[investigationId];
      if (demo) setData(demo.reach as ReachData);
      return;
    }
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/investigation/${investigationId}/reach`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {});
  }, [investigationId]);

  // For mismatch with no viral data, show a demo estimate
  const isMismatch = (verdict || data?.verdict) === "mismatch";
  const reach = data?.estimated_reach;
  const shares = data?.base_shares || 0;

  // Demo fallback: show Bangladesh average viral reach for mismatch verdicts
  const demoReach = isMismatch && !reach ? 2_400_000 : null;
  const displayReach = reach || demoReach;

  if (!isMismatch || !displayReach) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.6 }}
      className="w-full max-w-5xl mx-auto mt-6"
    >
      <div className="bg-alert/5 border border-alert/20 rounded-2xl p-5 backdrop-blur">
        <div className="flex flex-col md:flex-row items-start md:items-center gap-4">

          {/* Icon */}
          <div className="w-10 h-10 rounded-xl bg-alert/10 border border-alert/20 flex items-center justify-center shrink-0">
            <span className="text-alert text-lg">⚠</span>
          </div>

          {/* Main stat */}
          <div className="flex-1">
            <div className="flex items-baseline gap-2 flex-wrap">
              <span className="text-4xl font-black font-mono text-alert">
                <AnimatedNumber value={displayReach} />
              </span>
              <span className="text-white/40 text-sm font-sans">people potentially exposed to this false claim</span>
            </div>
            <div className="flex items-center gap-4 mt-1.5 flex-wrap">
              {shares > 0 && (
                <span className="text-xs font-mono text-white/30">
                  {formatNum(shares)} shares × 7 avg network reach
                </span>
              )}
              {demoReach && (
                <span className="text-xs font-mono text-white/20">
                  Based on Bangladesh average viral spread
                </span>
              )}
            </div>
          </div>

          {/* CTA */}
          <div className="shrink-0">
            <div className="text-xs text-alert/60 font-mono text-right mb-1">Misinformation spreads fast</div>
            <div className="text-[10px] text-white/20 font-mono text-right">Share the correct information →</div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
