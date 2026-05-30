"use client";

import URLInput from "@/components/console/URLInput";
import { useInvestigationStore } from "@/lib/store";
import { t } from "@/lib/i18n";
import { DEMO_INVESTIGATIONS } from "@/lib/demo-data";
import { DEMO_MODE } from "@/lib/demo-config";

const DEMO_VERDICT_STYLE = {
  mismatch: { color: "text-alert", bg: "bg-alert/10 border-alert/25", label: "MISMATCH" },
  authentic: { color: "text-truth", bg: "bg-truth/10 border-truth/25", label: "AUTHENTIC" },
};

export default function Home() {
  const lang = useInvestigationStore(state => state.language);
  const demos = Object.values(DEMO_INVESTIGATIONS);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24 bg-background relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="absolute top-6 right-6 z-50 flex gap-3 items-center">
        <a href="/chat" className="text-gray-400 hover:text-white font-mono text-sm transition-colors bg-card px-4 py-2 rounded-full border border-gray-800">
          Knowledge Base
        </a>
        <a href="/dashboard" className="text-gray-400 hover:text-white font-mono text-sm transition-colors bg-card px-4 py-2 rounded-full border border-gray-800">
          Viral Monitor
        </a>
        <div className="flex bg-gray-900 rounded-full p-1 border border-gray-700">
          <button
            onClick={() => useInvestigationStore.getState().setLanguage('en')}
            className={`px-3 py-1 rounded-full text-xs font-bold font-sans transition-colors ${lang === 'en' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'}`}
          >
            EN
          </button>
          <button
            onClick={() => useInvestigationStore.getState().setLanguage('bn')}
            className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${lang === 'bn' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'}`}
          >
            বাং
          </button>
        </div>
      </div>

      <div className="z-10 w-full max-w-4xl text-center flex flex-col items-center">
        <h1 className="text-5xl md:text-7xl font-sans font-black text-transparent bg-clip-text bg-gradient-to-r from-primary via-white to-primary mb-6 animate-pulse">
          OriginX
        </h1>
        <p className={`text-lg md:text-xl text-gray-400 mb-12 max-w-2xl text-balance ${lang === 'bn' ? 'font-bangla' : 'font-sans'}`}>
          {t('hero_subtitle', lang)}
        </p>

        <URLInput />

        {/* Demo Mode Notice */}
        {DEMO_MODE && (
          <div className="w-full mt-8 rounded-2xl border border-primary/25 bg-primary/5 backdrop-blur p-4 md:p-5 text-left">
            <div className="flex items-start gap-3">
              <span className="relative flex h-2.5 w-2.5 mt-1.5 shrink-0">
                <span className="absolute inline-flex h-full w-full rounded-full bg-primary opacity-60 animate-ping" />
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-primary" />
              </span>
              <div className="flex-1">
                <p className="text-[10px] font-mono tracking-[0.18em] uppercase text-primary/90 mb-1">
                  Live Demo Mode · Active
                </p>
                <p className="text-sm text-white/75 leading-relaxed">
                  This instance is running in showcase mode. Three pre-verified investigations are loaded below — each one runs the full five-agent pipeline end-to-end against pre-indexed evidence, completing in roughly three seconds. Select any case to watch the verdict assemble in real time.
                </p>
                <p className="text-sm text-white/60 leading-relaxed mt-2">
                  Also try the <a href="/chat" className="text-primary hover:text-white underline underline-offset-2 decoration-primary/40 hover:decoration-white transition-colors">Knowledge Base chatbot</a> and the <a href="/dashboard" className="text-primary hover:text-white underline underline-offset-2 decoration-primary/40 hover:decoration-white transition-colors">Viral Monitor</a>.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Demo Cases */}
        <div className="w-full mt-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-px flex-1 bg-white/5" />
            <span className="text-white/25 font-mono text-[11px] tracking-widest uppercase">Pre-verified investigations</span>
            <div className="h-px flex-1 bg-white/5" />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {demos.map((demo) => {
              const style = DEMO_VERDICT_STYLE[demo.expectedVerdict];
              return (
                <a
                  key={demo.id}
                  href={`/investigation/${demo.id}`}
                  className={`group relative rounded-2xl border p-4 text-left flex flex-col gap-3 transition-all hover:-translate-y-0.5 bg-card/40 backdrop-blur hover:bg-card/60 ${style.bg}`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-2xl leading-none">{demo.thumbnail}</span>
                    <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${style.bg} ${style.color}`}>
                      {style.label} · {Math.round(demo.expectedConfidence * 100)}%
                    </span>
                  </div>
                  <div>
                    <p className="text-white/80 text-xs leading-relaxed line-clamp-2">{demo.labelEn}</p>
                    <p className="text-white/30 text-[10px] font-mono mt-1 truncate">{demo.claim}</p>
                  </div>
                  <div className="mt-auto flex items-center gap-1 text-white/30 group-hover:text-white/60 transition-colors">
                    <span className="text-[10px] font-mono">Watch investigation live</span>
                    <span className="text-[10px]">→</span>
                  </div>
                </a>
              );
            })}
          </div>
        </div>
      </div>
    </main>
  );
}
