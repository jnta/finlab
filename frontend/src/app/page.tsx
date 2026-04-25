"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Activity, Terminal, Zap, ArrowUpRight, ArrowDownRight, Settings, LayoutGrid, Database, Loader2, Bot, BookOpen } from 'lucide-react';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchMode, setSearchMode] = useState<"RAG" | "AGENT">("RAG");
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const handleSearch = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && searchQuery.trim()) {
      setIsLoading(true);
      const currentQuery = searchQuery;
      setSearchQuery(""); // clear input
      try {
        const endpoint = searchMode === "RAG" ? "http://127.0.0.1:8000/rag" : "http://127.0.0.1:8000/agent/analyze";
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: currentQuery, limit: 3 })
        });
        const data = await response.json();
        setSearchResults(prev => [{ mode: searchMode, query: currentQuery, data, id: Date.now() }, ...prev]);
      } catch (error) {
        console.error("Search error:", error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="p-4 max-w-[1600px] mx-auto w-full space-y-4 flex flex-col min-h-full">
        
        {/* Neural Search Bar */}
        <div className="relative group w-full max-w-3xl mx-auto my-4">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 rounded border border-cyan-500/30 group-hover:bg-cyan-500/20 transition duration-500"></div>
          <div className="relative flex items-center bg-[#0a0f1c] px-4 py-3 border border-cyan-500/20 shadow-[0_0_15px_rgba(6,182,212,0.05)]">
            <Search className="w-4 h-4 text-cyan-500 mr-3" />
            <span className="text-cyan-500/70 text-xs font-mono mr-2">NEURAL_SEARCH:</span>
            <input 
              type="text" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={handleSearch}
              placeholder={searchMode === "RAG" ? "Query Vault Documents (e.g., 'Tesla growth')" : "Run Deep Analysis (e.g., 'Analyze Apple')"} 
              className="bg-transparent border-none outline-none text-white text-sm w-full placeholder:text-slate-600 font-mono"
              disabled={isLoading}
            />
            <button 
              onClick={() => setSearchMode(searchMode === "RAG" ? "AGENT" : "RAG")}
              className={`flex items-center gap-1.5 px-2 py-1 border text-[10px] font-mono font-bold uppercase tracking-wider transition-colors mr-3 ${searchMode === "RAG" ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20" : "border-purple-500/30 bg-purple-500/10 text-purple-400 hover:bg-purple-500/20"}`}
            >
              {searchMode === "RAG" ? <BookOpen className="w-3 h-3" /> : <Bot className="w-3 h-3" />}
              {searchMode}
            </button>
            <div className="flex items-center gap-1 px-1.5 py-0.5 bg-slate-800 border border-white/5 text-[10px] text-slate-400 font-mono">
              <span>CMD</span>
              <span>K</span>
            </div>
          </div>
        </div>



        {/* Main Area */}
        <div className="flex flex-col gap-4 flex-1">
            
            {/* Workspace Feed */}
            <div className="flex-1 bg-[#0a0f1c] border border-white/5 flex flex-col overflow-hidden min-h-[300px]">
              <div className="px-3 py-2 border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Terminal className="w-3.5 h-3.5 text-slate-500" />
                  <h2 className="text-[10px] font-mono font-semibold text-slate-300 tracking-wider">WORKSPACE FEED</h2>
                </div>
                {isLoading ? (
                  <div className="text-[10px] text-cyan-500 font-mono flex items-center gap-2">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    PROCESSING...
                  </div>
                ) : (
                  <div className="text-[10px] text-slate-500 font-mono flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    READY
                  </div>
                )}
              </div>
              
              <div className="p-4 flex-1 overflow-auto space-y-4">
                
                {/* Dynamically Rendered Search Results */}
                {searchResults.map((result) => (
                  <div key={result.id} className="border border-white/5 bg-[#0e1424] flex flex-col group">
                    <div className="px-3 py-2 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
                      <div className="flex items-center gap-2">
                        {result.mode === "RAG" ? <BookOpen className="w-3 h-3 text-emerald-500" /> : <Bot className="w-3 h-3 text-purple-500" />}
                        <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300">
                          {result.mode === "RAG" ? "RAG SYNTHESIS" : "AGENT ANALYSIS"}
                        </span>
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono truncate max-w-[200px]">"{result.query}"</span>
                    </div>
                    
                    <div className="p-4 space-y-4">
                      {result.mode === "RAG" && result.data.answer && (
                        <div>
                          <div className="text-sm text-slate-300 leading-relaxed space-y-3">
                            {result.data.answer.split('\n').filter((p: string) => p.trim() !== '').map((paragraph: string, idx: number) => (
                              <p key={idx}>{paragraph}</p>
                            ))}
                          </div>
                          {result.data.metadata && result.data.metadata.length > 0 && (
                            <div className="mt-4 pt-3 border-t border-white/5">
                              <h4 className="text-[10px] font-mono text-slate-500 mb-2">SOURCES:</h4>
                              <div className="flex gap-2 flex-wrap">
                                {result.data.metadata.map((m: any, i: number) => {
                                  const label = m.form_type ? `SEC ${m.form_type}` : m.source || 'UNKNOWN';
                                  const detail = m.title || m.company_name;
                                  
                                  return (
                                    <a 
                                      key={i} 
                                      href={m.url || '#'} 
                                      target={m.url ? "_blank" : undefined} 
                                      rel={m.url ? "noopener noreferrer" : undefined}
                                      className="flex flex-col gap-1 text-[10px] font-mono bg-black/50 border border-white/5 p-2 hover:border-emerald-500/30 hover:bg-emerald-500/5 transition-colors group cursor-pointer max-w-[250px]"
                                    >
                                      <div className="flex items-center gap-2 text-slate-500 group-hover:text-emerald-400/70">
                                        <span className="text-emerald-500 font-bold">{m.ticker}</span>
                                        <span className="text-[8px] border border-white/10 px-1 py-0.5 rounded-sm uppercase">{label}</span>
                                        {m.score && <span className="text-[8px] opacity-50">{(m.score * 100).toFixed(0)}% Match</span>}
                                      </div>
                                      {detail && <span className="text-slate-400 truncate w-full group-hover:text-emerald-300 transition-colors">{detail}</span>}
                                    </a>
                                  );
                                })}
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                      
                      {result.mode === "AGENT" && result.data.final_recommendation && (
                        <div className="space-y-4">
                          {/* Final Recommendation Banner */}
                          <div className="border border-white/5 bg-black/20 p-4 flex flex-col gap-3">
                            <div className="flex justify-between items-start">
                              <div>
                                <div className="flex items-center gap-2 mb-1">
                                  <h3 className="text-sm font-mono text-purple-400 font-bold">{result.data.ticker} ANALYSIS</h3>
                                  <span className="text-[10px] font-mono px-2 py-0.5 border border-white/10 text-slate-400">
                                    CONFIDENCE: {(result.data.final_recommendation.confidence * 100).toFixed(0)}%
                                  </span>
                                  <span className="text-[10px] font-mono px-2 py-0.5 border border-white/10 text-slate-400 uppercase">
                                    HORIZON: {result.data.final_recommendation.time_horizon}
                                  </span>
                                </div>
                              </div>
                              <div className={`px-4 py-2 border font-mono font-bold text-lg shrink-0 ${result.data.final_recommendation.action === 'BUY' ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400' : result.data.final_recommendation.action === 'SELL' ? 'border-red-500/30 bg-red-500/10 text-red-400' : 'border-slate-500/30 bg-slate-500/10 text-slate-400'}`}>
                                {result.data.final_recommendation.action}
                              </div>
                            </div>
                            <p className="text-xs text-slate-300 leading-relaxed border-t border-white/5 pt-3">
                              {result.data.final_recommendation.rationale}
                            </p>
                          </div>
                          
                          {/* The 3 pillars: Fundamental, Momentum, Sentiment */}
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Fundamental */}
                            <div className="border border-white/5 bg-black/20 p-3 flex flex-col gap-2">
                              <div className="flex justify-between items-center border-b border-white/5 pb-2">
                                <h4 className="text-[10px] font-mono text-slate-400">FUNDAMENTAL</h4>
                                <span className="text-[10px] font-mono text-cyan-400">GRADE: {result.data.fundamental_analysis?.investment_grade}</span>
                              </div>
                              <p className="text-[10px] text-slate-400 leading-relaxed">
                                {result.data.fundamental_analysis?.overall_investment_thesis}
                              </p>
                            </div>
                            
                            {/* Momentum */}
                            <div className="border border-white/5 bg-black/20 p-3 flex flex-col gap-2">
                              <div className="flex justify-between items-center border-b border-white/5 pb-2">
                                <h4 className="text-[10px] font-mono text-slate-400">MOMENTUM</h4>
                                <span className="text-[10px] font-mono text-cyan-400">SCORE: {result.data.momentum_analysis?.momentum_score}/10</span>
                              </div>
                              <div className="flex flex-col gap-1.5 mt-1">
                                <div className="flex justify-between text-[10px] font-mono">
                                  <span className="text-slate-500">TREND:</span>
                                  <span className="text-slate-300 uppercase">{result.data.momentum_analysis?.overall_momentum}</span>
                                </div>
                                <div className="flex justify-between text-[10px] font-mono">
                                  <span className="text-slate-500">STRENGTH:</span>
                                  <span className="text-slate-300 uppercase">{result.data.momentum_analysis?.momentum_strength}</span>
                                </div>
                                <div className="flex justify-between text-[10px] font-mono">
                                  <span className="text-slate-500">OUTLOOK:</span>
                                  <span className="text-slate-300 uppercase">{result.data.momentum_analysis?.short_term_outlook}</span>
                                </div>
                              </div>
                            </div>

                            {/* Sentiment */}
                            <div className="border border-white/5 bg-black/20 p-3 flex flex-col gap-2">
                              <div className="flex justify-between items-center border-b border-white/5 pb-2">
                                <h4 className="text-[10px] font-mono text-slate-400">SENTIMENT</h4>
                                <span className="text-[10px] font-mono text-cyan-400">SCORE: {result.data.sentiment_analysis?.sentiment_score}/10</span>
                              </div>
                              <div className="flex justify-between text-[10px] font-mono mt-1">
                                <span className="text-slate-500">DIRECTION:</span>
                                <span className="text-slate-300 uppercase">{result.data.sentiment_analysis?.sentiment_direction}</span>
                              </div>
                              <p className="text-[10px] text-slate-400 leading-relaxed mt-1">
                                {result.data.sentiment_analysis?.market_outlook}
                              </p>
                            </div>
                          </div>
                          
                          {/* Opportunities and Risks from Final Recommendation */}
                          <div className="grid grid-cols-2 gap-4">
                            <div className="border border-white/5 bg-emerald-500/5 p-3">
                              <h4 className="text-[10px] font-mono text-emerald-500/70 mb-2">KEY OPPORTUNITIES</h4>
                              <ul className="list-disc pl-4 text-xs text-emerald-400/80 space-y-1">
                                {result.data.final_recommendation.key_opportunities?.map((o: string, i: number) => <li key={i}>{o}</li>)}
                              </ul>
                            </div>
                            <div className="border border-white/5 bg-red-500/5 p-3">
                              <h4 className="text-[10px] font-mono text-red-500/70 mb-2">KEY RISKS</h4>
                              <ul className="list-disc pl-4 text-xs text-red-400/80 space-y-1">
                                {result.data.final_recommendation.key_risks?.map((r: string, i: number) => <li key={i}>{r}</li>)}
                              </ul>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}

              </div>
            </div>

        </div>
    </div>
  );
}

