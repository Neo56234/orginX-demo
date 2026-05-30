"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { getViralFeed, getViralStats, getTrustGraph, getCampaigns, getCredibilityLeaderboard } from "@/lib/api";
import TrustGraph from "@/components/dashboard/TrustGraph";

const CATEGORY_LABELS: Record<string, string> = {
  communal: "Communal",
  politics: "Politics",
  health: "Health",
  disaster: "Disaster",
};

const REGION_LABELS: Record<string, string> = {
  dhaka: "Dhaka",
  chittagong: "Chittagong",
  sylhet: "Sylhet",
  rajshahi: "Rajshahi",
  khulna: "Khulna",
  barisal: "Barisal",
  mymensingh: "Mymensingh",
  nationwide: "Nationwide",
};

const CATEGORY_COLORS: Record<string, string> = {
  communal: "bg-alert/10 text-alert border-alert/30",
  politics: "bg-warning/10 text-warning border-warning/30",
  health: "bg-primary/10 text-primary border-primary/30",
  disaster: "bg-purple-400/10 text-purple-400 border-purple-400/30",
};

function formatShareCount(n: number): string {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(0)}K`;
  return String(n);
}

function PulsingDot({ color = "bg-alert" }: { color?: string }) {
  return (
    <span className="relative flex h-2.5 w-2.5">
      <span className={`animate-ping absolute inline-flex h-full w-full rounded-full ${color} opacity-60`} />
      <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${color}`} />
    </span>
  );
}

