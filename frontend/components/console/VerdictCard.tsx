"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useInvestigationStore, KeyEvidence } from "@/lib/store";
import { useRouter } from "next/navigation";
import { t } from "@/lib/i18n";
import { useState, useEffect } from "react";

const AGENT_COLORS: Record<string, string> = {
  tracer:       'text-[#3D8BFF] bg-[#3D8BFF]/10 border-[#3D8BFF]/25',
  chronologist: 'text-[#A78BFA] bg-[#A78BFA]/10 border-[#A78BFA]/25',
  geolocator:   'text-[#34D399] bg-[#34D399]/10 border-[#34D399]/25',
  linguist:     'text-[#FBBF24] bg-[#FBBF24]/10 border-[#FBBF24]/25',
};

function EvidenceRow({ item, index }: { item: KeyEvidence; index: number }) {
  const agentColor = AGENT_COLORS[item.agent] ?? 'text-gray-400 bg-gray-800/50 border-gray-700';
  const weightColor =
    item.weight === 'high'   ? 'text-[#FF3B5C]' :
    item.weight === 'medium' ? 'text-[#FFB833]' :
                               'text-gray-500';
  const weightBars =
    item.weight === 'high'   ? '████' :
    item.weight === 'medium' ? '███░' :
                               '██░░';

  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.2 + index * 0.12, duration: 0.3 }}
      className="flex items-start gap-2 md:gap-3"
    >
      {/* Agent badge */}
      <span className={`shrink-0 text-[9px] md:text-[10px] font-mono font-bold px-1.5 md:px-2 py-0.5 rounded border uppercase ${agentColor}`}>
        {item.agent}
      </span>

      {/* Finding text */}
      <span className="text-xs md:text-sm text-gray-300 flex-1 leading-relaxed text-left">
        {item.finding}
      </span>

      {/* Weight bars — hidden on very small screens */}
      <span className={`hidden sm:block shrink-0 text-[11px] font-mono font-bold ${weightColor}`} title={item.weight}>
        {weightBars}
      </span>
    </motion.div>
  );
}

