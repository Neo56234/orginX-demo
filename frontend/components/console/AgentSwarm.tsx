"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { useInvestigationStore, AgentName } from "@/lib/store";
import { useSSE } from "@/lib/sse";
import AgentCard from "./AgentCard";
import { t } from "@/lib/i18n";
import { isDemoId } from "@/lib/demo-config";
import { DEMO_INVESTIGATIONS } from "@/lib/demo-data";

function useDemoPlayback(demoId: string | null, handler: (event: string, data: any) => void) {
  useEffect(() => {
    if (!demoId || !isDemoId(demoId)) return;
    const demo = DEMO_INVESTIGATIONS[demoId];
    if (!demo) return;

    const SPEED = 2.2; // slow down factor — makes agent thinking readable
    const timers: ReturnType<typeof setTimeout>[] = [];
    demo.events.forEach(({ delayMs, event, data }) => {
      timers.push(setTimeout(() => handler(event, data), delayMs * SPEED));
    });
    return () => timers.forEach(clearTimeout);
  }, [demoId]); // eslint-disable-line react-hooks/exhaustive-deps
}

export default function AgentSwarm() {
  const currentJobId = useInvestigationStore(state => state.currentJobId);
  const agents = useInvestigationStore(state => state.agents);
  const handleSSEEvent = useInvestigationStore(state => state.handleSSEEvent);
  const lang = useInvestigationStore(state => state.language);
  const verdict = useInvestigationStore(state => state.verdict);

  const isDemo = currentJobId ? isDemoId(currentJobId) : false;

  const streamUrl = currentJobId && currentJobId !== 'starting' && !verdict && !isDemo
    ? `/api/stream/${currentJobId}`
    : null;

  useSSE(streamUrl, handleSSEEvent);
  useDemoPlayback(isDemo ? currentJobId : null, handleSSEEvent);

  const AGENTS: { id: AgentName; emoji: string; nameKey: any; roleKey: any }[] = [
    { id: "geolocator",   emoji: "🌍", nameKey: "agent_geolocator_name",   roleKey: "agent_geolocator_role" },
    { id: "chronologist", emoji: "🕐", nameKey: "agent_chronologist_name", roleKey: "agent_chronologist_role" },
    { id: "tracer",       emoji: "🔍", nameKey: "agent_tracer_name",       roleKey: "agent_tracer_role" },
    { id: "linguist",     emoji: "🗣️", nameKey: "agent_linguist_name",     roleKey: "agent_linguist_role" },
    { id: "adjudicator",  emoji: "⚖️", nameKey: "agent_adjudicator_name",  roleKey: "agent_adjudicator_role" },
  ];

  return (
    <div className="w-full max-w-7xl mx-auto mt-8">
      <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-5 gap-4">
        {AGENTS.map((agent, i) => (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1, duration: 0.5, ease: "easeOut" }}
          >
            <AgentCard 
              id={agent.id}
              emoji={agent.emoji}
              name={t(agent.nameKey, lang)}
              role={t(agent.roleKey, lang)}
              state={agents[agent.id]}
            />
          </motion.div>
        ))}
      </div>
    </div>
  );
}
