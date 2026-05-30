"use client";

import { useInvestigationStore } from "@/lib/store";

export default function LanguageSwitcher() {
  const lang = useInvestigationStore(state => state.language);
  const setLanguage = useInvestigationStore(state => state.setLanguage);

  return (
    <div className="fixed top-4 right-4 z-50 flex bg-gray-900 rounded-full p-1 border border-gray-700 shadow-lg">
      <button
        onClick={() => setLanguage('en')}
        className={`px-4 py-1.5 rounded-full text-sm font-bold font-sans transition-colors ${
          lang === 'en' ? 'bg-primary text-white shadow' : 'text-gray-400 hover:text-white'
        }`}
      >
        EN
      </button>
      <button
        onClick={() => setLanguage('bn')}
        className={`px-4 py-1.5 rounded-full text-sm font-bold font-bangla transition-colors ${
          lang === 'bn' ? 'bg-primary text-white shadow' : 'text-gray-400 hover:text-white'
        }`}
      >
        বাংলা
      </button>
    </div>
  );
}
