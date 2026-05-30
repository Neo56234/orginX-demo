"use client";

import { useEffect, useState } from "react";
import { getCases } from "@/lib/api";

export default function CasesPage() {
  const [cases, setCases] = useState<any[]>([]);

  useEffect(() => {
    getCases().then(setCases).catch(console.error);
  }, []);

  return (
    <main className="min-h-screen bg-background p-8">
      <h1 className="text-3xl font-bold font-sans text-white mb-8">Known Cases Database</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cases.map((c, i) => (
          <div key={i} className="bg-card p-6 rounded-xl border border-gray-800">
            <h3 className="text-xl text-white font-bangla font-bold mb-3">{c.title}</h3>
            <div className="flex gap-2 mb-4">
              <span className="px-2 py-1 bg-alert/20 text-alert rounded text-xs">Misinformation</span>
            </div>
            <p className="text-sm text-gray-400 font-sans line-clamp-3">{c.description}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
