# FinLab Monorepo

Welcome to the FinLab project, an AI-native financial analysis and research laboratory.

## Structure

- `backend/`: FastAPI application (Python)
- `frontend/`: Next.js application (TypeScript, Tailwind, Framer Motion)

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- `uv` (for backend package management)

### Installation

1. Install frontend dependencies:
   ```bash
   npm install
   ```

2. Install backend dependencies (using `uv`):
   ```bash
   cd backend
   uv sync
   ```

### Running the Project

You can run both the frontend and backend concurrently from the root:

```bash
npm run dev
```

Alternatively, run them separately:

- **Frontend**: `npm run dev:frontend`
- **Backend**: `npm run dev:backend`

## Tech Stack

### Backend
- **FastAPI**: Modern, fast (high-performance) web framework.
- **Qdrant**: Vector database for RAG.
- **Search API**: Integration with financial data sources.

### Frontend
- **Next.js 15+**: App Router, Server Components.
- **Tailwind CSS**: Modern styling.
- **Framer Motion**: Smooth animations.
- **Lucide React**: Beautiful icons.
- **TanStack Query**: Efficient data fetching.
