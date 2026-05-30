import { DEMO_MODE } from './demo-config';
import { DEMO_DASHBOARD } from './demo-data';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AnalyzeResponse {
  investigation_id: string;
  stream_url: string;
  share_url: string;
}

export async function analyzeVideo(url: string, claimedContext?: string): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ video_url: url, claimed_context: claimedContext || "" }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to start investigation');
  }

  return response.json();
}

export async function analyzeUpload(file: File, claimedContext?: string): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append('video', file);
  if (claimedContext) {
    formData.append('claimed_context', claimedContext);
  }

  const response = await fetch(`${API_BASE_URL}/api/analyze/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to upload and start investigation');
  }

  return response.json();
}

export async function getInvestigation(id: string) {
  const response = await fetch(`${API_BASE_URL}/api/investigation/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch investigation');
  }
  return response.json();
}

export async function getCases(query?: string) {
  const url = query ? `${API_BASE_URL}/api/cases?q=${encodeURIComponent(query)}` : `${API_BASE_URL}/api/cases`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch cases');
  }
  return response.json();
}

export async function getViralFeed() {
  if (DEMO_MODE) return DEMO_DASHBOARD.viralFeed;
  const response = await fetch(`${API_BASE_URL}/api/dashboard/viral`);
  if (!response.ok) throw new Error('Failed to fetch viral feed');
  return response.json();
}

export async function getViralStats() {
  if (DEMO_MODE) return DEMO_DASHBOARD.stats;
  const response = await fetch(`${API_BASE_URL}/api/dashboard/stats`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
}

export async function getTrustGraph() {
  if (DEMO_MODE) return DEMO_DASHBOARD.trustGraph;
  const response = await fetch(`${API_BASE_URL}/api/dashboard/trust-graph`);
  if (!response.ok) throw new Error('Failed to fetch trust graph');
  return response.json();
}

export async function getCampaigns() {
  if (DEMO_MODE) return DEMO_DASHBOARD.campaigns;
  const response = await fetch(`${API_BASE_URL}/api/dashboard/campaigns`);
  if (!response.ok) throw new Error('Failed to fetch campaigns');
  return response.json();
}

export async function getCredibilityLeaderboard(limit = 10) {
  if (DEMO_MODE) return DEMO_DASHBOARD.leaderboard.slice(0, limit);
  const response = await fetch(`${API_BASE_URL}/api/dashboard/credibility-leaderboard?limit=${limit}`);
  if (!response.ok) throw new Error('Failed to fetch leaderboard');
  return response.json();
}
