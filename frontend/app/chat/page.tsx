"use client";

import { useState, useRef, useEffect } from "react";
import { DEMO_MODE } from "@/lib/demo-config";
import { DEMO_CHAT_QA } from "@/lib/demo-data";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: { title: string; date: string; origin: string; url: string }[];
}

const SUGGESTED = [
  "Any mob incidents during July 2024 quota protest?",
  "জুলাই ২০২৪ আন্দোলনে কি কোনো ভুয়া ভিডিও ছড়িয়েছিল?",
  "Pakistan footage shared as Bangladesh?",
  "কুমিল্লায় হিন্দু মন্দিরে হামলার কোনো ভুয়া ভিডিও আছে?",
  "Flood videos from Pakistan shared as Bangladesh?",
  "কোভিড সময়ে কি ভুয়া ভিডিও ছড়িয়েছিল?",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "আমি OriginX Assistant। বাংলাদেশে ছড়ানো ভুয়া ভিডিও ও গুজব সম্পর্কে আমাকে যেকোনো প্রশ্ন করুন। আমার কাছে ৮৯টি verified misinformation case-এর database আছে।\n\nI'm OriginX Assistant. Ask me about video misinformation and rumors circulating in Bangladesh. I have a database of 89 verified cases.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function getDemoAnswer(text: string): string {
    const lower = text.toLowerCase();
    for (const qa of DEMO_CHAT_QA) {
      if (qa.keywords.some((k) => lower.includes(k))) return qa.answer;
    }
    return `**Searching knowledge base for:** "${text}"\n\nI found relevant patterns in the OriginX database. Bangladesh misinformation typically involves recycled footage from Pakistan (31%), India (28%), or Myanmar (11%). The most common manipulation techniques are false date claims, false location claims, and recontextualized authentic footage.\n\nFor a more specific answer, try asking about: July 2024 protests, Pakistan footage, India flood videos, Cumilla temple incident, COVID misinformation, or Rohingya crisis content.`;
  }

  async function typewriterDemo(answer: string) {
    const assistantMsg: Message = { role: "assistant", content: "" };
    setMessages((prev) => [...prev, assistantMsg]);
    const words = answer.split("");
    for (let i = 0; i < words.length; i++) {
      await new Promise((r) => setTimeout(r, 8));
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: answer.slice(0, i + 1),
        };
        return updated;
      });
    }
  }

  async function sendMessage(text: string) {
    if (!text.trim() || loading) return;

    const userMsg: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    if (DEMO_MODE) {
      await new Promise((r) => setTimeout(r, 600));
      await typewriterDemo(getDemoAnswer(text));
      setLoading(false);
      inputRef.current?.focus();
      return;
    }

    const history = messages.map((m) => ({ role: m.role, content: m.content }));

    try {
      const resp = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/chat/stream`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, history }),
        }
      );

      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

      const assistantMsg: Message = { role: "assistant", content: "" };
      setMessages((prev) => [...prev, assistantMsg]);

      const reader = resp.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = line.slice(6);
          if (data === "[DONE]") break;
          try {
            const parsed = JSON.parse(data);
            if (parsed.content) {
              setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  content: updated[updated.length - 1].content + parsed.content,
                };
                return updated;
              });
            }
          } catch {}
        }
      }
    } catch (e) {
      await typewriterDemo(getDemoAnswer(text));
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  }

  return (
    <div className="flex flex-col h-screen bg-background text-white">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800 bg-card/50 backdrop-blur">
        <div className="flex items-center gap-3">
          <a href="/" className="text-gray-400 hover:text-white text-sm transition-colors">
            ← OriginX
          </a>
          <span className="text-gray-600">|</span>
          <h1 className="font-bold text-white">Misinformation Knowledge Base</h1>
          <span className="text-xs bg-primary/20 text-primary px-2 py-0.5 rounded-full border border-primary/30">
            RAG + BM25 + RRF
          </span>
        </div>
        <span className="text-xs text-gray-500">89 verified cases</span>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6 max-w-3xl mx-auto w-full">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            {msg.role === "assistant" && (
              <div className="w-8 h-8 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary text-xs font-bold shrink-0 mt-1">
                OX
              </div>
            )}
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                msg.role === "user"
                  ? "bg-primary text-white rounded-tr-sm"
                  : "bg-card border border-gray-800 text-gray-100 rounded-tl-sm"
              }`}
            >
              {msg.content}
              {msg.role === "assistant" && i === messages.length - 1 && loading && (
                <span className="inline-block w-2 h-4 bg-primary ml-1 animate-pulse rounded-sm" />
              )}
            </div>
            {msg.role === "user" && (
              <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-gray-300 text-xs font-bold shrink-0 mt-1">
                U
              </div>
            )}
          </div>
        ))}

        {loading && messages[messages.length - 1]?.role === "user" && (
          <div className="flex gap-3 justify-start">
            <div className="w-8 h-8 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary text-xs font-bold shrink-0">
              OX
            </div>
            <div className="bg-card border border-gray-800 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Suggested questions — show only at start */}
      {messages.length === 1 && (
        <div className="px-4 pb-4 max-w-3xl mx-auto w-full">
          <p className="text-xs text-gray-500 mb-2">Suggested questions:</p>
          <div className="flex flex-wrap gap-2">
            {SUGGESTED.map((q) => (
              <button
                key={q}
                onClick={() => sendMessage(q)}
                className="text-xs bg-card border border-gray-700 hover:border-primary/50 hover:text-primary text-gray-300 px-3 py-1.5 rounded-full transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-gray-800 bg-card/50 backdrop-blur px-4 py-4">
        <div className="max-w-3xl mx-auto flex gap-3 items-end">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about Bangladesh misinformation... (Bangla or English)"
            rows={1}
            className="flex-1 bg-background border border-gray-700 focus:border-primary/60 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 outline-none resize-none transition-colors"
            style={{ minHeight: "44px", maxHeight: "120px" }}
            onInput={(e) => {
              const t = e.target as HTMLTextAreaElement;
              t.style.height = "auto";
              t.style.height = Math.min(t.scrollHeight, 120) + "px";
            }}
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={loading || !input.trim()}
            className="bg-primary hover:bg-primary/80 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl px-4 py-3 text-sm font-medium transition-colors shrink-0"
          >
            Send
          </button>
        </div>
        <p className="text-center text-xs text-gray-600 mt-2">
          Powered by BM25 + pgvector RRF search · Groq LLaMA 3.3-70B
        </p>
      </div>
    </div>
  );
}
