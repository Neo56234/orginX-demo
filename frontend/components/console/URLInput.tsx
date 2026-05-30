"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { analyzeVideo, analyzeUpload } from "@/lib/api";
import { useInvestigationStore } from "@/lib/store";
import { t } from "@/lib/i18n";

export default function URLInput() {
  const [url, setUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [claimedContext, setClaimedContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recent, setRecent] = useState<{ id: string; url: string; date: number }[]>([]);
  const router = useRouter();
  const startInvestigation = useInvestigationStore((state) => state.startInvestigation);
  const lang = useInvestigationStore((state) => state.language);

  useEffect(() => {
    const saved = localStorage.getItem("originx_recent");
    if (saved) {
      try {
        setRecent(JSON.parse(saved));
      } catch (e) {}
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url && !file) return;

    setLoading(true);
    setError(null);

    try {
      let result;
      if (file) {
        result = await analyzeUpload(file, claimedContext);
      } else {
        result = await analyzeVideo(url, claimedContext);
      }
      
      // Save to recent
      const newRecent = [
        { id: result.investigation_id, url: file ? file.name : url, date: Date.now() },
        ...recent.filter(item => item.id !== result.investigation_id)
      ].slice(0, 5);
      
      localStorage.setItem("originx_recent", JSON.stringify(newRecent));
      setRecent(newRecent);

      await startInvestigation(file ? file.name : url);
      router.push(`/investigation/${result.investigation_id}`);
    } catch (err: any) {
      setError(err.message || "Failed to start investigation");
      setLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setUrl(""); // Clear URL if file is selected
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-12">
      <form onSubmit={handleSubmit} className="relative w-full">
        <motion.div
          animate={{
            boxShadow: loading 
              ? ["0px 0px 0px #3D8BFF", "0px 0px 20px #3D8BFF", "0px 0px 0px #3D8BFF"]
              : "0px 0px 0px transparent"
          }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="relative flex items-center p-2 rounded-xl bg-card border border-gray-800 focus-within:border-primary focus-within:shadow-[0_0_15px_rgba(61,139,255,0.3)] transition-all duration-300"
        >
          <div className="flex-1 flex flex-col sm:flex-row gap-2 relative w-full">
            <input
              type="url"
              value={url}
              onChange={(e) => { setUrl(e.target.value); setFile(null); }}
              placeholder={file ? file.name : t('paste_url', lang)}
              disabled={loading}
              required={!file}
              className="flex-1 bg-transparent border-none outline-none text-foreground px-4 py-3 text-lg font-sans placeholder-gray-500 min-w-0"
            />
            <div className="relative flex items-center justify-center border-l border-gray-800 pl-2">
              <input 
                type="file" 
                accept="video/mp4,video/webm,video/quicktime" 
                onChange={handleFileChange}
                disabled={loading}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                title="Upload Video File"
              />
              <button 
                type="button"
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-sans text-sm transition-colors ${file ? 'bg-primary/20 text-primary' : 'bg-gray-800 text-gray-300 hover:bg-gray-700'}`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                {file ? "File Selected" : "Upload"}
              </button>
            </div>
          </div>
          <button
            type="submit"
            disabled={loading || (!url && !file)}
            className="ml-2 bg-primary text-white font-bold py-3 px-8 rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors tracking-wide shrink-0"
          >
            {loading ? t('analyzing', lang) : t('analyze', lang)}
          </button>
        </motion.div>
        <div className="mt-4">
          <input
            type="text"
            value={claimedContext}
            onChange={(e) => setClaimedContext(e.target.value)}
            placeholder="Optional: What is the claimed context? (e.g., Bangladesh protests 2024)"
            disabled={loading}
            className="w-full bg-card border border-gray-800 rounded-xl px-4 py-3 text-sm font-sans placeholder-gray-500 focus:border-primary focus:outline-none transition-colors text-white"
          />
        </div>
        {error && (
          <p className="text-alert mt-4 text-center font-bangla">{error}</p>
        )}
      </form>

      {recent.length > 0 && (
        <div className="mt-12">
          <h3 className="text-gray-500 text-sm uppercase tracking-wider mb-4 font-sans pl-2">
            Recent Investigations
          </h3>
          <div className="space-y-2">
            {recent.map((item) => (
              <div 
                key={item.id} 
                onClick={() => router.push(`/investigation/${item.id}`)}
                className="flex justify-between items-center bg-card/50 p-4 rounded-lg border border-gray-800/50 hover:border-gray-600 cursor-pointer transition-colors"
              >
                <div className="truncate text-gray-300 mr-4 font-mono text-sm max-w-[70%]">
                  {item.url}
                </div>
                <div className="text-xs text-gray-500 font-sans">
                  {new Date(item.date).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
