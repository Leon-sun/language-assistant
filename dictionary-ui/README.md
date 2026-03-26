# Dictionary Project — Next.js UI

Premium Linear-style / SaaS minimalist redesign of the Dictionary Project. Same content and structure as the Django app, with a dark Zinc palette, glassmorphism navbar, card-style sidebar, and refined typography.

## Stack

- **Next.js 15** (App Router)
- **Tailwind CSS** (Zinc palette, dark mode)
- **shadcn-style** components (Card, Button, Input, Label)
- **Lucide React** icons
- **Inter** font

## Run

```bash
npm install
npm run dev
```

Open [http://localhost:3001](http://localhost:3001).

## Structure

- **Layout:** Sticky navbar (glassmorphism), optional sidebar (hidden on mobile), main content `max-w-6xl`, footer
- **Pages:** Home, Lookup Word, Stories, About, Sign In, Sign Up
- **Components:** `Navbar`, `Sidebar`, `CardSection`, `WarningBanner`, `LookupForm`, `Footer`
- **i18n:** Client-side EN/FR via `LanguageProvider` and `t(lang, key)`

## Design

- **Navbar:** `bg-zinc-900/70 backdrop-blur-xl`, `border-b border-zinc-800`, active tab highlight
- **Sidebar:** Card-style links, `rounded-xl`, `border-zinc-700`, hover `border-zinc-600`, active left accent
- **Content:** Page header with icon, gradient accent bar, `text-3xl`/`text-4xl` titles
- **Warning callout:** `bg-zinc-800`, `border border-amber-500/30`, AlertTriangle icon
- **Forms:** Card-wrapped, inputs `bg-zinc-900 border-zinc-700`, primary button `bg-white text-zinc-900`
- **Micro-interactions:** `transition-all duration-200`, hover `scale-[1.01]` / `scale-[1.005]`, soft shadow

## Build

```bash
npm run build
npm start
```
