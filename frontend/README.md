# Cognitive Deception Frontend

Production-grade Next.js 14 interface for the **Cognitive Deception** adaptive honeypot platform.

## Stack

- Next.js 14 + React + TypeScript
- TailwindCSS + shadcn-style component architecture
- Framer Motion animations
- Recharts analytics charts
- Three.js (`@react-three/fiber`, `@react-three/drei`) for 3D globe
- Deck.gl + Mapbox-compatible rendering for attack paths

## UX Design Direction

- Palantir / cyber intelligence aesthetic
- Glassmorphism panels over deep dark background
- Neon blue + purple accents with high-contrast alert red
- Dense SOC-style information hierarchy with live telemetry behavior

## Implemented Pages

1. **Threat Intelligence Command Center** (`/dashboard`)
2. **Attacker Cognitive Profile** (`/attacker-analysis`)
3. **Deception Environment Generator** (`/deception-generator`)
4. **Attack Simulation Console** (`/attack-console`)
5. **Threat Intelligence Report** (`/threat-intelligence`)
6. **Network Topology** (`/network-topology`)

The root route (`/`) redirects to `/dashboard`. Legacy route modules remain in `frontend/views/` and can be deprecated later if needed.

## Run

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Environment

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Set Mapbox token to enable map basemap rendering:

```env
NEXT_PUBLIC_MAPBOX_TOKEN=...
NEXT_PUBLIC_MAP_STYLE=mapbox://styles/mapbox/dark-v11
```

Without token, Deck.gl still renders animated arc overlays on a dark cyber fallback canvas.

## Design Sources (MCP/Web curated)

- TailAdmin design system baseline: [https://tailadmin.com/](https://tailadmin.com/)
- NextAdmin enterprise dashboard patterns: [https://nextadmin.co/](https://nextadmin.co/)
- shadcn/ui component primitives: [https://ui.shadcn.com/](https://ui.shadcn.com/)
- Deck.gl ArcLayer visualization reference: [https://deck.gl/docs/api-reference/layers/arc-layer](https://deck.gl/docs/api-reference/layers/arc-layer)
- Cyber dashboard visual trend search: [https://dribbble.com/search/cybersecurity-dashboard](https://dribbble.com/search/cybersecurity-dashboard)
- Mapbox dark map examples: [https://docs.mapbox.com/mapbox-gl-js/example/](https://docs.mapbox.com/mapbox-gl-js/example/)

## Folder Structure

```text
frontend/
  app/
  components/
  hooks/
  pages/
  views/
  services/
  styles/
  visualizations/
```
