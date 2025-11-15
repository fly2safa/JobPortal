## Presentation Prep Checklist

This checklist builds on `presentation-guidelines.md` and focuses on how to turn it into a polished, 20-minute live presentation plus 10-minute Q&A.

---

### 1. Map Sections to Concrete Slides

Target: **12–14 slides** total.

- **Slide 1 – Title**
  - Project name (TalentNest), one-line pitch, your name(s), course, ASU / Revature.
- **Slide 2 – Agenda**
  - Bullets: Why → Demo → How (Architecture & AI) → Costs → Lessons → Q&A.
- **Slide 3 – The Opportunity (Why)**
  - 3–4 bullets: pain points for job seekers and employers; why a smarter portal.
- **Slides 4–6 – Live Demo Support**
  - Slide: Job Seeker journey (high-level flow).
  - Slide: Employer journey.
  - Optional: Key AI touchpoints (resume parsing, recommendations, matching).
- **Slides 7–9 – System Architecture & Data Model**
  - Frontend architecture diagram.
  - Backend / services architecture diagram.
  - ERD / data model.
- **Slide 10 – AI Engine**
  - Simple diagram of RAG + recommendations + candidate matching pipeline.
- **Slide 11 – AI Cost Simulation**
  - Small, clear table with Launch / Growth / Scale cost scenarios.
- **Slide 12 – Cost-Control Strategy**
  - 3 bullets: process-once-store-forever, caching, tiered models / fallbacks.
- **Slide 13 – Lessons & Known Issues**
  - 2–3 lessons, 1–2 honest known limitations.
- **Slide 14 – Thank You / Q&A**
  - Clean slide with logo and “Questions?”.

---

### 2. Script a Strict Live Demo Path

Prepare a one-page script for your demo:

- **Job Seeker flow:**
  - Login → Profile → Resume upload → Job search → Apply → AI recommendations.
- **Employer flow:**
  - Login → Post job → View applications → AI candidate recommendations → Schedule interview.

Guidelines:
- Keep the flow **identical** every rehearsal to avoid surprises.
- As you click, narrate *value*, not just actions:
  - “Here the AI parses the resume and highlights key skills…”
  - “This recommendation card is powered by vector search + LLM scoring…”

---

### 3. Export and Insert Diagrams

From the root `README.md`:

- Export as images (PNG/SVG) using a Mermaid-capable viewer:
  - System Architecture diagram.
  - Frontend Architecture diagram.
  - ERD / MongoDB Schema diagram.
  - System Flow diagram (optional).

Then:
- Place **one diagram per slide**.
- Add a **one-sentence explanation** per diagram (keep text light).

---

### 4. Apply Light Visual Polish

- Reuse **TalentNest branding**:
  - Bird + wordmark on Title and Q&A slides.
  - Primary blue as accent color for headings / key icons.
- Use a **consistent layout**:
  - Same title position and font.
  - Similar spacing and bullet style.
- Add simple icons where helpful:
  - 👤 for job seeker, 🏢 for employer, 🧠 for AI, 🗄️ for database, 💲 for costs.

Goal: clean, modern, not cluttered.

---

### 5. Time and Rehearse

Target timing:

- **2–3 min**: Opportunity + Agenda.
- **10 min**: Live demo (majority of time).
- **5 min**: Architecture + AI + Costs.
- **2–3 min**: Lessons + Q&A intro.

Rehearsal tips:
- Do at least **2–3 timed run-throughs**.
- Practice transitions explicitly:
  - “You’ve just seen what the platform does for seekers and employers. Now I’ll show you how it works under the hood.”
  - “Now that we’ve seen how the AI behaves, let’s talk about what it costs and how we control that.”

---

### 6. Prepare Backup Plans

For the demo:
- Capture **screenshots** of key flows (seeker and employer journeys).
- Optionally record a **short demo video** (screen capture).

If something fails live:
- Use screenshots or video while explaining what *would* happen.
- Keep debugger / logs **closed** during the main demo; only open if specifically asked in Q&A.

---

### 7. Final Pre-Presentation Checklist

- [ ] Slides complete and in correct order.
- [ ] Diagrams export cleanly and are readable on a projector.
- [ ] Demo environment tested (backend + frontend + DB + env vars).
- [ ] At least 2 timed rehearsals completed within ~20 minutes.
- [ ] Clear handoff to Q&A at the end (“Thank you. What questions do you have?”).


