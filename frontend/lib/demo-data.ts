export interface DemoEvent {
  delayMs: number;
  event: string;
  data: any;
}

export interface DemoInvestigation {
  id: string;
  label: string;
  labelEn: string;
  category: string;
  thumbnail: string;
  claim: string;
  claimedDate: string;
  expectedVerdict: 'mismatch' | 'authentic';
  expectedConfidence: number;
  events: DemoEvent[];
  reach: { base_shares: number; estimated_reach: number | null; network_multiplier: number; amplification: number; verdict: string };
  similarCases: any[];
}

// ─── Demo 1: Pakistan PTI Protest → claimed as BD student protest ────────────
const PAKISTAN_PROTEST: DemoInvestigation = {
  id: 'demo-pakistan-protest',
  label: 'পাকিস্তানের ভিডিও বাংলাদেশের দাবিতে',
  labelEn: 'Pakistan footage claimed as Bangladesh protest',
  category: 'politics',
  thumbnail: '🇵🇰',
  claim: 'Bangladesh student protest 2024 — police crackdown on quota reform demonstrators in Dhaka',
  claimedDate: '2024-07-15',
  expectedVerdict: 'mismatch',
  expectedConfidence: 0.94,
  events: [
    { delayMs: 0,    event: 'agent_started',  data: { agent: 'geolocator' } },
    { delayMs: 400,  event: 'agent_progress', data: { agent: 'geolocator', data: { progress: 0.3, text: 'Extracting GPS metadata from video frames...' } } },
    { delayMs: 900,  event: 'agent_finding',  data: { agent: 'geolocator', data: { type: 'metadata', description: 'No embedded GPS data found. Switching to visual landmark analysis.', confidence: 0.6 } } },
    { delayMs: 1500, event: 'agent_finding',  data: { agent: 'geolocator', data: { type: 'visual_landmark', description: 'Urban crowd scene — road signs and building architecture consistent with South Asian setting, non-specific.', confidence: 0.55 } } },
    { delayMs: 2000, event: 'agent_complete', data: { agent: 'geolocator' } },

    { delayMs: 2100, event: 'agent_started',  data: { agent: 'linguist' } },
    { delayMs: 2500, event: 'agent_progress', data: { agent: 'linguist', data: { progress: 0.35, text: 'Scanning all visible text overlays in video frames...' } } },
    { delayMs: 3100, event: 'agent_finding',  data: { agent: 'linguist', data: { type: 'script_detection', description: 'Urdu script detected in lower-third text banner — Urdu is not used in Bangladesh (uses Bengali script only)', confidence: 0.97, weight: 'high' } } },
    { delayMs: 3800, event: 'agent_finding',  data: { agent: 'linguist', data: { type: 'watermark', description: 'GEO NEWS watermark visible in top-right corner at 0:04 — GEO is a Pakistan-based television network', confidence: 0.95, weight: 'high' } } },
    { delayMs: 4400, event: 'agent_complete', data: { agent: 'linguist' } },

    { delayMs: 4500, event: 'agent_started',  data: { agent: 'tracer' } },
    { delayMs: 4900, event: 'agent_progress', data: { agent: 'tracer', data: { progress: 0.3, text: 'Running reverse image search on 6 keyframes...' } } },
    { delayMs: 5600, event: 'agent_finding',  data: { agent: 'tracer', data: { type: 'source_match', description: 'Exact match: GEO TV Pakistan broadcast — PTI anti-government rally in Lahore, November 5, 2023', confidence: 0.93, weight: 'high' } } },
    { delayMs: 6300, event: 'agent_finding',  data: { agent: 'tracer', data: { type: 'fact_check', description: 'Previously debunked by AFP Bangladesh and Rumor Scanner (November 2023)', confidence: 0.91, weight: 'high' } } },
    { delayMs: 6900, event: 'agent_complete', data: { agent: 'tracer' } },

    { delayMs: 7000, event: 'agent_started',  data: { agent: 'chronologist' } },
    { delayMs: 7400, event: 'agent_progress', data: { agent: 'chronologist', data: { progress: 0.5, text: 'Cross-referencing event dates with claimed context...' } } },
    { delayMs: 7900, event: 'agent_finding',  data: { agent: 'chronologist', data: { type: 'date_mismatch', description: 'Original event: November 2023 (Lahore, Pakistan) — Claimed: July 2024 Bangladesh protest. 8-month temporal gap confirmed.', confidence: 0.91, weight: 'high' } } },
    { delayMs: 8400, event: 'agent_complete', data: { agent: 'chronologist' } },

    { delayMs: 8500, event: 'agent_started',  data: { agent: 'adjudicator' } },
    { delayMs: 8900, event: 'agent_progress', data: { agent: 'adjudicator', data: { progress: 0.4, text: 'Weighing 4 high-confidence findings...' } } },
    { delayMs: 9500, event: 'agent_progress', data: { agent: 'adjudicator', data: { progress: 0.82, text: 'Urdu script + GEO News watermark + verified source match = definitive mismatch' } } },
    { delayMs: 10200, event: 'agent_complete', data: { agent: 'adjudicator' } },
    {
      delayMs: 10500,
      event: 'investigation_complete',
      data: { data: { verdict: {
        verdict: 'mismatch',
        confidence: 0.94,
        summary_bn: 'এটি পাকিস্তানের লাহোরে PTI সমর্থকদের সমাবেশের ভিডিও। ভিডিওতে উর্দু লিপি এবং GEO News পাকিস্তানের watermark স্পষ্ট দেখা যাচ্ছে। মূল ঘটনা নভেম্বর ২০২৩ সালের — বাংলাদেশের জুলাই ২০২৪ আন্দোলনের সাথে এর কোনো সম্পর্ক নেই।',
        summary_en: 'This video is from a PTI political rally in Lahore, Pakistan (November 2023). Urdu script and GEO News Pakistan watermark are clearly visible. The footage is unrelated to the July 2024 Bangladesh quota protest movement.',
        actual_origin: { country: 'Pakistan', city: 'Lahore', earliest_date: '2023-11-05' },
        key_evidence: [
          { agent: 'linguist',      finding: 'Urdu script detected in banner — not used in Bangladesh', weight: 'high' },
          { agent: 'linguist',      finding: 'GEO NEWS Pakistan watermark visible at 0:04',             weight: 'high' },
          { agent: 'tracer',        finding: 'Original source: GEO TV broadcast, Lahore Nov 2023',       weight: 'high' },
          { agent: 'chronologist',  finding: '8-month date discrepancy confirmed',                        weight: 'high' },
        ],
      } } },
    },
  ],
  reach: { base_shares: 847000, estimated_reach: 23716000, network_multiplier: 7, amplification: 4.0, verdict: 'mismatch' },
  similarCases: [
    { id: 101, title_en: 'Pakistan police crackdown on PTI shared as Bangladesh protest footage', title_bn: 'পাকিস্তানে PTI দমনের ভিডিও বাংলাদেশের আন্দোলনের দাবিতে', false_claim_en: 'Pakistan PTI crackdown footage shared as Bangladesh student protest', actual_origin_country: 'Pakistan', actual_origin_city: 'Islamabad', actual_origin_date: '2023-08-05', debunk_url: 'https://www.afp.com/fact-check', debunk_source: 'AFP Bangladesh' },
    { id: 102, title_en: 'Geo News Pakistan broadcast shown as live Bangladesh news', title_bn: 'জিও নিউজের সম্প্রচার বাংলাদেশের খবর হিসেবে প্রচার', false_claim_en: 'Pakistan Geo News broadcast shown as Bangladesh live coverage', actual_origin_country: 'Pakistan', actual_origin_city: 'Karachi', actual_origin_date: '2023-09-12', debunk_url: 'https://www.somoy.com/fact-check', debunk_source: 'Rumor Scanner' },
    { id: 103, title_en: 'Pakistani mosque attack shared as Hindu temple attack in Bangladesh', title_bn: 'পাকিস্তানের মসজিদ হামলার ভিডিও বাংলাদেশে হিন্দু মন্দির হামলার দাবিতে', false_claim_en: 'Pakistan mosque attack video shared as Hindu temple attack in Bangladesh', actual_origin_country: 'Pakistan', actual_origin_city: 'Peshawar', actual_origin_date: '2023-07-30', debunk_url: 'https://www.bdfact.com', debunk_source: 'Bangladesh Fact Check' },
  ],
};

