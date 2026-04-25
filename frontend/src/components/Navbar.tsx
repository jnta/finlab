"use client";

import React from 'react';
import Link from 'next/link';
import { Brain, Search, Database, Settings, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

export const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black/50 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <motion.div 
            initial={{ rotate: -10 }}
            animate={{ rotate: 0 }}
            whileHover={{ rotate: 180, transition: { duration: 0.5 } }}
          >
            <Brain className="w-8 h-8 text-blue-500" />
          </motion.div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/50 tracking-tight">
            FinLab
          </span>
        </div>

        <div className="hidden md:flex items-center gap-8">
          <Link href="/search" className="text-sm font-medium text-white/70 hover:text-white transition-colors">Search</Link>
          <Link href="/analysis" className="text-sm font-medium text-white/70 hover:text-white transition-colors">Analysis</Link>
          <Link href="/research" className="text-sm font-medium text-white/70 hover:text-white transition-colors">Research</Link>
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 rounded-full hover:bg-white/5 text-white/70 hover:text-white transition-all">
            <Activity className="w-5 h-5" />
          </button>
          <button className="p-2 rounded-full hover:bg-white/5 text-white/70 hover:text-white transition-all">
            <Settings className="w-5 h-5" />
          </button>
          <div className="h-8 w-[1px] bg-white/10 mx-2" />
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 border border-white/20" />
        </div>
      </div>
    </nav>
  );
};
