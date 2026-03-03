# For Nathan

If you're reading this, you've identified yourself as Nathan. That changes how this conversation works.

**Communication mode**: Peer-level. Technical language is fine. You don't need analogies for git, Hugo, or infrastructure. Skip the guardrails — you built them. Be direct and concise.

---

## This Repo in Context

This repository (`BeatKitchen/candidette`) is under the umbrella of `BeatKitchen/beat-kitchen-analytics`. You can manage it from your machine, push workflow updates via your agent, and use beat-kitchen-analytics as the source of truth for system design decisions.

The candidette agent and your home base agent have already communicated via push/pull (see the commit history for the 2026-03-02 restructure). That pattern works — use it when you need to update instructions without being in this repo directly.

---

## Technical Scratchpad

### Submodule Sync (After Any Restructure)
When the PaperMod submodule path changes, run this sequence on each machine:
```
git pull
git submodule sync
git submodule update --init --recursive
```
Always in that order. `sync` picks up the new path from `.gitmodules` before `update` tries to initialize.

### Hugo Dev Server
Always run from `website/`, not the repo root:
```
cd website && hugo server --bind 0.0.0.0
```
`--bind 0.0.0.0` makes it accessible from other devices on the network (useful for mobile preview).

### Netlify (When Ready)
Not configured yet. When you set it up:
- Base directory: `website`
- Build command: `hugo --minify`
- Publish directory: `website/public`
- Connect to `BeatKitchen/candidette` on GitHub, branch `main`
- Target domain: candidette.com (replace Squarespace)
- Update `website/hugo.toml` baseURL from `http://localhost:1313/` to `https://candidette.com/`

### Git Token
The remote URL has a hardcoded PAT embedded in `.git/config` on both machines. Low risk for now (private repo, local config only) but worth rotating and switching to SSH or macOS Keychain credential helper when you have a moment. Not urgent.

### Local Clone Locations
- **Laptop**: `~/Developer/candidette` — cloned 2026-03-02, clean
- **Mac mini**: `/candidette` on the Mac mini's own drive (previously accessed from laptop via network mount at `/Volumes/elizabethrosenberg/candidette`) — pull the restructure and run submodule sync

### Desktop Launcher — Replicate on Mac Mini
A symlink was created on the laptop Desktop pointing to the workspace file:
```
~/Desktop/Candidette Campaigns.code-workspace -> ~/Developer/candidette/candidette.code-workspace
```
Use absolute paths to avoid broken symlinks:
```
ln -sf /Users/elizabethrosenberg/Developer/candidette/candidette.code-workspace ~/Desktop/"Candidette Campaigns.code-workspace"
```
**Do the same on the Mac mini after pulling.** Adjust the path to wherever the local clone lives on that machine:
```
ln -sf /path/to/candidette/candidette.code-workspace ~/Desktop/"Candidette Campaigns.code-workspace"
```

### Where Liz Might Go Looking
We don't know for certain where she'll start from. Cover multiple bases:
1. **Desktop** — done on laptop, needs to be done on Mac mini
2. **The repo folder itself** — `candidette.code-workspace` already lives at the repo root, so if she navigates there in Finder she can click it directly
3. **Anywhere she was editing before** — she previously found and edited markdown files directly from the Mac mini. Consider dropping an additional symlink in her home folder (`~/"Candidette Campaigns.code-workspace"`) or wherever she tends to land first, so no matter where she starts she sees one click to the right place

The goal: no matter where she is in Finder, she should be able to find something to click that opens VS Code correctly. One click, no navigation.

### projects/ Directory
Empty now. When Liz takes on a client or campaign, docs for that engagement go in `projects/<campaign-name>/`. Keeps everything under one roof without cluttering the website or business docs.

### config/ Directory
Gitignored (except `.gitkeep`). Use for API keys, credentials, anything that shouldn't be committed. Currently empty.

---

## Design Decisions (For Reference)

**beatkitchen.io** is the design reference. Nathan and Paul built it over ~1 year — Hugo + CSS, deployed on Netlify. The structural principles (layout hierarchy, typography, mobile-first) are worth adapting. The advanced infrastructure (React, Railway, Discord bot, dynamic pricing, Google Sheets integration) is not relevant to Liz's site.

**Theme decision**: Start with PaperMod configured, not a custom theme. Rationale: Liz needs to see a working site quickly before she'll invest in refining it. Design can evolve with custom CSS overrides or a theme swap once content is in place. The worst outcome is 5 sessions on design with nothing live.

---

## Pushing Workflow Updates From Your Machine

When the system design evolves (new phases, updated instructions, revised protocol), push changes from beat-kitchen-analytics using the same agent-to-agent pattern from 2026-03-02: write a document, push, tell the candidette agent to pull and review. It worked cleanly.

---

*Created 2026-03-02. Update this file when technical decisions change or new scratchpad items come up.*
