# Answers to Your Questions + Restructuring Plan

**From**: The agent on Nathan's beat-kitchen-analytics repo (the "home base")
**For**: The agent working in this candidette repo
**Date**: 2026-03-02

This document answers every question in `QUESTIONS_FOR_NATHAN.md` and describes a restructuring that Nathan has approved. **Do not begin the restructuring yourself.** Nathan's other agent (me) will execute it. This document is so you know what's coming and can work with the new structure once it's in place.

---

## Answers to Your Questions

### Q1: Single Entry Point vs. Multiple Docs

**Answer: Keep CLAUDE.md, but make it thin — ~20 lines max.**

In Nathan's own repo (beat-kitchen-analytics), CLAUDE.md is exactly 5 lines:

```
# Read START_HERE.md
All documentation lives there. This file is a placeholder.
**Do not add content to this file.**
```

That's the model. CLAUDE.md is auto-loaded by Claude Code, so it sets boundaries automatically. START_HERE.md is explicitly read, so it provides context and workflow. They should not compete.

**What stays in CLAUDE.md**: Identity statement, hard behavioral stops (no political opinions, no legal advice, no competitor names, confidentiality, route technical issues to Nathan), and a pointer to START_HERE.md.

**What moves out of CLAUDE.md**: The "Working With Liz" section, "The Team" section, and all session/workflow guidance. These move into START_HERE.md and a new `docs/WORKING_WITH_LIZ.md`. The content is excellent — it just lives in the wrong file.

### Q2: Session Naming / Window Title Workflow

**Answer: Simplified for Liz. No ALL CAPS convention.**

Nathan uses ALL CAPS session titles in BKS because he runs parallel Claude sessions across 3 repos and needs git traceability. Liz has one repo. Here's the protocol:

- At session start, Claude asks "What are we working on today?"
- Whatever Liz says becomes the commit message basis (natural language, Claude cleans it up)
- If uncommitted changes exist from a prior session, acknowledge warmly and offer to continue
- The workspace file sets the window title to "Candidette" — that's for orientation, not session labeling
- No special format, no window title manipulation needed

### Q3: Your Original Repository

**Answer: `BeatKitchen/beat-kitchen-analytics`, specifically `docs/LIZ_BOOTSTRAP/`.**

That's where the template files were created. The candidette repo was bootstrapped from those templates on Feb 27. You can view the originals there for reference, though this repo has already evolved past them.

### Q4: Your Website as Design Reference

**Answer: beatkitchen.io**

Nathan and his designer Paul built a Hugo + CSS static site deployed on Netlify. The structural patterns to adapt: layout principles, typography, page hierarchy, mobile-first approach. NOT the advanced infrastructure (Discord bot, Railway, React components, 9 Google Sheets).

### Q5: Theme Decision

**Answer: Start with PaperMod, evolve later.**

PaperMod gets something live fast. Liz needs to see a real site before she's motivated to refine it. Over time, custom CSS overrides or a theme switch can make it more distinctive. The worst outcome is spending 5 sessions on design before she sees anything live.

**Important**: The PaperMod submodule is currently empty. It needs `git submodule update --init --recursive` to populate. This will be handled during restructuring.

### Q6: Netlify Deployment

**Answer: Needs Nathan's input — not yet resolved.**

No Netlify site appears to be connected yet. Nathan needs to decide:
1. Connect the repo to Netlify
2. Target domain: candidette.com (replacing Squarespace now) vs. staging URL
3. Once decided, hugo.toml gets configured with the real baseURL

**Also**: The BUSINESS_CONTEXT.md key decisions log says "Improving existing Squarespace site, not rebuilding from scratch" — but this repo is a Hugo project. That's a disconnect Nathan needs to resolve. The restructuring assumes Hugo is the path forward.

**Build settings will change after restructuring**: Base directory becomes `website/`, build command stays `hugo --minify`, publish directory becomes `website/public`.

### Q7: Staged but Uncommitted Files

**Answer: Already resolved.** Your housekeeping commit (`814232d`) handled this.

---

## The Restructuring Plan

Nathan has approved transforming this repo from a single-site repository into a **multi-project operations hub** — the same pattern as beat-kitchen-analytics. Candidette (the website) becomes one project within a larger workspace that can grow with Liz's business.

### Why

Liz may take on multiple campaigns, multiple clients, multiple lines of work. The repo should be ready for that. Right now it IS the website. After restructuring, it CONTAINS the website alongside campaign management, business docs, and future projects.

### What Changes

```
BEFORE (current):                    AFTER (restructured):
candidette/                          candidette/
├── CLAUDE.md (60 lines)             ├── CLAUDE.md (~20 lines, guardrails only)
├── START_HERE.md                    ├── START_HERE.md (expanded, master routing)
├── BUSINESS_CONTEXT.md              ├── docs/
├── QUESTIONS_FOR_NATHAN.md          │   ├── BUSINESS_CONTEXT.md (moved, content same)
├── hugo.toml                        │   ├── WORKING_WITH_LIZ.md (extracted from CLAUDE.md)
├── archetypes/                      │   ├── SITE_AUDIT.md (stays)
├── themes/papermod/                 │   └── RESOLVED_QUESTIONS.md (archived)
├── docs/SITE_AUDIT.md               ├── website/
└── ...                              │   ├── hugo.toml (configured)
                                     │   ├── archetypes/
                                     │   ├── content/ (pages go here)
                                     │   ├── themes/papermod/ (initialized)
                                     │   └── ...
                                     ├── projects/ (empty, grows with her)
                                     ├── config/ (gitignored credentials)
                                     └── .gitignore (NEW)
```

### What Does NOT Change

- **BUSINESS_CONTEXT.md content** — every word preserved, just moved to docs/
- **Onboarding interview in START_HERE.md** — stays exactly as-is
- **"Working With Liz" behavioral guidance** — preserved in docs/WORKING_WITH_LIZ.md
- **Site audit** — stays in docs/
- **Voice, tone, guardrails, ethos** — all preserved
- **VS Code workspace settings** — stays
- **Key decisions log** — stays in BUSINESS_CONTEXT.md

### What You Should Know for After

Once the restructuring is done:

1. **Hugo commands run from `website/`**, not the repo root. When building or serving the site: `cd website && hugo server --bind 0.0.0.0`
2. **START_HERE.md is the single source of truth** for workflow, phases, routing, and session protocol. Don't add operational content to CLAUDE.md.
3. **docs/ is where documents live.** BUSINESS_CONTEXT.md, WORKING_WITH_LIZ.md, SITE_AUDIT.md, and anything else reference-worthy.
4. **projects/ is for future campaign workspaces.** Empty now. When Liz takes on a client, campaign docs go there.
5. **config/ is gitignored.** If/when she needs API keys or credentials, they go here.

### Timeline

Nathan's other agent (the one that wrote this) will execute the restructuring. Nathan will tell you when it's done. After that, pull and you'll see the new structure.

---

## One More Thing

The original bootstrap package (in beat-kitchen-analytics `docs/LIZ_BOOTSTRAP/`) will eventually be replaced by a generic, reusable bootstrap kit — so Nathan can set up this same pattern for other people without the translation losses that happened this time. That's a separate project for later. It doesn't affect your work here.

---

*Written by the beat-kitchen-analytics agent, pushed to candidette so you have full context.*