function StatCard({ label, sublabel, value, color }: { label: string; sublabel: string; value: any; color: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative bg-card/60 backdrop-blur border border-white/5 rounded-2xl p-5 overflow-hidden group hover:border-white/10 transition-all"
    >
      <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl`}
        style={{ background: `radial-gradient(circle at 0% 0%, ${color}10 0%, transparent 60%)` }} />
      <div className="relative">
        <div className="text-3xl font-black font-mono mb-1" style={{ color }}>{value ?? "—"}</div>
        <div className="text-white/90 text-sm font-medium">{label}</div>
        <div className="text-white/30 text-xs mt-0.5">{sublabel}</div>
      </div>
    </motion.div>
  );
}

export default function DashboardPage() {
  const [videos, setVideos] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [graphData, setGraphData] = useState<{ nodes: any[]; edges: any[] }>({ nodes: [], edges: [] });
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [filter, setFilter] = useState({ category: "", region: "" });

  useEffect(() => {
    async function load() {
      try {
        const [feed, s, graph, camps, lb] = await Promise.all([
          getViralFeed(),
          getViralStats().catch(() => null),
          getTrustGraph().catch(() => ({ nodes: [], edges: [] })),
          getCampaigns().catch(() => []),
          getCredibilityLeaderboard().catch(() => []),
        ]);
        setVideos(feed);
        setStats(s);
        setGraphData(graph);
        setCampaigns(camps);
        setLeaderboard(lb);
      } catch (e) {
        console.error(e);
      }
    }
    load();
    const id = setInterval(load, 30000);
    return () => clearInterval(id);
  }, []);

  const filtered = videos.filter((v) => {
    if (filter.category && v.category !== filter.category) return false;
    if (filter.region && v.region !== filter.region) return false;
    return true;
  });

  const categories = ["", "communal", "politics", "health", "disaster"];
  const regions = ["", "dhaka", "chittagong", "sylhet", "nationwide"];

  return (
    <div className="min-h-screen bg-background text-white relative overflow-x-hidden">

      {/* Ambient glows — matching main page */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute top-[-200px] left-[-200px] w-[600px] h-[600px] rounded-full bg-primary/8 blur-[120px]" />
        <div className="absolute bottom-[-200px] right-[-200px] w-[500px] h-[500px] rounded-full bg-alert/6 blur-[120px]" />
      </div>

      {/* Nav */}
      <nav className="sticky top-0 z-40 border-b border-white/5 bg-background/70 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <a href="/" className="text-2xl font-black tracking-tight">
              Origin<span className="text-primary">X</span>
            </a>
            <div className="h-5 w-px bg-white/10" />
            <div className="flex items-center gap-2">
              <PulsingDot color="bg-alert" />
              <span className="text-alert font-mono text-xs font-bold tracking-widest uppercase">
                Viral Monitor
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <a href="/chat" className="text-white/40 hover:text-white font-mono text-xs transition-colors bg-white/5 hover:bg-white/10 px-4 py-2 rounded-full border border-white/5">
              Knowledge Base
            </a>
            <span className="text-white/20 font-mono text-xs">AUTO-REFRESH 30s</span>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8 relative">

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatCard label="Active Alerts" sublabel="Currently Monitoring" value={stats.total_viral} color="#FF3B5C" />
            <StatCard label="Confirmed Fake" sublabel="Mismatch Found" value={stats.total_mismatch} color="#FF3B5C" />
            <StatCard label="Confirmed Authentic" sublabel="No Issue Found" value={stats.total_authentic} color="#00D67E" />
            <StatCard
              label="Most Affected"
              sublabel="Region"
              value={REGION_LABELS[Object.entries(stats.by_region || {}).sort(([, a]: any, [, b]: any) => b - a)[0]?.[0]] || "—"}
              color="#FFB833"
            />
          </div>
        )}

        {/* Campaign Alert Banner */}
        <AnimatePresence>
          {campaigns.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="mb-6 p-4 bg-alert/5 border border-alert/20 rounded-2xl backdrop-blur"
            >
              <div className="flex items-center gap-3 mb-3">
                <PulsingDot color="bg-alert" />
                <span className="text-alert font-mono font-bold text-xs tracking-widest uppercase">
                  Coordinated Campaign Detected
                </span>
              </div>
              <div className="flex flex-col gap-2">
                {campaigns.map((c) => (
                  <div key={c.id} className="flex items-center justify-between bg-white/3 rounded-xl px-4 py-2.5 border border-white/5">
                    <span className="text-white/80 text-sm">{c.sample_claim_bn || "Unknown Campaign"}</span>
                    <span className="text-alert font-mono text-xs font-bold ml-4 whitespace-nowrap bg-alert/10 px-2 py-0.5 rounded-full border border-alert/20">
                      {c.investigation_count} sources
                    </span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2 mb-6">
          <div className="flex gap-2 flex-wrap">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setFilter((f) => ({ ...f, category: cat }))}
                className={`px-3.5 py-1.5 rounded-full text-xs font-mono border transition-all ${
                  filter.category === cat
                    ? "bg-primary text-white border-primary shadow-[0_0_12px_rgba(61,139,255,0.3)]"
                    : "border-white/10 text-white/40 hover:border-white/20 hover:text-white/70 bg-white/3"
                }`}
              >
                {cat ? CATEGORY_LABELS[cat] : "All"}
              </button>
            ))}
          </div>
          <div className="h-4 w-px bg-white/10 hidden md:block" />
          <div className="flex gap-2 flex-wrap">
            {regions.map((reg) => (
              <button
                key={reg}
                onClick={() => setFilter((f) => ({ ...f, region: reg }))}
                className={`px-3.5 py-1.5 rounded-full text-xs font-mono border transition-all ${
                  filter.region === reg
                    ? "bg-primary text-white border-primary shadow-[0_0_12px_rgba(61,139,255,0.3)]"
                    : "border-white/10 text-white/40 hover:border-white/20 hover:text-white/70 bg-white/3"
                }`}
              >
                {reg ? REGION_LABELS[reg] : "All Regions"}
              </button>
            ))}
          </div>
        </div>

        {/* Video Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <AnimatePresence mode="popLayout">
            {filtered.map((vid, i) => {
              const isHot = vid.share_count >= 500000;
              const hasVerdict = !!vid.investigation_id;
              return (
                <motion.div
                  key={vid.id}
                  layout
                  initial={{ opacity: 0, scale: 0.97 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.97 }}
                  transition={{ delay: i * 0.04 }}
                  className={`group relative bg-card/50 backdrop-blur rounded-2xl border flex flex-col gap-4 p-5 overflow-hidden transition-all hover:-translate-y-0.5 ${
                    isHot
                      ? "border-alert/25 shadow-[0_0_30px_rgba(255,59,92,0.08)] hover:shadow-[0_0_40px_rgba(255,59,92,0.14)]"
                      : "border-white/5 hover:border-white/10"
                  }`}
                >
                  {/* Subtle inner glow for hot videos */}
                  {isHot && (
                    <div className="absolute inset-0 bg-gradient-to-br from-alert/5 to-transparent rounded-2xl pointer-events-none" />
                  )}

                  {/* VIRAL badge */}
                  {isHot && (
                    <div className="absolute top-3 right-3 flex items-center gap-1.5 bg-alert/10 border border-alert/30 text-alert text-[10px] font-bold font-mono px-2.5 py-1 rounded-full">
                      <span className="w-1.5 h-1.5 rounded-full bg-alert animate-pulse inline-block" />
                      VIRAL
                    </div>
                  )}

                  {/* Share count + category */}
                  <div className="flex items-start justify-between relative">
                    <div>
                      <div className={`text-4xl font-black font-mono leading-none ${isHot ? "text-alert" : "text-warning"}`}>
                        {formatShareCount(vid.share_count || 0)}
                      </div>
                      <div className="text-white/30 text-xs mt-1 font-mono">shares</div>
                    </div>
                    {vid.category && (
                      <span className={`text-[10px] font-mono px-2.5 py-1 rounded-full border mt-1 ${
                        CATEGORY_COLORS[vid.category] || "bg-white/5 text-white/40 border-white/10"
                      }`}>
                        {CATEGORY_LABELS[vid.category] || vid.category}
                      </span>
                    )}
                  </div>

                  {/* Claim text */}
                  <p className="text-white/80 text-sm leading-relaxed line-clamp-3 relative">
                    {vid.claim_text || vid.claim_text_bn}
                  </p>

                  {/* Region */}
                  {vid.region && (
                    <div className="flex items-center gap-1.5 relative">
                      <span className="text-white/20 text-xs">📍</span>
                      <span className="text-white/30 text-xs font-mono">
                        {REGION_LABELS[vid.region] || vid.region}
                      </span>
                    </div>
                  )}

                  {/* Action */}
                  <div className="mt-auto pt-3 border-t border-white/5 relative">
                    {hasVerdict ? (
                      <a
                        href={`/investigation/${vid.investigation_id}`}
                        className="flex items-center justify-center gap-2 w-full bg-truth/10 text-truth border border-truth/20 text-xs font-mono py-2.5 rounded-xl hover:bg-truth/15 transition-all"
                      >
                        <span className="w-1.5 h-1.5 rounded-full bg-truth inline-block" />
                        View Verdict
                      </a>
                    ) : (
                      <a
                        href={vid.video_url ? `/?url=${encodeURIComponent(vid.video_url)}` : "/"}
                        className="flex items-center justify-center gap-2 w-full bg-primary/10 text-primary border border-primary/20 text-xs font-mono py-2.5 rounded-xl hover:bg-primary/15 transition-all group-hover:border-primary/35"
                      >
                        Investigate
                        <span className="opacity-60">→</span>
                      </a>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>

        {/* Empty state */}
        {filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center py-32 text-center">
            <div className="w-16 h-16 rounded-full bg-white/3 border border-white/5 flex items-center justify-center mb-4">
              <span className="text-white/20 text-2xl">⬡</span>
            </div>
            <p className="text-white/20 font-mono text-sm">No videos found</p>
            <p className="text-white/10 font-mono text-xs mt-1">Try changing the filters</p>
          </div>
        )}

        {/* Source Credibility Leaderboard */}
        {leaderboard.length > 0 && (
          <div className="mt-16">
            <div className="flex items-center gap-3 mb-6">
              <div className="h-px flex-1 bg-white/5" />
              <div className="flex items-center gap-2">
                <span className="text-alert text-sm">⚠</span>
                <h2 className="text-white/50 font-mono text-xs tracking-widest uppercase">Unreliable Source Leaderboard</h2>
              </div>
              <div className="h-px flex-1 bg-white/5" />
            </div>
            <div className="bg-card/40 backdrop-blur border border-white/5 rounded-2xl overflow-hidden">
              <div className="grid grid-cols-[auto_1fr_auto] md:grid-cols-[auto_1fr_auto_auto_auto] gap-0 text-[10px] font-mono text-white/30 uppercase tracking-widest px-4 md:px-5 py-3 border-b border-white/5">
                <span className="w-7 md:w-8">#</span>
                <span>Source</span>
                <span className="hidden md:block w-24 text-right">Total Shared</span>
                <span className="hidden md:block w-24 text-right">Flagged</span>
                <span className="w-20 text-right">Flag Rate</span>
              </div>
              <AnimatePresence>
                {leaderboard.map((s, i) => (
                  <motion.div
                    key={s.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="grid grid-cols-[auto_1fr_auto] md:grid-cols-[auto_1fr_auto_auto_auto] gap-0 items-center px-4 md:px-5 py-3 md:py-3.5 border-b border-white/5 last:border-0 hover:bg-white/2 transition-colors"
                  >
                    <span className="w-7 md:w-8 text-white/20 font-mono text-sm font-bold">{i + 1}</span>
                    <div className="min-w-0">
                      <div className="text-white/80 text-sm font-medium truncate">{s.display_name}</div>
                      <div className="text-white/20 text-[10px] font-mono truncate">{s.platform} · <span className="hidden sm:inline">{s.source_identifier}</span><span className="sm:hidden">{s.flagged_count.toLocaleString()} flagged</span></div>
                    </div>
                    <span className="hidden md:block w-24 text-right font-mono text-white/40 text-xs">{s.total_shared.toLocaleString()}</span>
                    <span className="hidden md:block w-24 text-right font-mono text-alert text-xs font-bold">{s.flagged_count.toLocaleString()}</span>
                    <span className="w-20 text-right">
                      <span className={`font-mono text-xs font-bold px-2 py-0.5 rounded-full ${
                        s.flag_rate >= 50 ? "bg-alert/15 text-alert" :
                        s.flag_rate >= 20 ? "bg-warning/15 text-warning" :
                        "bg-white/5 text-white/30"
                      }`}>{s.flag_rate}%</span>
                    </span>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </div>
        )}

        {/* Trust Network */}
        {graphData.nodes.length > 0 && (
          <div className="mt-16">
            <div className="flex items-center gap-3 mb-6">
              <div className="h-px flex-1 bg-white/5" />
              <h2 className="text-white/50 font-mono text-xs tracking-widest uppercase">Source Trust Network</h2>
              <div className="h-px flex-1 bg-white/5" />
            </div>
            <div className="bg-card/40 backdrop-blur border border-white/5 rounded-2xl overflow-hidden">
              <TrustGraph nodes={graphData.nodes} edges={graphData.edges} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