// ─── Demo 2: India Kerala Flood → claimed as Bangladesh 2024 flood ────────────
const INDIA_FLOOD: DemoInvestigation = {
  id: 'demo-india-flood',
  label: 'ভারতের বন্যার ভিডিও বাংলাদেশের দাবিতে',
  labelEn: 'India flood footage claimed as Bangladesh 2024',
  category: 'disaster',
  thumbnail: '🌊',
  claim: 'Bangladesh flood 2024 — victims trapped in rising floodwaters in Sylhet region',
  claimedDate: '2024-08-20',
  expectedVerdict: 'mismatch',
  expectedConfidence: 0.89,
  events: [
    { delayMs: 0,    event: 'agent_started',  data: { agent: 'geolocator' } },
    { delayMs: 350,  event: 'agent_progress', data: { agent: 'geolocator', data: { progress: 0.4, text: 'Analyzing geographic visual features and architecture...' } } },
    { delayMs: 900,  event: 'agent_finding',  data: { agent: 'geolocator', data: { type: 'visual_landmark', description: 'Kerala-style sloped tiled roofs detected — architectural pattern typical of South Indian coastal regions, not found in Bangladesh', confidence: 0.82, weight: 'high' } } },
    { delayMs: 1600, event: 'agent_complete', data: { agent: 'geolocator' } },

    { delayMs: 1700, event: 'agent_started',  data: { agent: 'linguist' } },
    { delayMs: 2100, event: 'agent_progress', data: { agent: 'linguist', data: { progress: 0.45, text: 'Analyzing text overlays and spoken audio...' } } },
    { delayMs: 2700, event: 'agent_finding',  data: { agent: 'linguist', data: { type: 'language_detection', description: 'Malayalam text visible on rescue boat banner — official language of Kerala, India (not Bangladesh)', confidence: 0.88, weight: 'high' } } },
    { delayMs: 3300, event: 'agent_finding',  data: { agent: 'linguist', data: { type: 'audio_analysis', description: 'Background speech identified as Malayalam language — not Bengali', confidence: 0.84, weight: 'medium' } } },
    { delayMs: 3900, event: 'agent_complete', data: { agent: 'linguist' } },

    { delayMs: 4000, event: 'agent_started',  data: { agent: 'tracer' } },
    { delayMs: 4500, event: 'agent_progress', data: { agent: 'tracer', data: { progress: 0.35, text: 'Searching news archives for matching footage...' } } },
    { delayMs: 5200, event: 'agent_finding',  data: { agent: 'tracer', data: { type: 'source_match', description: 'Original footage: NDTV India coverage of Kerala floods, August 2018 — 6 years before claimed date', confidence: 0.87, weight: 'high' } } },
    { delayMs: 5900, event: 'agent_complete', data: { agent: 'tracer' } },

    { delayMs: 6000, event: 'agent_started',  data: { agent: 'chronologist' } },
    { delayMs: 6400, event: 'agent_progress', data: { agent: 'chronologist', data: { progress: 0.5, text: 'Verifying event timeline...' } } },
    { delayMs: 6900, event: 'agent_finding',  data: { agent: 'chronologist', data: { type: 'date_mismatch', description: 'Original event: August 2018 Kerala floods — 6 years before claimed 2024 Bangladesh disaster', confidence: 0.87, weight: 'high' } } },
    { delayMs: 7400, event: 'agent_complete', data: { agent: 'chronologist' } },

    { delayMs: 7500, event: 'agent_started',  data: { agent: 'adjudicator' } },
    { delayMs: 7900, event: 'agent_progress', data: { agent: 'adjudicator', data: { progress: 0.5, text: 'Evaluating cross-agent evidence...' } } },
    { delayMs: 8600, event: 'agent_progress', data: { agent: 'adjudicator', data: { progress: 0.85, text: 'Kerala architecture + Malayalam text + 2018 NDTV source = mismatch confirmed' } } },
    { delayMs: 9200, event: 'agent_complete', data: { agent: 'adjudicator' } },
    {
      delayMs: 9500,
      event: 'investigation_complete',
      data: { data: { verdict: {
        verdict: 'mismatch',
        confidence: 0.89,
        summary_bn: 'ভিডিওটি ২০১৮ সালের ভারতের কেরালা রাজ্যের বন্যার। ভিডিওতে মালায়ালাম ভাষার লেখা এবং কেরালার স্থাপত্য স্পষ্ট দেখা যাচ্ছে। এটি ২০২৪ সালের বাংলাদেশের বন্যার ভিডিও নয় — ৬ বছর আগের পুরনো ভিডিও।',
        summary_en: 'This video is from the 2018 Kerala, India floods — not the 2024 Bangladesh floods. Malayalam text on rescue banners and Kerala-style architecture confirm the Indian origin. The footage is 6 years old.',
        actual_origin: { country: 'India', city: 'Kerala', earliest_date: '2018-08-16' },
        key_evidence: [
          { agent: 'geolocator',    finding: 'Kerala-style tiled roof architecture detected in frames',  weight: 'high' },
          { agent: 'linguist',      finding: 'Malayalam text on rescue boat banner',                     weight: 'high' },
          { agent: 'tracer',        finding: 'Matched to NDTV Kerala flood broadcast, August 2018',      weight: 'high' },
          { agent: 'chronologist',  finding: '6-year date discrepancy confirmed',                         weight: 'high' },
        ],
      } } },
    },
  ],
  reach: { base_shares: 312000, estimated_reach: 5616000, network_multiplier: 7, amplification: 2.5, verdict: 'mismatch' },
  similarCases: [
    { id: 201, title_en: 'Assam India flood footage shared as Bangladesh 2022 flood', title_bn: 'ভারতের আসাম বন্যার ভিডিও বাংলাদেশের ২০২২ বন্যার দাবিতে', false_claim_en: 'India Assam flood video shared as Bangladesh 2022 flood disaster', actual_origin_country: 'India', actual_origin_city: 'Assam', actual_origin_date: '2022-06-18', debunk_url: 'https://www.somoy.com/fact-check', debunk_source: 'Somoy TV' },
    { id: 202, title_en: 'Pakistan 2022 flood footage reshared as Bangladesh 2024 disaster', title_bn: 'পাকিস্তানের ২০২২ বন্যার ভিডিও বাংলাদেশের ২০২৪ দুর্যোগ দাবিতে', false_claim_en: '2022 Pakistan flood footage shared as recent Bangladesh disaster', actual_origin_country: 'Pakistan', actual_origin_city: 'Sindh', actual_origin_date: '2022-08-30', debunk_url: 'https://www.afp.com/fact-check', debunk_source: 'AFP Bangladesh' },
    { id: 203, title_en: 'Old 2017 Sri Lanka flood video shared as 2024 Bangladesh disaster', title_bn: '২০১৭ সালের শ্রীলংকার বন্যার ভিডিও ২০২৪ বাংলাদেশের দাবিতে', false_claim_en: 'Sri Lanka 2017 flood reshared as recent Bangladesh disaster footage', actual_origin_country: 'Sri Lanka', actual_origin_city: 'Colombo', actual_origin_date: '2017-05-26', debunk_url: 'https://www.rtvonline.com/fact-check', debunk_source: 'RTV Fact Check' },
  ],
};

