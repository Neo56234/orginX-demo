"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AgentState, Finding } from "@/lib/store";

interface AgentCardProps {
  id: 'geolocator' | 'chronologist' | 'tracer' | 'linguist' | 'adjudicator';
  emoji: string;
  name: string;
  role: string;
  state: AgentState;
}

function WeightBadge({ weight, type }: { weight?: string; type?: string }) {
  if (type === 'decision_logic') {
    return (
      <span className="shrink-0 text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border text-primary bg-primary/10 border-primary/30">
        VERDICT
      </span>
    );
  }
  const cfg: Record<string, { color: string; label: string }> = {
    high:   { color: 'text-[#FF3B5C] bg-[#FF3B5C]/10 border-[#FF3B5C]/30', label: 'HIGH' },
    medium: { color: 'text-[#FFB833] bg-[#FFB833]/10 border-[#FFB833]/30', label: 'MED'  },
    low:    { color: 'text-gray-500 bg-gray-800 border-gray-700',           label: 'LOW'  },
  };
  const w = (weight ?? 'low').toLowerCase();
  const { color, label } = cfg[w] ?? cfg['low'];
  return (
    <span className={`shrink-0 text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border ${color}`}>
      {label}
    </span>
  );
}

function FindingRow({ finding, index }: { finding: Finding; index: number }) {
  const isDecision = finding.type === 'decision_logic';
  return (
    <motion.div
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.18, delay: index < 3 ? 0 : 0 }}
      className={`flex items-start gap-2 text-xs px-1 py-0.5 rounded ${
        isDecision ? 'bg-primary/5 border border-primary/20 mt-1' : ''
      }`}
    >
      <WeightBadge weight={finding.weight} type={finding.type} />
      <span className={`leading-relaxed break-words min-w-0 ${
        isDecision ? 'text-primary font-mono font-semibold' : 'text-gray-300'
      }`}>
        {finding.description ?? (finding as any).value ?? ''}
      </span>
    </motion.div>
  );
}

export default function AgentCard({ id, emoji, name, role, state }: AgentCardProps) {
  const feedRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest finding
  useEffect(() => {
    const el = feedRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [state.findings.length]);

  const getBorderColor = () => {
    if (state.status === 'running')  return '#3D8BFF';
    if (state.status === 'complete') return '#00D67E';
    if (state.status === 'failed')   return '#FF3B5C';
    return '#1f2937';
  };

  const getGlow = () => {
    if (state.status === 'running')  return '0 0 16px rgba(61,139,255,0.35)';
    if (state.status === 'complete') return '0 0 12px rgba(0,214,126,0.25)';
    if (state.status === 'failed')   return '0 0 12px rgba(255,59,92,0.25)';
    return 'none';
  };

  return (
    <motion.div
      layout
      animate={{ boxShadow: getGlow(), borderColor: getBorderColor() }}
      transition={{ duration: 0.5 }}
      className={`relative w-full rounded-xl bg-card border-2 p-4 overflow-hidden flex flex-col gap-2.5 transition-opacity ${
        state.status === 'idle' ? 'opacity-40' : 'opacity-100'
      }`}
    >
      {/* ── Header ── */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2.5 min-w-0">
          <span className={`text-2xl shrink-0 ${state.status === 'idle' ? 'grayscale opacity-50' : ''}`}>
            {emoji}
          </span>
          <div className="min-w-0">
            <h4 className="text-foreground font-bold font-sans tracking-wide m-0 leading-none text-sm">
              {name}
            </h4>
            <span className="text-gray-500 text-[11px] font-bangla truncate block">{role}</span>
          </div>
        </div>

        {/* Status pill */}
        <div className="shrink-0 text-[11px] font-mono font-bold">
          {state.status === 'running'  && (
            <motion.span
              className="text-primary"
              animate={{ opacity: [1, 0.4, 1] }}
              transition={{ repeat: Infinity, duration: 1.2 }}
            >
              RUNNING
            </motion.span>
          )}
          {state.status === 'complete' && <span className="text-[#00D67E]">DONE ✓</span>}
          {state.status === 'failed'   && <span className="text-[#FF3B5C]">FAILED</span>}
        </div>
      </div>

      {/* ── Progress bar ── */}
      <AnimatePresence>
        {(state.status === 'running' || state.status === 'complete') && (
          <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.max(4, state.progress * 100)}%` }}
              transition={{ duration: 0.4, ease: 'easeOut' }}
              className={`h-full ${state.status === 'complete' ? 'bg-[#00D67E]' : 'bg-primary'}`}
            />
          </div>
        )}
      </AnimatePresence>

      {/* ── Live terminal feed ── */}
      <div className="border-t border-gray-800/60 pt-2 flex flex-col gap-0.5 min-h-[56px]">

        {/* Current activity label */}
        {state.status === 'running' && state.statusText && (
          <motion.div
            key={state.statusText}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-1.5 text-[11px] text-primary font-mono mb-1 px-1"
          >
            <span className="shrink-0">▶</span>
            <span className="truncate">{state.statusText}</span>
            <motion.span
              animate={{ opacity: [1, 0, 1] }}
              transition={{ repeat: Infinity, duration: 0.9 }}
            >_</motion.span>
          </motion.div>
        )}

        {/* Findings list */}
        {state.findings.length > 0 ? (
          <div
            ref={feedRef}
            className="flex flex-col gap-0.5 max-h-[130px] overflow-y-auto pr-0.5"
            style={{ scrollbarWidth: 'none' }}
          >
            {state.findings.map((f, i) => (
              <FindingRow key={i} finding={f} index={i} />
            ))}
          </div>
        ) : (
          <p className="text-[11px] text-gray-600 italic px-1">
            {state.status === 'idle'    ? 'Waiting to start...'
            : state.status === 'running' ? 'Scanning...'
            : 'No findings recorded.'}
          </p>
        )}

        {/* Count badge when findings overflow */}
        {state.findings.length > 6 && (
          <p className="text-[10px] text-gray-600 font-mono text-right pr-1 mt-0.5">
            {state.findings.length} findings total
          </p>
        )}
      </div>

      {/* ── Error state ── */}
      {state.status === 'failed' && state.error && (
        <div className="text-[#FF3B5C] text-xs bg-[#0A0E1A] p-2 rounded border border-[#FF3B5C]/20">
          {state.error}
        </div>
      )}
    </motion.div>
  );
}
