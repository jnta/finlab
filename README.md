# ⚡ FinLab

> **An AI-Native Financial Research Terminal**

FinLab is a modern, high-density financial analysis and research laboratory designed for speed, clarity, and deep synthesis. Built as a showcase portfolio application, it demonstrates the seamless integration of advanced AI workflows (RAG, agent-driven analysis) within a premium, responsive user interface.

## ✨ Showcase Features

- **AI-Native Synthesis:** Moves beyond raw data dumps by providing agent-driven analysis across Fundamental, Momentum, and Sentiment pillars.
- **Local RAG Integration:** Utilizes Qdrant as a vector database for semantic search over ingested financial documents and reports.
- **High-Density UI:** A terminal-like experience built with Next.js and Tailwind CSS, focusing on analytical clarity without legacy clutter.
- **Frictionless Interactions:** Smooth micro-animations powered by Framer Motion ensure the interface feels alive and responsive.
- **Concurrent Monorepo Architecture:** Clean separation of concerns with a FastAPI Python backend and a React/TypeScript frontend, orchestrated via a single development command.

## 🛠️ Technical Stack

**Frontend**
- **Framework:** Next.js 15+ (App Router, Server Components)
- **Styling:** Tailwind CSS (Custom dark-mode tailored palettes)
- **Animations:** Framer Motion
- **State/Data:** TanStack Query
- **Icons:** Lucide React

**Backend**
- **API:** FastAPI (Python 3.10+)
- **Vector DB:** Qdrant (Semantic search & document retrieval)
- **AI/LLM Integration:** Agent logic for deep-dive financial synthesis
- **Package Management:** `uv`

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://python.org/) (v3.10+)
- [`uv`](https://github.com/astral-sh/uv) (for blazing-fast backend dependency management)

### Installation

1. **Install frontend dependencies:**
   ```bash
   npm install
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   uv sync
   ```

### Running the Environment

Start both the Next.js frontend and the FastAPI backend concurrently from the root directory:

```bash
npm run dev
```

- **Frontend:** http://localhost:3000
- **Backend (API Docs):** http://localhost:8000/docs

*To run them separately:*
- Frontend: `npm run dev:frontend`
- Backend: `npm run dev:backend`

## 🧠 Design Philosophy

FinLab was built adhering to strict product principles outlined in its design specification:
1. **Data Density without Clutter:** Whitespace and typography guide the eye through rich financial information.
2. **Speed and Reliability:** Interactions are instantaneous, matching the fast-paced nature of financial data.
3. **Analytical Clarity:** Charts and metrics are unambiguous; insights are presented at a glance.
4. **Agentic Power:** AI is integrated naturally into the research workflow, acting as an active participant rather than a black-box tool.

---
*FinLab is developed as a portfolio showcase highlighting modern full-stack engineering, AI integrations, and premium UI/UX design.*
