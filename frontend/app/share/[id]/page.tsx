"use client";

import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import { useInvestigationStore } from "@/lib/store";
import { getInvestigation } from "@/lib/api";
import CounterCard from "@/components/share/CounterCard";
import * as htmlToImage from "html-to-image";

export default function SharePage() {
  const params = useParams();
  const id = params.id as string;
  const cardRef = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getInvestigation(id);
        if (data.verdict) {
          useInvestigationStore.setState({
            verdict: typeof data.verdict === 'string' ? {
              status: data.verdict,
              confidence: data.confidence,
              summary_bn: data.summary_bn,
              summary_en: data.summary_en,
              actual_origin_country: data.actual_origin_country,
              actual_origin_city: data.actual_origin_city
            } as any : data.verdict
          });
          setReady(true);
        }
      } catch (e) {
        console.error(e);
      }
    }
    if (id) loadData();
  }, [id]);

  const downloadImage = async () => {
    if (!cardRef.current) return;
    try {
      const dataUrl = await htmlToImage.toPng(cardRef.current);
      const link = document.createElement("a");
      link.download = `originx-factcheck-${id}.png`;
      link.href = dataUrl;
      link.click();
    } catch (error) {
      console.error("Error generating image:", error);
    }
  };

  if (!ready) {
    return <div className="min-h-screen bg-background flex items-center justify-center text-white">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div ref={cardRef} className="w-full max-w-[540px]">
        <CounterCard />
      </div>
      
      <div className="mt-8 flex gap-4">
        <button 
          onClick={downloadImage}
          className="bg-primary text-white font-bold py-3 px-8 rounded-xl hover:bg-blue-600 transition-colors"
        >
          Download Card
        </button>
        <button 
          onClick={() => window.location.href = '/'}
          className="bg-card text-gray-300 font-bold py-3 px-8 rounded-xl border border-gray-700 hover:bg-gray-800 transition-colors"
        >
          Home
        </button>
      </div>
    </div>
  );
}
