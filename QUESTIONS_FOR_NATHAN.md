# Questions for Nathan

This document was created during a session on 2026-03-02 to capture what didn't carry over cleanly from Nathan's original workflow design. Nathan will read this from his own repository, push updates, and we'll reconcile afterward.

---

## 1. Single Entry Point vs. Multiple Docs

**What happened:** A previous Claude session created `CLAUDE.md` as a separate behavioral rules file. Your design intent appears to be `START_HERE.md` as the single entry point that branches to everything.

**Question:** Should `CLAUDE.md` be eliminated and its contents folded into `START_HERE.md`? Or is there a reason to keep them separate that I'm not seeing?

---

## 2. Session Naming / Window Title Workflow

**What I understand so far:**
- The VS Code window title names the session
- That title flows into the commit message at the end of the session
- If the title is already set when a session opens, skip the preamble and dive in
- If no title, ask "What are we working on today?" — both to orient and to label the commit

**What's not documented:**
- How does Liz set the window title? (File > Save Workspace As...? You set it? Something else?)
- Is there a specific format for the title, or just whatever she says naturally?
- What happens if she opens a session mid-task with no clear label — is there a fallback?

---

## 3. Your Original Repository

**Question:** What is the URL or location of the "original repository" you mentioned — the one that contains your intended workflow design? Once you push updates there, I'll need to know where to pull from or what to compare against.

---

## 4. Your Website as Design Reference

**What I understand:** You and your designer Paul have built a Hugo + CSS static site over the past year. You want to use it as a reference for Liz's site — not the advanced parts (React, Railway, etc.), but the layout principles, typography, and structure.

**Question:** What is the URL of your site? I'll audit it the same way I audited candidette.com so we have a clear sense of what to adapt.

---

## 5. Theme Decision

**Current state:** PaperMod is installed as a git submodule and fully present. The `hugo.toml` still has placeholder values ("My New Hugo Project," example.org baseURL).

**Question:** Is PaperMod the intended theme for Liz's site, or do you want to replace it with something derived from your site's approach? This affects whether we configure PaperMod or strip it out and start from your CSS foundation.

---

## 6. Netlify Deployment

**Question:** Has a Netlify site already been connected to this repository? If so, what's the target domain — candidette.com replacing the current Squarespace, or a staging URL for now? I want to make sure any `hugo.toml` baseURL I set doesn't break a live deployment.

---

## 7. Staged but Uncommitted Files

**Current state:** Two files are staged but not committed: `archetypes/default.md` and `hugo.toml` (the placeholder version). The branch is also 1 commit ahead of `origin/main` (the onboarding commit was never pushed).

**Question:** Want me to clean this up — commit the staged files and push everything to sync the remote — before you push your workflow updates? Or do you want to handle the push from the Mac mini side first?

---

*Created by Claude, 2026-03-02. To be resolved when Nathan pushes updated workflow from his repository.*
