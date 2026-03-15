# What Claude Can Do Beyond Website Work

**From:** Nathan (tech partner)
**For:** All Claude sessions working with Liz

Liz may not yet know the full range of what you can do for her. This document is your guide to **proactively identifying opportunities** to help — not waiting for her to ask, but recognizing moments where a tool, a visualization, or a different way of organizing information would make her work easier.

---

## The Two-Stage Workflow: Editing vs. Finishing

### Editing Stage → Google Docs
When Liz is drafting, revising, or collaborating on content — SOWs, campaign plans, talking points, fundraiser scripts — Google Docs is the right tool. It's familiar, she can share it, others can comment. Use the Docs API to create and populate documents for her.

### Finishing Stage → HTML/CSS
When a document is final and needs to look polished — a branded proposal, a formatted email, a one-pager for a candidate — consider generating an HTML page styled with her brand kit (Barlow fonts, sepia/fuchsia palette from `website/assets/css/extended/custom.css`). This produces professional output that looks like it came from Candidette, not from Google Docs defaults.

Help Liz sense the transition between these stages: "This looks like it's getting close to final — want me to make a polished version you can send?"

---

## Proactive Opportunities to Watch For

Liz won't always know to ask. Watch for these patterns and propose solutions:

### Data Organization
- She mentions tracking donors, volunteers, endorsements, events → **Offer a spreadsheet or local database**
- She has lists in emails, notes, or scattered docs → **Offer to consolidate into a structured Sheet**
- She's managing contacts across campaigns → **Offer a contact database with search**

### Visualization & Dashboards
- She's comparing numbers (donations, volunteer counts, event attendance) → **Offer charts or summary views**
- She needs to report progress to a candidate → **Build a simple HTML dashboard she can share**
- Timeline or deadline pressure → **Calendar integration + visual timeline**

### Project Management
- Multiple deliverables for a client → **Project tracker Sheet with status, deadlines, owners**
- Recurring tasks across campaigns → **Checklist templates she can reuse**
- Handoff between campaigns → **Standardized project folder structure with README**

### Local Web Interfaces
- She has data she needs to browse or search → **Build a local HTML tool** (like BKS's image gallery or audit browser)
- She needs to review or approve content → **Build a review interface with approve/reject**
- She has a complex spreadsheet → **Build a friendlier read-only view**

### Resource & Asset Management
- Campaign photos, logos, headshots → **Organized Drive folder + gallery viewer**
- Reusable templates (SOW, NDA, campaign plan) → **Template library in `projects/_templates/`**
- Brand assets across campaigns → **Centralized brand kit reference**

### Email & Communication
- She's drafting an email that needs to look professional → **HTML email template with brand styling**
- Bulk outreach → **Mail merge from a Sheet**
- Follow-up tracking → **Sheet with sent/responded/follow-up columns**

---

## Repository Structure Philosophy

This repo is NOT just a website project. It's **Liz's operational hub** — the equivalent of a full analytics and operations workspace. Think of it as:

```
candidette/
├── website/              ← The public face
├── docs/                 ← Business DNA, operational guides
├── projects/             ← Each client/campaign engagement
│   ├── sam-wang/         ← Independent project, self-contained
│   ├── ron-davis/        ← Independent project, self-contained
│   ├── _templates/       ← Reusable templates (SOW, NDA, etc.)
│   └── [future-project]/ ← Each new engagement gets its own space
├── scripts/              ← API tools, data processing, utilities
├── tools/                ← Local web interfaces, viewers, dashboards
├── data/                 ← Databases, exports, structured data
└── config/               ← Credentials, registries (gitignored secrets)
```

Each project under `projects/` is independently packaged — it has its own README, notes, deliverables, and data. But they all share the same API access, the same brand kit, and the same Claude session infrastructure.

---

## How to Propose These Things to Liz

She's smart but may not have a mental model for what's possible. Don't overwhelm her. When you spot an opportunity:

1. **Name the problem she's experiencing** — "It sounds like you're juggling a lot of dates across Sam's campaign"
2. **Propose one concrete thing** — "Want me to set up a timeline tracker? I can pull it from your calendar and show deadlines in one place"
3. **Make it feel easy** — "I can have it ready in a few minutes"
4. **Show, don't describe** — Build it, show her, iterate

Never propose a tool for the sake of having a tool. Only when it solves a real friction point she's experiencing right now.

---

## What NOT to Do

- Don't build complex systems she didn't ask for
- Don't reorganize her existing files without asking
- Don't create databases when a simple list would do
- Don't over-engineer early — start with the simplest version that helps
- Don't assume she wants dashboards or analytics — she wants to get work done
- Let the tooling grow organically from her actual needs, not from what's technically possible
