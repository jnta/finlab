"use client";

import React, { useState, useEffect } from 'react';

export const Navbar = () => {
  const [systemHealth, setSystemHealth] = useState<"OPTIMAL" | "DOWN" | "POLLING">("POLLING");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/health", { method: "GET" });
        if (res.ok) {
          setSystemHealth("OPTIMAL");
        } else {
          setSystemHealth("DOWN");
        }
      } catch (error) {
        setSystemHealth("DOWN");
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="flex-none flex items-center justify-between px-4 py-3 border-b border-white/5 bg-[#020617]">
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.8)] animate-pulse"></div>
          <span className="font-bold text-white tracking-wider text-sm">FINLAB.OS</span>
        </div>
        <nav className="hidden md:flex items-center gap-4 text-[11px] font-mono tracking-wider">
          <button className="text-cyan-400 font-semibold border-b border-cyan-400 pb-1">RESEARCH LAB</button>
        </nav>
      </div>
      <div className="flex items-center gap-4 text-xs font-mono">
        <div className="flex items-center gap-2 text-slate-500">
          <span className={`w-1.5 h-1.5 rounded-full ${systemHealth === 'OPTIMAL' ? 'bg-emerald-500' : systemHealth === 'DOWN' ? 'bg-red-500 animate-pulse' : 'bg-yellow-500 animate-pulse'}`}></span>
          SYSTEM: <span className={`${systemHealth === 'OPTIMAL' ? 'text-emerald-400' : systemHealth === 'DOWN' ? 'text-red-400 font-bold' : 'text-yellow-400'}`}>{systemHealth}</span>
        </div>

      </div>
    </header>
  );
};
