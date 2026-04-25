# FinLab Design System

## The "Terminal" Aesthetic
FinLab's UI is an AI-native financial laboratory. It eschews generic SaaS "dashboard" tropes (pastel colors, rounded pill buttons, side-stripe borders) in favor of a high-density, authoritative, terminal-inspired interface. It prioritizes data legibility, low-latency UI performance, and professional gravitas.

## 1. Color Palette

### Backgrounds
* **App Canvas:** `bg-[#030712]` - Deep, near-black space for maximum contrast.
* **Panels / Cards:** `bg-[#0a0f1c]` - Subtle elevation for data containers.
* **Header / Navigation:** `bg-[#020617]` - Extremely dark slate for structural framing.
* **Hover States:** `hover:bg-slate-800/30` - Barely perceptible lightening for interactivity.

### Text
* **Primary Headers / High-Value Data:** `text-white`
* **Body / Standard Text:** `text-slate-300`
* **Metadata / Labels / Secondary Data:** `text-slate-400`
* **Disabled / Lowest Priority:** `text-slate-500`

### Accents & Signals
* **Primary / Active Agent / Cybernetic:** `cyan-400` (e.g., `text-cyan-400`, `bg-cyan-400`, `border-cyan-400`)
* **Positive Alpha / Online / Success:** `emerald-400` / `emerald-500`
* **Negative / Drawdown:** `red-400`

## 2. Typography
We utilize a stark duality between modern sans-serif and utilitarian monospace.

* **Sans-Serif (`font-sans`):** Used for narrative text, standard body copy, and UI controls. (Geist Sans)
* **Monospace (`font-mono`):** Used for **all** financial data, ticker symbols, timestamps, agent logs, system status, and column headers. (Geist Mono)
* **Letter Spacing:** Monospace labels often use `tracking-wider` or `tracking-widest` to evoke a command-center aesthetic (e.g., `text-[10px] tracking-wider uppercase`).

## 3. Layout & Structure
* **Grid First:** The UI relies on rigid CSS Grids (e.g., `grid-cols-2 md:grid-cols-4`, `grid-cols-12`) to manage high data density without clutter.
* **Borders over Shadows:** Depth is established via crisp, 1px borders (`border-white/5` or `border-white/10`), not drop shadows.
* **Density:** Padding is tight (`p-3`, `px-4 py-2`). Information is compressed but strictly aligned. Semantic HTML tables (`<table className="w-full">`) are preferred over arbitrary flex rows for structured list data.
* **Corner Radius:** Avoid heavy rounding. Use sharp corners or minimal rounding (`rounded`, `rounded-sm`) for inputs and internal badges.

## 4. Interaction & Motion
* **Hover States:** Subtle background shifts (`hover:bg-white/5` or `hover:bg-slate-800/30`) or text color brightens (`text-slate-400 hover:text-white`).
* **Focus States:** Neural/cybernetic glow effects for critical inputs. 
  * Example: `focus-within:border-cyan-500/50 focus-within:shadow-[0_0_15px_rgba(34,211,238,0.1)]`
* **Micro-animations:** Use `animate-pulse` sparingly on crucial status indicators (e.g., system online dot, active agent glowing badge) to make the UI feel "alive".

## 5. Anti-Patterns (STRICTLY FORBIDDEN)
* **No Side-Stripe Borders:** Do not use 2px colored left/right borders to indicate status on rows. Use leading icons, dots, or full row tinting.
* **No "Hero" Metric Cards:** Do not use giant singular numbers in a massive white box with a drop shadow. Data must be dense and contextualized.
* **No Pastel Accents:** Avoid soft purples, pinks, or generic blue gradients unless specifically modeling a data chart. 