export default function VerdictCard() {
  const verdict = useInvestigationStore(state => state.verdict);
  const lang = useInvestigationStore(state => state.language);
  const jobId = useInvestigationStore(state => state.currentJobId);
  const router = useRouter();
  const [show, setShow] = useState(false);
  const [thinkingStep, setThinkingStep] = useState(0);

  useEffect(() => {
    if (verdict) {
      setShow(true);
      setThinkingStep(0);
      
      const steps = [1, 2, 3, 4];
      steps.forEach((step, index) => {
        setTimeout(() => {
          setThinkingStep(step);
        }, (index + 1) * 1500); // 1.5s per step
      });
    } else {
      setShow(false);
      setThinkingStep(0);
    }
  }, [verdict]);

  if (!verdict) return null;

  const getStatusConfig = () => {
    switch(verdict.status) {
      case 'mismatch': return { color: 'text-[#FF3B5C]', bg: 'bg-[#FF3B5C]/10', border: 'border-[#FF3B5C]', icon: '⚠️', labelBn: 'মিথ্যা প্রসঙ্গ সনাক্ত', labelEn: 'False Context Detected' };
      case 'authentic': return { color: 'text-[#00D67E]', bg: 'bg-[#00D67E]/10', border: 'border-[#00D67E]', icon: '✓', labelBn: 'সত্যতা নিশ্চিত', labelEn: 'Authentic Video' };
      case 'insufficient_evidence': return { color: 'text-[#FFB833]', bg: 'bg-[#FFB833]/10', border: 'border-[#FFB833]', icon: '◐', labelBn: 'অপর্যাপ্ত প্রমাণ', labelEn: 'Insufficient Evidence' };
      default: return { color: 'text-gray-400', bg: 'bg-gray-800', border: 'border-gray-700', icon: '?', labelBn: 'অজানা', labelEn: 'Unknown' };
    }
  };

  const config = getStatusConfig();
  const confPercentage = Math.round(verdict.confidence * 100);

  const getThinkingText = (step: number) => {
    if (step === 0) return lang === 'bn' ? "অ্যাডজুডিকেটর প্রোটোকল শুরু হচ্ছে..." : "Initializing Adjudicator protocol...";
    if (step === 1) return lang === 'bn' ? "এজেন্টদের রিপোর্ট অ্যানালাইজ করা হচ্ছে..." : "Synthesizing evidence from specialist agents...";
    if (step === 2) return lang === 'bn' ? "দাবিকৃত সময়ের সাথে আসল তথ্যের তুলনা চলছে..." : "Cross-referencing claimed context with actual findings...";
    if (step === 3) {
      if (verdict.status === 'mismatch') return lang === 'bn' ? "⚠️ বড় ধরনের অসামঞ্জস্য পাওয়া গেছে!" : "⚠️ Critical contradiction detected!";
      if (verdict.status === 'authentic') return lang === 'bn' ? "✓ দাবির সাথে প্রমাণের মিল পাওয়া গেছে।" : "✓ Evidence corroborates claim.";
      return lang === 'bn' ? "◐ চূড়ান্ত সিদ্ধান্তের জন্য যথেষ্ট প্রমাণ নেই।" : "◐ Insufficient evidence to conclude.";
    }
    return "";
  };

  return (
    <AnimatePresence>
      {show && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#0A0E1A]/90 backdrop-blur-md overflow-y-auto">
          {thinkingStep < 4 ? (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center justify-center gap-6"
            >
              <div className="w-16 h-16 border-4 border-gray-800 border-t-primary rounded-full animate-spin" />
              <div className="text-sm md:text-xl font-mono text-primary bg-black/50 px-4 md:px-6 py-3 rounded-lg border border-primary/30 shadow-[0_0_15px_rgba(61,139,255,0.2)] max-w-[90vw] text-center">
                {getThinkingText(thinkingStep)}
                <motion.span
                  animate={{ opacity: [0, 1, 0] }}
                  transition={{ repeat: Infinity, duration: 0.8 }}
                >
                  _
                </motion.span>
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="final-card"
              initial={{ opacity: 0, scale: 0.8, y: 50 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              transition={{ duration: 0.8, ease: [0.34, 1.56, 0.64, 1] }}
              className={`relative w-full max-w-3xl bg-card rounded-3xl border-2 ${config.border} p-8 md:p-12 flex flex-col items-center text-center overflow-hidden`}
              style={{
                boxShadow: verdict.status === 'mismatch' ? '0 25px 50px -12px rgba(255,59,92,0.3)' :
                           verdict.status === 'authentic' ? '0 25px 50px -12px rgba(0,214,126,0.3)' :
                           '0 25px 50px -12px rgba(255,184,51,0.2)'
              }}
            >
              {/* Status Badge */}
              <div className={`inline-flex items-center gap-3 px-6 py-3 rounded-full ${config.bg} ${config.border} border mb-8`}>
                <span className={`text-3xl ${config.color}`}>{config.icon}</span>
                <span className={`text-2xl font-bold font-bangla ${config.color} tracking-wide`}>
                  {lang === 'bn' ? config.labelBn : config.labelEn}
                </span>
              </div>

              {/* Summaries */}
              <h2 className="text-xl md:text-3xl lg:text-4xl font-bold font-bangla text-foreground mb-4 leading-tight">
                {verdict.summary_bn}
              </h2>
              <p className="text-sm md:text-lg lg:text-xl text-gray-400 font-sans mb-8 md:mb-10 max-w-2xl">
                {verdict.summary_en}
              </p>

              {/* Confidence Bar */}
              <div className="w-full max-w-md mb-12">
                <div className="flex justify-between text-sm font-sans mb-2">
                  <span className="text-gray-400 uppercase tracking-wider">{t('confidence', lang)}</span>
                  <span className={`font-mono font-bold ${config.color}`}>{confPercentage}%</span>
                </div>
                <div className="h-3 w-full bg-gray-800 rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${confPercentage}%` }}
                    transition={{ delay: 0.5, duration: 1, ease: "easeOut" }}
                    className={`h-full ${
                      verdict.status === 'mismatch' ? 'bg-alert' : 
                      verdict.status === 'authentic' ? 'bg-truth' : 'bg-warning'
                    }`}
                  />
                </div>
              </div>

              {/* ── Why this decision? ── */}
              {verdict.key_evidence && verdict.key_evidence.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.2, duration: 0.4 }}
                  className="w-full max-w-2xl mb-8"
                >
                  <div className="border border-gray-700/80 rounded-xl overflow-hidden text-left">
                    {/* Header bar */}
                    <div className="bg-gray-900/80 px-4 py-2 border-b border-gray-700/80 flex items-center gap-2">
                      <span className="text-[10px] font-mono text-gray-400 uppercase tracking-widest">
                        ⚖ Why this decision?
                      </span>
                    </div>

                    {/* Evidence rows */}
                    <div className="px-4 py-3 flex flex-col gap-3 bg-[#0A0E1A]/60">
                      {verdict.key_evidence.map((item, i) => (
                        <EvidenceRow key={i} item={item} index={i} />
                      ))}
                    </div>

                    {/* Decision summary footer */}
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.2 + verdict.key_evidence.length * 0.12 + 0.3 }}
                      className="border-t border-gray-700/80 bg-gray-900/60 px-4 py-2.5 flex items-center justify-between"
                    >
                      <span className="text-[11px] font-mono text-gray-500">
                        {verdict.key_evidence.filter(e => e.weight === 'high').length}× HIGH&nbsp;
                        {verdict.key_evidence.filter(e => e.weight === 'medium').length > 0 &&
                          `+ ${verdict.key_evidence.filter(e => e.weight === 'medium').length}× MED`
                        }
                        &nbsp;evidence
                      </span>
                      <span className={`text-[11px] font-mono font-bold shrink-0 ${
                        verdict.status === 'mismatch'             ? 'text-[#FF3B5C]' :
                        verdict.status === 'authentic'            ? 'text-[#00D67E]' :
                                                                    'text-[#FFB833]'
                      }`}>
                        {Math.round(verdict.confidence * 100)}% → {verdict.status.toUpperCase().replace('_', ' ')}
                      </span>
                    </motion.div>
                  </div>
                </motion.div>
              )}

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 w-full justify-center">
                <button 
                  onClick={() => setShow(false)}
                  className="px-8 py-4 rounded-xl font-bold font-bangla text-lg border-2 border-gray-600 text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                >
                  {t('view_investigation', lang)}
                </button>
                
                {verdict.status === 'mismatch' && (
                  <button 
                    onClick={() => router.push(`/share/${jobId}`)}
                    className="px-8 py-4 rounded-xl font-bold font-bangla text-lg bg-[#FF3B5C] text-white hover:bg-red-600 transition-colors shadow-[0_0_15px_rgba(255,59,92,0.4)]"
                  >
                    {t('share_rebuttal', lang)}
                  </button>
                )}
              </div>
            </motion.div>
          )}
        </div>
      )}
    </AnimatePresence>
  );
}
