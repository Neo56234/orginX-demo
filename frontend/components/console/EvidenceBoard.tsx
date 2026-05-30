"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useInvestigationStore } from "@/lib/store";
import { t } from "@/lib/i18n";
import { useState } from "react";

export default function EvidenceBoard() {
  const evidence = useInvestigationStore(state => state.evidence);
  const lang = useInvestigationStore(state => state.language);
  const isComplete = useInvestigationStore(state => state.verdict !== null);
  const [selectedImg, setSelectedImg] = useState<string | null>(null);

  // Filter evidence to only those with a frame_ref
  const visualEvidence = evidence.filter(e => e.finding.frame_ref);

  const getAgentColor = (agentId: string) => {
    switch(agentId) {
      case 'geolocator': return 'bg-blue-900 text-blue-200 border-blue-500/50';
      case 'chronologist': return 'bg-purple-900 text-purple-200 border-purple-500/50';
      case 'tracer': return 'bg-orange-900 text-orange-200 border-orange-500/50';
      case 'linguist': return 'bg-emerald-900 text-emerald-200 border-emerald-500/50';
      case 'adjudicator': return 'bg-gray-700 text-gray-200 border-gray-500/50';
      default: return 'bg-gray-800 text-gray-300 border-gray-600';
    }
  };

  const getAgentEmoji = (agentId: string) => {
    switch(agentId) {
      case 'geolocator': return '🌍';
      case 'chronologist': return '🕐';
      case 'tracer': return '🔍';
      case 'linguist': return '🗣️';
      case 'adjudicator': return '⚖️';
      default: return '🤖';
    }
  };

  const getImageUrl = (frameRef: string) => {
    if (frameRef.startsWith('http')) return frameRef;
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    // Remove leading slash if present
    const cleanRef = frameRef.startsWith('/') ? frameRef.slice(1) : frameRef;
    return `${baseUrl}/${cleanRef}`;
  };

  return (
    <div className="w-full max-w-7xl mx-auto mt-12 bg-card/30 rounded-2xl border border-gray-800 p-6">
      <h3 className="text-xl font-bold font-sans text-foreground mb-6">
        {lang === 'bn' ? 'প্রমাণ বোর্ড' : 'Evidence Board'}
      </h3>

      {visualEvidence.length === 0 ? (
        <div className="flex items-center justify-center h-48 border-2 border-dashed border-gray-800 rounded-xl">
          <motion.p 
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-gray-500 font-bangla text-lg"
          >
            {isComplete 
              ? (lang === 'bn' ? 'কোনো ভিজ্যুয়াল প্রমাণ পাওয়া যায়নি' : 'No visual evidence found')
              : t('investigating', lang)
            }
          </motion.p>
        </div>
      ) : (
        <motion.div layout className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
          <AnimatePresence>
            {visualEvidence.map((ev) => (
              <motion.div
                key={ev.id}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
                onClick={() => setSelectedImg(getImageUrl(ev.finding.frame_ref!))}
                className="bg-card rounded-xl overflow-hidden border border-gray-800 group hover:border-primary transition-colors cursor-pointer flex flex-col"
              >
                <div className="relative aspect-video w-full bg-gray-900 overflow-hidden">
                  <img
                    src={getImageUrl(ev.finding.frame_ref!)}
                    alt="Evidence Frame"
                    className="object-cover w-full h-full opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = '/fallback-frame.png'; // Make sure you have a fallback if API fails
                    }}
                  />
                  <div className="absolute top-2 left-2 flex gap-2">
                    <span className={`text-xs px-2 py-1 rounded font-sans font-bold flex items-center gap-1 shadow-lg border ${getAgentColor(ev.agent)}`}>
                      {getAgentEmoji(ev.agent)} {ev.agent.charAt(0).toUpperCase() + ev.agent.slice(1)}
                    </span>
                  </div>
                  {ev.finding.confidence && (
                    <div className="absolute bottom-2 right-2 bg-black/80 backdrop-blur-sm text-xs px-2 py-1 rounded text-primary font-mono shadow-lg border border-primary/30">
                      {Math.round(ev.finding.confidence * 100)}%
                    </div>
                  )}
                </div>
                <div className="p-4 flex-1 flex items-center">
                  <p className="text-sm text-gray-300 font-sans line-clamp-3">
                    {ev.finding.description || ev.finding.value}
                  </p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      )}

      {/* Full Screen Modal */}
      <AnimatePresence>
        {selectedImg && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedImg(null)}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4 cursor-zoom-out backdrop-blur-sm"
          >
            <motion.img 
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              src={selectedImg} 
              alt="Evidence Full" 
              className="max-w-full max-h-full rounded-lg shadow-2xl border border-gray-700" 
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
