# SenseBio Design Guidelines

## Design Approach
**System-Based**: Medical/Healthcare Dashboard utilizing Material Design principles for data visualization applications with emphasis on real-time monitoring clarity and status communication.

## Core Design Principles
1. **Clarity First**: Real-time data must be instantly readable
2. **Status Communication**: Color-coded system for immediate health status recognition
3. **Professional Medical Aesthetic**: Clean, trustworthy, scientific appearance
4. **Data Hierarchy**: Live value prominence over historical trends

---

## Typography

**Font Stack**: 
- Primary: 'Inter', 'Segoe UI', system-ui, sans-serif (via Google Fonts CDN)
- Monospace: 'JetBrains Mono', monospace (for numerical displays)

**Hierarchy**:
- Main Heading (SenseBio): 2.5rem (40px), weight 700
- Real-time Value Display: 4rem (64px), weight 700, monospace
- Unit Labels: 1.25rem (20px), weight 500
- Status Text: 1rem (16px), weight 600
- Chart Labels: 0.875rem (14px), weight 400
- Footer: 0.75rem (12px), weight 400, italic

---

## Layout System

**Spacing Units**: Tailwind scale - primary units: 4, 6, 8, 12, 16, 24
- Container padding: p-6 to p-8
- Card padding: p-8
- Section gaps: space-y-6
- Element margins: mb-4, mb-6

**Structure**:
- Full viewport height layout with centered content
- Maximum content width: 1200px (max-w-6xl)
- Single-column card-based layout
- White background (#FFFFFF) with subtle shadow elevation

---

## Color System

**Primary Palette**:
- Neon Blue Accent: #00D9FF (primary CTAs, highlights)
- Deep Blue: #0099CC (secondary accents)
- White: #FFFFFF (background, cards)
- Light Gray: #F8F9FA (subtle backgrounds)
- Text Dark: #1A1A1A (primary text)
- Text Gray: #6B7280 (secondary text)

**Status Indicators**:
- Normal (5-18 ng/mL): #10B981 (Emerald Green)
- Low (<5 ng/mL): #F59E0B (Amber Yellow)
- High (>18 ng/mL): #EF4444 (Red)

---

## Component Library

### 1. Main Dashboard Card
- White background with shadow (shadow-2xl)
- Rounded corners (rounded-2xl)
- Padding: p-8
- Center-aligned content
- Border: subtle 1px border in light gray

### 2. Real-time Value Display
- Large monospace numerals (4rem)
- Neon blue color (#00D9FF)
- Unit display in lighter weight adjacent to value
- Dynamic background glow effect matching status color
- Padding: p-6, rounded container

### 3. Status Indicator Badge
- Pill-shaped badge with status color background
- White text, weight 600
- Padding: px-4 py-2
- Positioned above or below value display
- Text: "Normal", "Low Cortisol", or "High Cortisol"

### 4. Chart Container
- Chart.js line chart
- Height: 400px on desktop, 300px on mobile
- Grid lines: subtle light gray
- Line color: Neon blue (#00D9FF) with gradient fill
- Point markers: visible, 4px radius
- Axis labels: 12px, gray text
- Background: transparent

### 5. Header Section
- Logo/title area: text-center, mb-8
- Title size: 2.5rem, weight 700
- Subtitle: "Real-time Hormone Monitoring Prototype"
- Color: Deep blue (#0099CC)

### 6. Footer
- Fixed to bottom or positioned below chart
- Text-center, small italic text (0.75rem)
- Gray color (#6B7280)
- Padding: py-4
- Border-top: 1px solid light gray
- Text: "SenseBio Prototype — Not a medical device"

---

## Responsive Behavior

**Desktop (1024px+)**:
- Card max-width: 1000px, centered
- Chart height: 400px
- Padding: generous (p-8)

**Tablet (768px - 1023px)**:
- Card max-width: 720px
- Chart height: 350px
- Padding: p-6

**Mobile (<768px)**:
- Full-width card with margin
- Chart height: 300px
- Value display: 3rem instead of 4rem
- Padding: p-4

---

## Animations
**Minimal & Purposeful**:
- Value update: subtle fade transition (0.3s)
- Status badge change: color transition (0.5s ease)
- Chart: smooth line animation on load only
- NO continuous pulsing or distracting animations

---

## Images
**No hero images required** - This is a data dashboard application focused on real-time monitoring. Visual emphasis should be on the data display and chart visualization, not decorative imagery.

---

## Icons
**Library**: Heroicons (via CDN)
- Activity icon for real-time indicator (animated pulse dot)
- Clock icon for timestamp display
- Alert icons for status warnings (if applicable)