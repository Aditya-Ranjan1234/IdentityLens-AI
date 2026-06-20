---
name: Sentinel Core
colors:
  surface: '#0f1419'
  surface-dim: '#0f1419'
  surface-bright: '#353a40'
  surface-container-lowest: '#0a0f14'
  surface-container-low: '#171c22'
  surface-container: '#1b2026'
  surface-container-high: '#262a30'
  surface-container-highest: '#30353b'
  on-surface: '#dfe3ea'
  on-surface-variant: '#bec7d4'
  inverse-surface: '#dfe3ea'
  inverse-on-surface: '#2c3137'
  outline: '#88919d'
  outline-variant: '#3f4852'
  surface-tint: '#98cbff'
  primary: '#98cbff'
  on-primary: '#003354'
  primary-container: '#00a3ff'
  on-primary-container: '#00375a'
  inverse-primary: '#00629d'
  secondary: '#bdc7d9'
  on-secondary: '#27313f'
  secondary-container: '#404a59'
  on-secondary-container: '#afb9cb'
  tertiary: '#c3c6d4'
  on-tertiary: '#2c303b'
  tertiary-container: '#999caa'
  on-tertiary-container: '#30343f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#cfe5ff'
  primary-fixed-dim: '#98cbff'
  on-primary-fixed: '#001d33'
  on-primary-fixed-variant: '#004a77'
  secondary-fixed: '#d9e3f6'
  secondary-fixed-dim: '#bdc7d9'
  on-secondary-fixed: '#121c2a'
  on-secondary-fixed-variant: '#3d4756'
  tertiary-fixed: '#dfe2f1'
  tertiary-fixed-dim: '#c3c6d4'
  on-tertiary-fixed: '#171b26'
  on-tertiary-fixed-variant: '#434652'
  background: '#0f1419'
  on-background: '#dfe3ea'
  surface-variant: '#30353b'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  table-data:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

This design system is engineered for high-stakes environments where clarity and rapid response are paramount. The brand personality is **authoritative, technical, and vigilant**, designed specifically for Security Operations Centers (SOC) and Identity Governance and Administration (IGA) teams.

The design style follows a **Modern Corporate** approach with **Cyber-Technical** accents. It utilizes deep, low-light backgrounds to reduce eye strain during long monitoring shifts, while employing high-contrast "neon" functional colors to draw immediate attention to critical threats. The aesthetic prioritizes data density and information hierarchy, ensuring that complex identity relationships and security events are legible at a glance. Visual elements take inspiration from tactical interfaces, utilizing subtle grid patterns and micro-interactions that reinforce a sense of precision and control.

## Colors

The palette is optimized for a dark-mode-first ecosystem, utilizing a tiered navy and slate foundation to create clear spatial depth.

- **Primary (Cyber Blue)**: Reserved for primary actions, focus states, and active identity markers. It represents the "pulse" of the secure system.
- **Surface Tiers**: The core background uses Deep Navy (#0B0F19), while Slate (#1F2937) is utilized for cards, headers, and container separation to create a clear visual hierarchy.
- **Functional/Risk Colors**: These colors are strictly semantic. Danger Red is for critical breaches or unauthorized access; Warning Amber for anomalies or pending certifications; Success Green for healthy systems and verified identities.
- **Neutral/Text**: A scale of muted slates ensures that secondary data doesn't compete with primary alerts.

## Typography

The design system employs **Inter** for its exceptional legibility in data-heavy interfaces and high-density tables. For technical strings, such as IP addresses, machine IDs, and log timestamps, **JetBrains Mono** is introduced to provide a distinct visual "code" style that developers and security analysts expect.

- **Headlines**: Use tight letter spacing and semi-bold weights to convey authority.
- **Labels**: Technical labels and risk scores use the monospaced font in uppercase to differentiate system-generated data from user-generated content.
- **Scale**: Sizes are kept conservative (rarely exceeding 32px) to maximize the amount of information visible on dashboard screens without requiring excessive scrolling.

## Layout & Spacing

This design system utilizes a **12-column fluid grid** for analytical dashboards, allowing widgets to reflow based on the screen real estate of a SOC monitor.

- **Density**: The system defaults to a "compact" density model. A 4px base unit governs all padding and margins.
- **Dashboards**: Use a "Bento-box" layout style where widgets are grouped into logical containers with 16px gutters.
- **Sidebars**: A fixed 240px left-hand navigation persists for global identity modules, while right-hand drawers are used for "Inspect" views of specific security events.
- **Breakpoints**: Desktop (1440px+), Tablet/Small Monitor (1024px), and Mobile (768px). On mobile, data tables collapse into list-based cards.

## Elevation & Depth

In a dark security environment, depth is achieved through **Tonal Layering** and **Subtle Outlines** rather than heavy shadows.

- **Level 0 (Base)**: Deep Navy (#0B0F19) for the canvas.
- **Level 1 (Containers)**: Slate (#1F2937) with a 1px border of #2D3748. This is used for primary dashboard cards.
- **Level 2 (Modals/Popovers)**: A slightly lighter slate with a soft 15% opacity primary-colored outer glow to indicate high-focus interaction.
- **Indicators**: Active states utilize a "inner-glow" effect (0px 0px 8px) using the Primary Cyber Blue to simulate a backlit terminal screen.

## Shapes

The shape language is **Soft-Technical**. We use a 4px (0.25rem) base radius to maintain a professional, rigid feel while avoiding the harshness of 0px corners which can feel dated.

- **Buttons & Inputs**: Use the standard 4px radius.
- **Status Badges**: Use a "pill" shape (1rem+) to differentiate status indicators from interactive buttons.
- **Risk Gauges**: Utilize circular strokes and semi-circular arcs to break up the rectilinear layout of the grid.

## Components

- **Risk Score Meters**: Radial gauges that transition from Success Green to Danger Red based on a value of 0-100. Always accompanied by a trend arrow (up/down).
- **Identity Status Badges**: Small dots paired with labels (e.g., [● Active], [● Suspended]). The dot should pulse slightly for "In Progress" or "MFA Verification" states.
- **Data Density Tables**: Rows should have a hover state of #2D3748. Use monospaced fonts for ID columns. Include "Bulk Action" checkboxes that appear on hover or selection.
- **Network Connection Indicators**: Thin, 1px lines connecting nodes in identity maps, using animated "marching ants" or gradient flows to show direction of data/access privilege.
- **Buttons**:
    - *Primary*: Solid Cyber Blue with white text.
    - *Secondary*: Ghost style with Cyber Blue border.
    - *Destructive*: Solid Danger Red for "Revoke Access" or "Terminate Session."
- **Input Fields**: Darker than the container background to create an "inset" feel, with a Cyber Blue bottom-border focus state.
