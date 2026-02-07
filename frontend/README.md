# Dictionary Project - Documentation UI

A modern, premium documentation-style website UI built with React and Tailwind CSS, featuring glassmorphism effects and a dark gradient design.

## Features

- 🎨 **Premium Design**: Dark gradient background (navy → charcoal) with subtle noise texture
- 🔮 **Glassmorphism**: Semi-transparent cards with backdrop blur effects
- 📱 **Responsive Layout**: 2-column layout with sidebar navigation
- 🎯 **Reusable Components**: Navbar, Card, SectionBlock, ContentPanel
- ✨ **Teal Accents**: Elegant accent lines for active navigation items

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

```bash
npm run build
```

## Components

### Navbar
Top navigation bar with logo and menu items. Features glassmorphism and active state indicators.

### Card
Reusable card component with glassmorphism effects. Supports multiple variants (default, strong, subtle).

### SectionBlock
Vertical section navigation for the sidebar. Displays clickable section cards with active states.

### ContentPanel
Main content area with frosted-glass styling. Displays documentation content with proper typography.

## Styling

The design uses:
- **Background**: Dark gradient (navy → charcoal) with vignette and noise texture
- **Glassmorphism**: Semi-transparent backgrounds with backdrop blur
- **Typography**: Clean sans-serif, muted gray body text, bright white headings
- **Accents**: Teal gradient lines for active states and highlights