// ─── Demo 3: Authentic Bangladesh July 2024 protest ───────────────────────────
const AUTHENTIC_BD: DemoInvestigation = {
  id: 'demo-authentic-bd',
  label: 'সত্যিকারের বাংলাদেশ আন্দোলন',
  labelEn: 'Authentic Bangladesh July 2024 protest',
  category: 'politics',
  thumbnail: '✓',
  claim: 'Student protest at Dhaka University demanding quota reform, July 15, 2024',
  claimedDate: '2024-07-15',
  expectedVerdict: 'authentic',
  expectedConfidence: 0.91,
  events: [
    { delayMs: 0,    event: 'agent_started',  data: { agent: 'geolocator' } },
    { delayMs: 400,  event: 'agent_progress', data: { agent: 'geolocator', data: { progress: 0.5, text: 'Analyzing architectural and geographic features...' } } },
    { delayMs: 1000, event: 'agent_finding',  data: { agent: 'geolocator', data: { type: 'landmark', description: 'Dhaka University campus recognized — "Aparajeyo Bangla" sculpture and Madhur Canteen visible in background', confidence: 0.89, weight: 'high' } } },
    { delayMs: 1600, event: 'agent_complete', data: { agent: 'geolocator' } },

    { delayMs: 1700, event: 'agent_started',  data: { agent: 'linguist' } },
    { delayMs: 2000, event: 'agent_progress', data: { agent: 'linguist', data: { progress: 0.4, text: 'Analyzing text and language in video...' } } },
    { delayMs: 2500, event: 'agent_finding',  data: { agent: 'linguist', data: { type: 'script_detection', description: 'Bengali script confirmed on all protest banners — consistent with Bangladesh origin', confidence: 0.96, weight: 'high' } } },
    { delayMs: 3100, event: 'agent_finding',  data: { agent: 'linguist', data: { type: 'content_analysis', description: 'Protest chants in Bangladeshi dialect — quota reform slogans match known July 2024 movement vocabulary exactly', confidence: 0.92, weight: 'high' } } },
    { delayMs: 3700, event: 'agent_complete', data: { agent: 'linguist' } },

    { delayMs: 3800, event: 'agent_started',  data: { agent: 'tracer' } },
    { delayMs: 4200, event: 'agent_progress', data: { agent: 'tracer', data: { progress: 0.4, text: 'Searching for original source publication...' } } },
    { delayMs: 4800, event: 'agent_finding',  data: { agent: 'tracer', data: { type: 'source_match', description: 'Video first published by verified Prothom Alo and Daily Star social media accounts on July 15, 2024', confidence: 0.88, weight: 'high' } } },
    { delayMs: 5400, event: 'agent_complete', data: { agent: 'tracer' } },

    { delayMs: 5500, event: 'agent_started',  data: { agent: 'chronologist' } },
    { delayMs: 5800, event: 'agent_progress', data: { agent: 'chronologist', data: { progress: 0.6, text: 'Verifying timeline against known events...' } } },
    { delayMs: 6300, event: 'agent_finding',  data: { agent: 'chronologist', data: { type: 'timeline_match', description: 'Event date matches July 15, 2024 — consistent with escalation of quota reform protests at Dhaka University', confidence: 0.91, weight: 'high' } } },
    { delayMs: 6800, event: 'agent_complete', data: { agent: 'chronologist' } },

    { delayMs: 6900, event: 'agent_started',  data: { agent: 'adjudicator' } },
    { delayMs: 7300, event: 'agent_progress', data: { agent: 'adjudicator', data: { progress: 0.5, text: 'Synthesizing all positive corroboration signals...' } } },
    { delayMs: 7900, event: 'agent_progress', data: { agent: 'adjudicator', data: { progress: 0.9, text: 'Bengali script + DU landmarks + Prothom Alo source = authentic confirmed' } } },
    { delayMs: 8500, event: 'agent_complete', data: { agent: 'adjudicator' } },
    {
      delayMs: 8800,
      event: 'investigation_complete',
      data: { data: { verdict: {
        verdict: 'authentic',
        confidence: 0.91,
        summary_bn: 'ভিডিওটি সত্যিকারের বাংলাদেশের জুলাই ২০২৪ কোটা সংস্কার আন্দোলনের। ঢাকা বিশ্ববিদ্যালয়ের পরিচিত স্থাপনা, বাংলা স্ক্রিপ্টের ব্যানার এবং প্রথম আলো ও ডেইলি স্টারের verified প্রকাশনা — সবই দাবির সাথে সামঞ্জস্যপূর্ণ।',
        summary_en: 'This video is authentic footage from the July 2024 quota reform protests in Bangladesh. Dhaka University landmarks, Bengali script banners, and original publication by verified news sources (Prothom Alo, Daily Star) all corroborate the claimed context.',
        actual_origin: { country: 'Bangladesh', city: 'Dhaka', earliest_date: '2024-07-15' },
        key_evidence: [
          { agent: 'geolocator',    finding: 'Dhaka University landmarks confirmed in background frames',     weight: 'high' },
          { agent: 'linguist',      finding: 'Bengali script on all banners — consistent with Bangladesh',    weight: 'high' },
          { agent: 'tracer',        finding: 'First published by Prothom Alo / Daily Star on July 15, 2024', weight: 'high' },
          { agent: 'chronologist',  finding: 'Date matches July 2024 quota movement timeline exactly',        weight: 'high' },
        ],
      } } },
    },
  ],
  reach: { base_shares: 0, estimated_reach: null, network_multiplier: 7, amplification: 1.2, verdict: 'authentic' },
  similarCases: [],
};

