# NovaJet Private — The Sky, Redefined.
### Ultra-Luxury Private Jet Charter & Sovereign Membership Web Platform

**NovaJet Private** is an ultra-premium, client-ready web platform for an elite private aviation brand (level of NetJets, VistaJet, or Flexjet). Engineered with a cinematic, minimal, and high-performance design system communicating power, silence, precision, and privilege.

Visit Demo :- [https://novajet-private-day3.onrender.com/](https://novajet-private-day3.onrender.com/)

---

## Brand & Design System

- **Brand Name**: NovaJet Private
- **Tagline**: *The Sky, Redefined.*
- **Color Palette**:
  - Primary Backgrounds: Obsidian (`#030712`), Deep Midnight Navy (`#060E1A`, `#0A1628`), Elevated Slate (`#0F1F38`)
  - Subtle Background Accents: Radar avionics grid, luminous depth gradients, and low-opacity grain
  - Metallic Accents: Pure Platinum (`#FFFFFF`), Soft Cool Silver (`#E2E8F0`, `#F1F5F9`), Slate Muted (`#94A3B8`)
  - Precision Highlights: Electric Blue (`#3B82F6`, `#60A5FA`), Subtle Cyan (`#06B6D4`)
- **Typography**:
  - Display / Headings: `Syne` & `Plus Jakarta Sans`
  - Body: `Inter`
  - Avionics / Flight Codes / Monospace: `JetBrains Mono`
- **Atmosphere**: Quiet luxury, military-precision flight operations, glassmorphic HUD controls, acoustic silence.

---

## Key Website Features & Upgraded Capabilities

1. **Compact & Balanced Luxury Layout**:
   - Zero unnecessary black voids: Tightened vertical margins, refined section padding (70–80px), and continuous ambient radar grids.
   - High visual density with clean typographic hierarchy.

2. **3D Interactive Avionics Jet Viewer (Three.js WebGL)**:
   - Interactive 3D Flagship Jet model with swept wings, aft turbofans, rotating radar gimbal rings, and HUD coordinates.
   - Interactive mouse pitch/yaw tilt and touch controls.

3. **VIP User Authentication System (Django Auth)**:
   - Full user authentication with **Sign In**, **Register**, and **Sign Out**.
   - Asynchronous AJAX login/registration modals with seamless state changes without losing scroll position.
   - Navbar updates dynamically (shows "VIP [Username]" with active status dot when logged in).
   - Charter and membership inquiries automatically link to the logged-in user.

4. **Dedicated Developer Profile Page (`/developer/`)**:
   - High-end dark theme profile page for **MOHAMMED BILAL MANSURI** (Full Stack Web Developer - Python / Django).
   - Features exact profile photo, phone (`+919723918213`), email (`mansuribilal9792@gmail.com`), LinkedIn, GitHub, technical competencies, and direct inquiry buttons.
   - Accessible via the main navbar and footer.

5. **Flagship Fleet Showcase (Default Visible & 3D Tilt)**:
   - All private jet cards visible immediately on initial page load.
   - Category filtering pills: *All Flagships*, *Ultra Long Range*, *Heavy Jets*, *Super Midsize*, *Midsize*, *Light Jets*.
   - 3D CSS perspective card tilt on mouse move.
   - Verified authentic private jet photos with exterior, interior, range, Mach speed, capacity, and direct prefill booking.

6. **"Life on Board" Video & Cabin Sanctuary**:
   - Working direct aviation/jet flight video stream with working play/pause overlay controls.
   - High-resolution private jet luxury leather cabin poster image.
   - Interactive tabs for *Haute Gastronomy*, *Whisper-Quiet TrueZero™ Acoustics*, *Private Master Staterooms*, and *Worldwide Ka-Band Satellite Connectivity*.

7. **Coveted Destinations & Interactive Flight Calculator**:
   - Horizontal swipe track of global private hubs (London FAB, New York TEB, Dubai DWC, Geneva GVA, Nice NCE, Malé MLE, Tokyo HND, Aspen ASE).
   - Real-time Great Circle calculation returning distance, flight time, cruise altitude, and recommended aircraft class via `/api/route-calculator/`.

8. **Scroll-Triggered Performance Statistics**:
   - Animated odometer counters powered by GSAP ScrollTrigger (`150+` Fleet, `5,000+` Hubs, `99.8%` On-Time, `< 2h` Readiness).

9. **Sovereign Membership Tiers**:
   - *Access Tier* ($150k deposit), *Prestige Tier* ($300k deposit), and *Sovereign Tier* ($600k deposit) with comparison perks and modal application dossier.

10. **Empty Leg Live Marketplace**:
    - Real-time discounted repositioning flights with discount badges (-54% off) and one-click booking prefill.

11. **Django-Powered Charter Request Engine**:
    - Multi-trip selector: One-Way, Round-Trip, Multi-City, Empty Leg.
    - Fields: Route, Date, Departure Time, Passenger Count, Aircraft Class, Client Name, Email, Phone, Haute Catering, and Ground Transit.
    - Asynchronous AJAX submission with CSRF protection, generating a reference code (`NVJ-XXXXX`) and instant confirmation modal.
    - Stored in SQLite with User foreign key association.

12. **Accredited Luxury Footer**:
    - ARG/US Platinum, Wyvern Wingman, IS-BAO Stage 3, and Carbon Offset certification badges.
    - 24/7 Global Tactical Operations Command hotlines and Mayfair / Manhattan / DIFC dispatch centers.

---

## Technical Stack & CDNs

- **Backend**: Python 3.12, Django 5.1.5
- **Database**: SQLite with seeded models (`FleetAircraft`, `Destination`, `MembershipTier`, `EmptyLegDeal`, `CharterInquiry`, `MembershipInquiry`)
- **3D Engine**: Three.js WebGL (r128)
- **Animation & Motion**: GSAP 3.12.5 + ScrollTrigger + Lenis Smooth Scroll (v1.1.9)
- **Audio Synthesis**: Web Audio API (soothing 88Hz luxury cabin atmosphere hum)
- **CDNs Utilized**:
  - Three.js: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
  - Google Fonts: `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap`
  - Lenis Smooth Scroll: `https://cdn.jsdelivr.net/npm/lenis@1.1.9/dist/lenis.min.js`
  - GSAP Core: `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`
  - GSAP ScrollTrigger: `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js`

---

## Step-by-Step Local Setup & Execution

### 1. Run Migrations & Seed Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### 2. Start the Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```

### 3. Portal URLs
- **Main Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Developer Page**: [http://127.0.0.1:8000/developer/](http://127.0.0.1:8000/developer/)
- **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - **Username**: `admin`
  - **Password**: `novajet2026!`

---

## Developer Information
- **Name**: MOHAMMED BILAL MANSURI
- **Title**: Full Stack Web Developer (Python / Django)
- **Phone**: +919723918213
- **Email**: mansuribilal9792@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/mohammed-bilal-mansuri-972013204
- **GitHub**: https://github.com/mansuribilal-codes
