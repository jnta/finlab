"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Search, Sparkles, TrendingUp, Zap, BookOpen, Layers } from 'lucide-react';

export default function Home() {
  return (
    <div className="relative isolate px-6 pt-14 lg:px-8 overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
        <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"></div>
      </div>

      <div className="mx-auto max-w-4xl py-32 sm:py-48 lg:py-56">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <div className="mb-8 flex justify-center">
            <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-white/60 ring-1 ring-white/10 hover:ring-white/20 transition-all flex items-center gap-2 bg-white/5">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span>Introducing the FinLab Intelligence Engine</span>
            </div>
          </div>
          
          <h1 className="text-6xl font-bold tracking-tight text-white sm:text-8xl bg-clip-text text-transparent bg-gradient-to-b from-white to-white/40">
            Next-Gen Finance.
          </h1>
          <p className="mt-8 text-lg leading-8 text-white/40 max-w-2xl mx-auto">
            The AI-native financial laboratory for deep market analysis. Synthesize massive datasets into actionable alpha through advanced neural search and RAG.
          </p>

          <div className="mt-12 flex items-center justify-center gap-x-6">
            <div className="relative group w-full max-w-xl">
              <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
              <div className="relative flex items-center bg-[#0a0a0a] rounded-xl border border-white/10 px-4 py-4">
                <Search className="w-5 h-5 text-white/40 mr-3" />
                <input 
                  type="text" 
                  placeholder="Analyze market trends with neural context..." 
                  className="bg-transparent border-none outline-none text-white w-full placeholder:text-white/20"
                />
                <div className="flex items-center gap-1 px-2 py-1 bg-white/5 rounded border border-white/10 text-[10px] text-white/40 font-mono">
                  <span>CMD</span>
                  <span>K</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Feature Grid */}
        <div className="mt-32 grid grid-cols-1 gap-6 sm:grid-cols-3">
          {[
            { icon: TrendingUp, title: "Active Projects", desc: "Linked to your current research focus.", color: "text-blue-400" },
            { icon: BookOpen, title: "Resource Vault", desc: "A curated library of financial deep dives.", color: "text-purple-400" },
            { icon: Layers, title: "PARA Structure", desc: "Organize by Projects, Areas, Resources, and Archives.", color: "text-emerald-400" },
          ].map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + i * 0.1 }}
              whileHover={{ scale: 1.02, backgroundColor: "rgba(255, 255, 255, 0.05)" }}
              className="p-6 rounded-2xl border border-white/5 bg-white/[0.02] backdrop-blur-sm transition-all"
            >
              <feature.icon className={`w-8 h-8 ${feature.color} mb-4`} />
              <h3 className="text-lg font-semibold text-white/90">{feature.title}</h3>
              <p className="mt-2 text-sm text-white/40 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]">
        <div className="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-20 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"></div>
      </div>
    </div>
  );
}