export const DEMO_INVESTIGATIONS: Record<string, DemoInvestigation> = {
  'demo-pakistan-protest': PAKISTAN_PROTEST,
  'demo-india-flood':       INDIA_FLOOD,
  'demo-authentic-bd':      AUTHENTIC_BD,
};

// ─── Dashboard mock data ──────────────────────────────────────────────────────
export const DEMO_DASHBOARD = {
  viralFeed: [
    { id: 1, video_url: null, thumbnail_url: null, claim_text: 'Pakistani PTI protest footage shared as Bangladesh student demonstration 2024', claim_text_bn: 'পাকিস্তানের PTI বিক্ষোভের ভিডিও বাংলাদেশের ছাত্র আন্দোলন হিসেবে প্রচার', share_count: 1240000, detected_at: '2024-07-16T08:00:00Z', region: 'dhaka', category: 'politics', investigation_id: 'demo-pakistan-protest', is_featured: true },
    { id: 2, video_url: null, thumbnail_url: null, claim_text: 'India Kerala flood video shared as Bangladesh Sylhet flood 2024', claim_text_bn: 'ভারতের কেরালা বন্যার ভিডিও সিলেটের বন্যা হিসেবে প্রচার', share_count: 892000, detected_at: '2024-08-21T10:00:00Z', region: 'sylhet', category: 'disaster', investigation_id: 'demo-india-flood', is_featured: true },
    { id: 3, video_url: null, thumbnail_url: null, claim_text: 'Old 2013 footage of Cumilla violence reshared as recent communal attack', claim_text_bn: '২০১৩ সালের কুমিল্লার পুরনো ঘটনার ভিডিও সাম্প্রতিক সাম্প্রদায়িক হামলার দাবিতে', share_count: 674000, detected_at: '2024-10-14T06:00:00Z', region: 'chittagong', category: 'communal', investigation_id: null, is_featured: false },
    { id: 4, video_url: null, thumbnail_url: null, claim_text: 'COVID vaccine deaths video using unrelated hospital footage from 2019', claim_text_bn: 'করোনা ভ্যাকসিনে মৃত্যু দাবিতে ২০১৯ সালের হাসপাতালের পুরনো ভিডিও', share_count: 456000, detected_at: '2024-06-01T14:00:00Z', region: 'nationwide', category: 'health', investigation_id: null, is_featured: false },
    { id: 5, video_url: null, thumbnail_url: null, claim_text: 'PM Sheikh Hasina resignation video manipulated to show false statement', claim_text_bn: 'প্রধানমন্ত্রী শেখ হাসিনার পদত্যাগের মিথ্যা বক্তব্য সম্বলিত ম্যানিপুলেটেড ভিডিও', share_count: 2100000, detected_at: '2024-08-05T18:00:00Z', region: 'nationwide', category: 'politics', investigation_id: null, is_featured: true },
    { id: 6, video_url: null, thumbnail_url: null, claim_text: 'Old 2021 Rohingya camp fire shared as recent Bangladesh border crisis', claim_text_bn: '২০২১ সালের রোহিঙ্গা ক্যাম্পের আগুনের ভিডিও সাম্প্রতিক ঘটনা দাবিতে', share_count: 321000, detected_at: '2024-09-10T09:00:00Z', region: 'chittagong', category: 'communal', investigation_id: null, is_featured: false },
    { id: 7, video_url: null, thumbnail_url: null, claim_text: 'False claim: Dhaka earthquake footage actually from Turkey 2023', claim_text_bn: 'ঢাকায় ভূমিকম্পের দাবিতে তুরস্কের ২০২৩ সালের ভিডিও', share_count: 187000, detected_at: '2024-05-15T12:00:00Z', region: 'dhaka', category: 'disaster', investigation_id: null, is_featured: false },
    { id: 8, video_url: null, thumbnail_url: null, claim_text: 'India mob lynching video falsely shared as Bangladesh communal violence', claim_text_bn: 'ভারতের গণপিটুনির ভিডিও বাংলাদেশের সাম্প্রদায়িক হিংসা দাবিতে', share_count: 534000, detected_at: '2024-07-28T16:00:00Z', region: 'rajshahi', category: 'communal', investigation_id: null, is_featured: false },
    { id: 9, video_url: null, thumbnail_url: null, claim_text: 'Fake health alert: drinking water contamination video from Indonesia', claim_text_bn: 'পানি দূষণের মিথ্যা স্বাস্থ্য সতর্কতা — ইন্দোনেশিয়ার ভিডিও', share_count: 98000, detected_at: '2024-04-20T08:00:00Z', region: 'nationwide', category: 'health', investigation_id: null, is_featured: false },
    { id: 10, video_url: null, thumbnail_url: null, claim_text: 'July 2024 protest student injuries — claim exaggerated, minor police response', claim_text_bn: 'জুলাই ২০২৪ আন্দোলনে আহতের সংখ্যা অতিরঞ্জিত দাবি', share_count: 445000, detected_at: '2024-07-19T11:00:00Z', region: 'dhaka', category: 'politics', investigation_id: null, is_featured: false },
    { id: 11, video_url: null, thumbnail_url: null, claim_text: 'False: Bangladeshi factory fire footage actually from Pakistan 2022', claim_text_bn: 'বাংলাদেশের কারখানায় আগুনের দাবিতে পাকিস্তানের ২০২২ সালের ভিডিও', share_count: 267000, detected_at: '2024-03-10T13:00:00Z', region: 'dhaka', category: 'disaster', investigation_id: null, is_featured: false },
    { id: 12, video_url: null, thumbnail_url: null, claim_text: 'Mymensingh temple desecration footage reused from 2016 incident', claim_text_bn: 'ময়মনসিংহ মন্দির ভাঙচুরের ২০১৬ সালের ভিডিও সম্প্রতি প্রচার', share_count: 312000, detected_at: '2024-11-01T07:00:00Z', region: 'mymensingh', category: 'communal', investigation_id: null, is_featured: false },
  ],
  stats: {
    total_viral: 247,
    total_mismatch: 183,
    total_authentic: 64,
    by_region: { dhaka: 89, chittagong: 42, sylhet: 31, rajshahi: 28, nationwide: 57 },
    by_category: { politics: 94, communal: 67, disaster: 48, health: 38 },
  },
  leaderboard: [
    { id: 1, platform: 'facebook', display_name: 'Viral BD Videos',          source_identifier: 'fb_viral_bd',        total_shared: 12450, flagged_count: 11780, credibility_score: 0.04, flag_rate: 94.6, last_flagged_at: '2024-11-01' },
    { id: 2, platform: 'facebook', display_name: 'বাংলাদেশ সংবাদ ২৪',       source_identifier: 'fb_bd_sangbad_24',   total_shared: 8920,  flagged_count: 6890,  credibility_score: 0.08, flag_rate: 77.2, last_flagged_at: '2024-10-28' },
    { id: 3, platform: 'facebook', display_name: 'সিলেট নিউজ বিডি',          source_identifier: 'fb_sylhet_news_bd',  total_shared: 5670,  flagged_count: 4320,  credibility_score: 0.12, flag_rate: 76.1, last_flagged_at: '2024-10-15' },
    { id: 4, platform: 'youtube',  display_name: 'BD Truth Channel',           source_identifier: 'yt_bd_truth',        total_shared: 7830,  flagged_count: 5450,  credibility_score: 0.15, flag_rate: 69.6, last_flagged_at: '2024-10-30' },
    { id: 5, platform: 'facebook', display_name: 'রাজশাহী এক্সপ্রেস',        source_identifier: 'fb_rajshahi_express', total_shared: 3240,  flagged_count: 2180,  credibility_score: 0.19, flag_rate: 67.3, last_flagged_at: '2024-09-22' },
    { id: 6, platform: 'tiktok',   display_name: 'BD Viral Clips',             source_identifier: 'tk_bd_viral',        total_shared: 15600, flagged_count: 9870,  credibility_score: 0.23, flag_rate: 63.3, last_flagged_at: '2024-11-02' },
    { id: 7, platform: 'facebook', display_name: 'Dhaka Underground News',     source_identifier: 'fb_dhaka_underground',total_shared: 4120,  flagged_count: 2380,  credibility_score: 0.27, flag_rate: 57.8, last_flagged_at: '2024-10-18' },
    { id: 8, platform: 'youtube',  display_name: 'সত্য প্রকাশ',               source_identifier: 'yt_satya_prokash',   total_shared: 2890,  flagged_count: 1560,  credibility_score: 0.31, flag_rate: 54.0, last_flagged_at: '2024-09-30' },
    { id: 9, platform: 'facebook', display_name: 'Breaking Bangladesh 24',     source_identifier: 'fb_breaking_bd24',   total_shared: 6780,  flagged_count: 3290,  credibility_score: 0.34, flag_rate: 48.5, last_flagged_at: '2024-10-25' },
    { id: 10, platform: 'tiktok',  display_name: 'Real News BD',               source_identifier: 'tk_real_news_bd',    total_shared: 9230,  flagged_count: 4010,  credibility_score: 0.38, flag_rate: 43.4, last_flagged_at: '2024-10-31' },
  ],
  campaigns: [
    { id: 1, phash: 'a3f8c1d2', investigation_count: 23, first_seen_at: '2024-07-15T00:00:00Z', sample_claim_bn: 'পাকিস্তানি ভিডিও দিয়ে জুলাই আন্দোলনের ভুল তথ্য ছড়ানো', investigation_ids: [] },
    { id: 2, phash: 'b7e2a9c4', investigation_count: 15, first_seen_at: '2024-10-14T00:00:00Z', sample_claim_bn: 'কুমিল্লা মন্দির হামলায় বিদেশি ভিডিও ব্যবহার', investigation_ids: [] },
  ],
  trustGraph: {
    nodes: [
      { id: 'fb_viral_bd',         label: 'Viral BD Videos',        platform: 'facebook', credibility_score: 0.04, total_shared: 12450, flagged_count: 11780 },
      { id: 'fb_bd_sangbad_24',    label: 'BD সংবাদ ২৪',           platform: 'facebook', credibility_score: 0.08, total_shared: 8920,  flagged_count: 6890 },
      { id: 'tk_bd_viral',         label: 'BD Viral Clips',          platform: 'tiktok',   credibility_score: 0.23, total_shared: 15600, flagged_count: 9870 },
      { id: 'yt_bd_truth',         label: 'BD Truth Channel',         platform: 'youtube',  credibility_score: 0.15, total_shared: 7830,  flagged_count: 5450 },
      { id: 'fb_sylhet_news_bd',   label: 'সিলেট নিউজ বিডি',        platform: 'facebook', credibility_score: 0.12, total_shared: 5670,  flagged_count: 4320 },
      { id: 'fb_dhaka_underground',label: 'Dhaka Underground',        platform: 'facebook', credibility_score: 0.27, total_shared: 4120,  flagged_count: 2380 },
    ],
    edges: [
      { source: 'fb_viral_bd',       target: 'fb_bd_sangbad_24',    weight: 5 },
      { source: 'fb_viral_bd',       target: 'tk_bd_viral',          weight: 4 },
      { source: 'fb_bd_sangbad_24',  target: 'yt_bd_truth',          weight: 3 },
      { source: 'tk_bd_viral',       target: 'fb_sylhet_news_bd',    weight: 2 },
      { source: 'yt_bd_truth',       target: 'fb_dhaka_underground', weight: 2 },
    ],
  },
};

