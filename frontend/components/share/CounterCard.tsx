"use client";

import { useInvestigationStore } from "@/lib/store";

export default function CounterCard() {
  const verdict = useInvestigationStore(state => state.verdict);
  const evidence = useInvestigationStore(state => state.evidence);

  if (!verdict) return null;

  const visualFinding = evidence.find(e => e.finding.frame_ref);
  
  const getImageUrl = (frameRef: string) => {
    if (frameRef.startsWith('http')) return frameRef;
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const cleanRef = frameRef.startsWith('/') ? frameRef.slice(1) : frameRef;
    return `${baseUrl}/${cleanRef}`;
  };

  const frameUrl = visualFinding?.finding.frame_ref ? getImageUrl(visualFinding.finding.frame_ref) : '/fallback-frame.png';

  const isMismatch = verdict.status === 'mismatch';
  const themeColor = isMismatch ? 'text-alert' : 'text-truth';

  // Find a specific finding to use as snippet (e.g., from linguist or adjudicator)
  const snippet = evidence.length > 0 ? (evidence[evidence.length - 1].finding.description || evidence[evidence.length - 1].finding.value) : verdict.summary_en;

  return (
    <div 
      className="w-full max-w-[540px] mx-auto overflow-hidden flex flex-col relative rounded-2xl shadow-2xl border-4 border-[#13192A]"
      style={{ aspectRatio: '1/1' }}
      id="counter-card"
    >
      {/* Top Half: Video Thumbnail */}
      <div className="relative h-[50%] w-full bg-gray-900 border-b-4 border-alert overflow-hidden flex items-center justify-center">
        <img 
          src={frameUrl} 
          alt="Video frame" 
          className="w-full h-full object-cover opacity-60 mix-blend-screen grayscale"
          onError={(e) => { (e.target as HTMLImageElement).src = '/fallback-frame.png'; }}
        />
        
        {/* Banner */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="bg-alert text-white font-bangla font-black text-5xl px-10 py-4 rotate-[-5deg] border-4 border-white shadow-[0_10px_30px_rgba(255,59,92,0.6)] uppercase tracking-wide">
            {isMismatch ? 'মিথ্যা প্রসঙ্গ' : 'সত্যতা নিশ্চিত'}
          </div>
        </div>
      </div>

      {/* Bottom Half */}
      <div className="h-[50%] w-full bg-[#13192A] p-8 flex flex-col justify-between relative">
        <div className="flex flex-col gap-3">
          <h2 className={`text-3xl font-bangla font-black ${themeColor} leading-tight`}>
            {isMismatch ? 'দাবিটি ভুয়া!' : 'দাবিটি সঠিক!'}
          </h2>
          
          <h3 className="text-xl font-bangla font-bold text-white leading-snug">
            {verdict.summary_bn}
          </h3>
          
          <div className="pl-4 border-l-4 border-primary mt-3 bg-[#0A0E1A]/50 p-3 rounded-r-lg">
            <p className="text-gray-400 font-sans text-sm italic line-clamp-2">
              {snippet}
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center font-bold text-white text-xl shadow-[0_0_15px_rgba(61,139,255,0.5)]">
              O
            </div>
            <div>
              <p className="font-black text-white text-xl leading-none font-sans">OriginX</p>
              <p className="text-gray-500 text-[10px] font-mono tracking-[0.2em] mt-1">VERIFIED INTELLIGENCE</p>
            </div>
          </div>
          
          {verdict.confidence && (
            <div className="text-right">
              <p className="text-gray-500 text-[10px] font-mono mb-1 tracking-widest">CONFIDENCE</p>
              <p className={`font-black text-2xl font-mono ${themeColor}`}>
                {Math.round(verdict.confidence * 100)}%
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
