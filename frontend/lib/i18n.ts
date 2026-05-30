export type Language = 'bn' | 'en';

export const strings = {
  bn: {
    analyze: "তদন্ত শুরু করুন",
    analyzing: "বিশ্লেষণ করা হচ্ছে...",
    paste_url: "ভিডিও লিংক পেস্ট করুন...",
    investigating: "তদন্ত চলছে...",
    
    verdict_mismatch: "মিথ্যা প্রসঙ্গ সনাক্ত",
    verdict_authentic: "সত্যতা নিশ্চিত",
    verdict_insufficient: "অপর্যাপ্ত প্রমাণ",
    
    share_rebuttal: "প্রতিবাদ শেয়ার করুন",
    view_investigation: "তদন্ত দেখুন",
    
    // Agent names & roles
    agent_geolocator_name: "Geolocator",
    agent_geolocator_role: "কোথায় তোলা হয়েছে?",
    
    agent_chronologist_name: "Chronologist",
    agent_chronologist_role: "কখন তোলা হয়েছে?",
    
    agent_tracer_name: "Tracer",
    agent_tracer_role: "আগে কোথায় দেখা গেছে?",
    
    agent_linguist_name: "Linguist",
    agent_linguist_role: "কী লেখা আছে?",
    
    agent_adjudicator_name: "Adjudicator",
    agent_adjudicator_role: "সত্য কী?",

    // Evidence
    confidence: "নিশ্চয়তা",
    actual_origin: "আসল উৎস",
    claimed_context: "দাবিকৃত প্রসঙ্গ",
    hero_subtitle: "অত্যাধুনিক AI এজেন্ট সোয়র্ম (Swarm) ব্যবহার করে যেকোনো ভিডিওর উৎস, সত্যতা এবং সময়কাল যাচাই করুন।"
  },
  en: {
    analyze: "START INVESTIGATION",
    analyzing: "Analyzing...",
    paste_url: "Paste video URL here...",
    investigating: "Investigation in progress...",
    
    verdict_mismatch: "False Context Detected",
    verdict_authentic: "Authentic Video",
    verdict_insufficient: "Insufficient Evidence",
    
    share_rebuttal: "Share Rebuttal",
    view_investigation: "View Investigation",
    
    // Agent names & roles
    agent_geolocator_name: "Geolocator",
    agent_geolocator_role: "Where was it filmed?",
    
    agent_chronologist_name: "Chronologist",
    agent_chronologist_role: "When was it filmed?",
    
    agent_tracer_name: "Tracer",
    agent_tracer_role: "Where was it seen before?",
    
    agent_linguist_name: "Linguist",
    agent_linguist_role: "What does it say?",
    
    agent_adjudicator_name: "Adjudicator",
    agent_adjudicator_role: "What is the truth?",

    // Evidence
    confidence: "Confidence",
    actual_origin: "Actual Origin",
    claimed_context: "Claimed Context",
    hero_subtitle: "Verify the origin, authenticity, and context of any video using an advanced AI agent swarm."
  }
};

export type StringKey = keyof typeof strings.bn;

export function t(key: StringKey, lang: Language = 'bn'): string {
  return strings[lang][key] || strings.bn[key] || key;
}
