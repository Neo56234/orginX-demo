"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { useInvestigationStore } from "@/lib/store";
import { getInvestigation } from "@/lib/api";
import { isDemoId } from "@/lib/demo-config";
import { DEMO_INVESTIGATIONS } from "@/lib/demo-data";
import AgentSwarm from "@/components/console/AgentSwarm";
import EvidenceBoard from "@/components/console/EvidenceBoard";
import Timeline from "@/components/console/Timeline";
import MapView from "@/components/console/MapView";
import VerdictCard from "@/components/console/VerdictCard";
import SimilarCases from "@/components/console/SimilarCases";
import ReachCounter from "@/components/console/ReachCounter";

export default function InvestigationPage() {
  const params = useParams();
  const id = params.id as string;
  const reset = useInvestigationStore(state => state.reset);
  const [, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    // Demo mode: skip API, let AgentSwarm playback handle the events
    if (isDemoId(id)) {
      const demo = DEMO_INVESTIGATIONS[id];
      useInvestigationStore.setState({
        currentJobId: id,
        claimedDate: demo?.claimedDate ?? null,
        verdict: null,
      });
      setLoading(false);
      return () => { reset(); };
    }

    let isMounted = true;

    async function checkStatus() {
      try {
        const data = await getInvestigation(id);
        if (!isMounted) return;

        const claimedDate = data.claimed_date ? String(data.claimed_date) : null;

        if (data.status === 'complete' || data.verdict) {
           useInvestigationStore.setState({
             currentJobId: id,
             claimedDate,
             verdict: typeof data.verdict === 'string' ? {
               status: data.verdict,
               confidence: data.confidence,
               summary_bn: data.summary_bn,
               summary_en: data.summary_en,
               actual_origin_country: data.actual_origin_country,
               actual_origin_city: data.actual_origin_city,
               actual_origin_date: data.actual_origin_date ? String(data.actual_origin_date) : undefined,
             } as any : data.verdict,
           });
        } else {
           useInvestigationStore.setState({ currentJobId: id, claimedDate });
        }
      } catch (err) {
        useInvestigationStore.setState({ currentJobId: id });
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    checkStatus();

    return () => {
      isMounted = false;
      reset();
    };
  }, [id, reset]);

  return (
    <main className="min-h-screen bg-background p-4 md:p-8 pb-24">
      <div className="max-w-7xl mx-auto flex items-center justify-between mb-8 gap-3">
        <h1 className="text-2xl md:text-3xl font-black text-white tracking-widest font-sans cursor-pointer hover:opacity-80 shrink-0" onClick={() => window.location.href='/'}>
          Origin<span className="text-primary">X</span>
        </h1>
        <div className="flex gap-2 md:gap-4 items-center min-w-0">
          <a href="/dashboard" className="text-gray-400 hover:text-white font-mono text-xs md:text-sm px-3 md:px-4 py-1 border border-gray-800 rounded-full bg-card transition-colors shrink-0">
            Viral Monitor
          </a>
          <div className="text-gray-500 font-mono text-[10px] md:text-sm px-2 md:px-4 py-1 border border-gray-800 rounded-full bg-card truncate max-w-[120px] md:max-w-none">
            {id.startsWith('demo-') ? id : `ID: ${id.slice(0, 8)}…`}
          </div>
        </div>
      </div>

      <AgentSwarm />
      <EvidenceBoard />
      <Timeline />
      <MapView />
      <VerdictCard />
      <ReachCounter investigationId={id} />
      <SimilarCases investigationId={id} />
    </main>
  );
}