// ─── Chat Q&A pairs ───────────────────────────────────────────────────────────
export const DEMO_CHAT_QA: { keywords: string[]; answer: string }[] = [
  {
    keywords: ['mob', 'july', 'quota', 'july 2024', 'protest', 'জুলাই', 'আন্দোলন', 'কোটা', 'ছাত্র'],
    answer: `During the July 2024 quota reform protests in Bangladesh, several mob violence videos circulated that were misattributed:\n\n**1. Narayanganj mob beating (July 19, 2024)**\nA video of a mob beating went viral with false claims that the victim was a "Chhatra League leader." Investigation revealed the incident was a local dispute unrelated to protests. *Debunked by AFP Bangladesh.*\n\n**2. Pakistan PTI footage shared as BD protest (July 2023 original)**\nMultiple videos from Pakistani PTI rallies were recirculated as Bangladesh protest footage. Urdu script and GEO News watermarks confirmed Pakistani origin.\n\n**3. India police crackdown shared as BD police response**\nHindi-language news watermarks exposed this as Indian footage.\n\nIn total, OriginX database has **14 verified false videos** linked to the July 2024 protest period.`,
  },
  {
    keywords: ['pakistan', 'pakistani', 'urdu', 'geo news', 'ptl', 'pti'],
    answer: `OriginX has documented **18 cases** of Pakistani footage being misrepresented as Bangladeshi content:\n\n**Most common patterns:**\n- PTI political rally footage labeled as BD student protests\n- GEO News / ARY News broadcasts shown as BD news coverage\n- Pakistan police crackdown videos shared as BD law enforcement actions\n- Karachi floods shared as Dhaka/Sylhet flooding\n\n**How to detect:** Urdu script in text overlays, Pakistani news channel watermarks (GEO, ARY, Samaa), Pakistani phone number formats (+92), and Sindhi/Punjabi architecture are key indicators.\n\n**Highest impact case:** A Lahore PTI rally video reached an estimated **23.7 million people** in Bangladesh before debunking.`,
  },
  {
    keywords: ['cumilla', 'comilla', 'hindu', 'temple', 'mandir', 'সাম্প্রদায়িক', 'কুমিল্লা', 'হিন্দু', 'মন্দির', 'হামলা'],
    answer: `The Cumilla Hindu temple incident (October 2021) generated significant misinformation:\n\n**Verified false videos circulating:**\n1. **2013 Ramu incident footage** reshared as Cumilla 2021 (7-year-old content)\n2. **India communal violence clips** (from UP, Delhi) labeled as Bangladesh\n3. **Manipulated audio** on authentic footage to make response seem muted\n\n**Fact-check sources:** Rumor Scanner, Prothom Alo Fact Check, BOOM Bangladesh\n\n**What actually happened:** Verified temple vandalism occurred on October 13, 2021 in Cumilla following a social media provocation. However, ~40% of viral videos claiming to show the event were from unrelated incidents in India or older BD events.`,
  },
  {
    keywords: ['flood', 'বন্যা', 'sylhet', 'সিলেট', 'water', 'disaster'],
    answer: `**Flood-related misinformation in Bangladesh (documented cases: 12)**\n\n**Recurring false footage sources:**\n- Kerala, India 2018 floods → shared as BD 2019, 2022, 2024\n- Pakistan Sindh 2022 floods → shared as Bangladesh disaster\n- Assam, India footage → shared as Sylhet floods\n\n**Why Bangladesh flood content gets mixed:** Geographic similarity (flat terrain, rivers, similar housing in rural areas) makes visual identification harder. Language is the key differentiator — Bengali script vs. Malayalam/Hindi/Urdu.\n\n**Most viral case:** Kerala 2018 NDTV footage shared as 2024 BD floods reached **5.6 million people** before correction.`,
  },
  {
    keywords: ['covid', 'vaccine', 'করোনা', 'স্বাস্থ্য', 'health', 'কোভিড', 'ভ্যাকসিন'],
    answer: `**COVID-19 misinformation cases in Bangladesh database: 9 verified incidents**\n\n**Top false narratives detected:**\n1. "Vaccine deaths" — hospital footage from 2019 pre-COVID era used as vaccine death evidence\n2. "5G towers causing COVID" — Italian tower fire footage shared in Bangladesh with false captions\n3. "COVID cure" herb videos — recycled traditional medicine content with new false COVID claims\n4. Inflated death count videos using morgue footage from unrelated countries\n\n**Verification tools used:** Reverse image search on keyframes, date metadata analysis, source tracing to original news broadcasts.\n\n**Key source:** icddr,b and WHO Bangladesh office issued clarifications on 6 of these cases.`,
  },
  {
    keywords: ['rohingya', 'রোহিঙ্গা', 'myanmar', 'cox bazar'],
    answer: `**Rohingya-related video misinformation (8 documented cases):**\n\n1. **2017 Myanmar military crackdown footage** recycled as "new" crisis in 2021, 2023\n2. **Cox's Bazar camp fire (2021)** — accurate footage but false captions claiming "government deliberately burned Rohingya"\n3. **Indonesian refugee footage** shared as Rohingya crossing to Bangladesh\n4. **Old Rakhine footage** reused to falsely claim ongoing genocide during non-crisis periods\n\n**Pattern:** Rohingya content tends to recirculate every ~18 months, often timed to political news cycles.\n\n**Credible sources:** UNHCR Bangladesh, Human Rights Watch Bangladesh reports, The Daily Star dedicated fact-check desk.`,
  },
  {
    keywords: ['বাংলাদেশ', 'ভুয়া', 'মিথ্যা', 'গুজব', 'fake', 'false', 'rumor', 'misinformation'],
    answer: `**OriginX Knowledge Base Overview**\n\nDatabase contains **89 verified Bangladesh misinformation incidents** across categories:\n\n| Category | Cases | Avg Reach |\n|---|---|---|\n| Politics / Protests | 34 | 8.2M |\n| Communal Violence | 22 | 5.1M |\n| Natural Disasters | 18 | 3.8M |\n| Health / COVID | 9 | 2.4M |\n| Rohingya Crisis | 6 | 4.7M |\n\n**Top origin countries for false content:** Pakistan (31%), India (28%), Myanmar (11%), domestic Bangladesh (22%), other (8%)\n\n**Key detection signals:** Urdu/Hindi/Malayalam script, foreign news watermarks, reverse image search matches, metadata timestamp discrepancies, architectural analysis.\n\nAsk me about any specific topic or incident for detailed information.`,
  },
];
