import { create } from 'zustand';
import { Language } from './i18n';

export type AgentName = 'geolocator' | 'chronologist' | 'tracer' | 'linguist' | 'adjudicator';

export interface Finding {
  type: string;
  value?: string;
  description?: string;
  confidence?: number;
  frame_ref?: string;
  weight?: string;
}

export interface AgentState {
  status: 'idle' | 'running' | 'complete' | 'failed';
  progress: number; // 0.0 to 1.0
  findings: Finding[];
  error: string | null;
  statusText: string; // live progress label from backend
}

export interface Evidence {
  id: string;
  agent: AgentName;
  finding: Finding;
  timestamp: number;
}

export interface KeyEvidence {
  agent: string;
  finding: string;
  weight: 'high' | 'medium' | 'low';
}

export interface Verdict {
  status: 'authentic' | 'mismatch' | 'insufficient_evidence';
  confidence: number;
  summary_bn: string;
  summary_en: string;
  actual_origin_country?: string;
  actual_origin_city?: string;
  actual_origin_date?: string; // YYYY-MM-DD from adjudicator actual_origin.earliest_date
  key_evidence?: KeyEvidence[];
}

const blankAgent: AgentState = { status: 'idle', progress: 0, findings: [], error: null, statusText: '' };

const initialAgentsState: Record<AgentName, AgentState> = {
  geolocator:   { ...blankAgent },
  chronologist: { ...blankAgent },
  tracer:       { ...blankAgent },
  linguist:     { ...blankAgent },
  adjudicator:  { ...blankAgent },
};

export interface InvestigationStore {
  currentJobId: string | null;
  claimedDate: string | null; // parsed from user's claim text, set on initial fetch
  agents: Record<AgentName, AgentState>;
  evidence: Evidence[];
  verdict: Verdict | null;
  language: Language;
  
  startInvestigation: (url: string) => Promise<void>;
  handleSSEEvent: (event: string, data: any) => void;
  setLanguage: (lang: Language) => void;
  reset: () => void;
}

export const useInvestigationStore = create<InvestigationStore>((set) => ({
  currentJobId: null,
  claimedDate: null,
  agents: initialAgentsState,
  evidence: [],
  verdict: null,
  language: 'bn',

  startInvestigation: async (url: string) => {
    // API logic will be implemented in Step 4.
    set({
      currentJobId: 'starting',
      agents: {
        geolocator:   { ...blankAgent },
        chronologist: { ...blankAgent },
        tracer:       { ...blankAgent },
        linguist:     { ...blankAgent },
        adjudicator:  { ...blankAgent },
      },
      evidence: [],
      verdict: null
    });
  },

  handleSSEEvent: (event: string, data: any) => {
    set((state) => {
      // If it's a global investigation complete event
      if (event === 'investigation_complete') {
        const raw = data.data?.verdict || data.verdict;
        if (!raw) return state;
        return {
          ...state,
          verdict: {
            status: raw.verdict ?? raw.status,
            confidence: raw.confidence,
            summary_bn: raw.summary_bn,
            summary_en: raw.summary_en,
            actual_origin_country: raw.actual_origin?.country || raw.actual_origin_country,
            actual_origin_city: raw.actual_origin?.city || raw.actual_origin_city,
            actual_origin_date: raw.actual_origin?.earliest_date || raw.actual_origin_date || null,
            key_evidence: raw.key_evidence || [],
          }
        };
      }

      // Agent specific events
      if (!data || !data.agent) return state;
      const agentName = data.agent as AgentName;
      
      const updatedAgents = { ...state.agents };
      const agentState = { ...updatedAgents[agentName] };
      let newEvidence = [...state.evidence];

      switch (event) {
        case 'agent_started':
          agentState.status = 'running';
          agentState.progress = 0.1;
          break;
        case 'agent_progress':
          agentState.progress = data.data?.progress ?? data.progress ?? agentState.progress;
          if (data.data?.text) agentState.statusText = data.data.text;
          break;
        case 'agent_finding':
          const finding = data.data || data.finding || data; // handle depending on how it's sent
          if (finding && (finding.type || finding.description)) {
            agentState.findings = [...agentState.findings, finding];
            newEvidence.push({
              id: `${agentName}-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
              agent: agentName,
              finding: finding,
              timestamp: Date.now()
            });
          }
          break;
        case 'agent_complete':
          agentState.status = 'complete';
          agentState.progress = 1.0;
          break;
        case 'agent_failed':
          agentState.status = 'failed';
          agentState.error = data.data?.error || data.error || 'Failed';
          break;
      }
      
      updatedAgents[agentName] = agentState;
      return { ...state, agents: updatedAgents, evidence: newEvidence };
    });
  },

  setLanguage: (lang: Language) => set({ language: lang }),
  
  reset: () => set({
    currentJobId: null,
    claimedDate: null,
    agents: initialAgentsState,
    evidence: [],
    verdict: null
  })
}));
