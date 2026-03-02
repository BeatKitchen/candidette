# Notes for the Restructuring Agent

**From**: The agent working in this candidette repo (Liz's laptop session, 2026-03-02)
**For**: The beat-kitchen-analytics agent executing the restructure
**Re**: Remaining decisions + one correction + sync protocol

---

## Decisions Resolved by Nathan

### Squarespace vs. Hugo
Squarespace stays live and untouched until the Hugo site is built and tested locally. No cutover, no domain changes, no Netlify setup yet. Nathan will configure Netlify when ready. For now:
- `hugo.toml` baseURL should be set to `http://localhost:1313/` for local development
- The key decisions log in BUSINESS_CONTEXT.md should be updated to reflect: "Rebuilding as Hugo site; Squarespace remains live during development; Netlify deployment is Nathan's responsibility when ready"

### Workspace Structure
The `candidette.code-workspace` file stays at repo root and opens the umbrella workspace — that's correct. **START_HERE.md must make it unmistakably clear** that website files live in `website/` and that all Hugo commands run from there. Liz should never have to navigate the folder structure or think about where things live. START_HERE.md is the router. It should tell her (and Claude) exactly where to go for each type of task.

### Netlify
Not configured yet. Nathan will handle it. No action needed during restructure.

---

## One Correction

**PaperMod is already initialized** in the local clone at `~/Developer/candidette`. It was cloned with `--recurse-submodules` and is fully populated. Do not re-initialize. If you're moving it to `website/themes/papermod/`, the submodule reference in `.gitmodules` will need to be updated to reflect the new path. Handle that carefully — a broken submodule path is invisible until Hugo tries to build.

---

## Sync Protocol (Critical — Please Encode This)

Nathan flagged that even he gets confused about when the repo is in sync. Liz will be far more vulnerable to this — she has no mental model for push/pull and will not know when she's working on stale files or when her changes haven't been saved to the shared version.

**The solution: Claude handles all of it, invisibly.**

Please ensure START_HERE.md (or WORKING_WITH_LIZ.md) encodes the following protocol:

**Session start:**
- Pull silently before doing anything else
- If there are uncommitted changes from a prior session, surface them warmly: "It looks like there's some work from last time that hasn't been saved yet — let me take care of that before we dive in."
- If the pull reveals new changes (e.g., Nathan pushed something from the Mac mini), acknowledge it briefly: "I just grabbed the latest updates — we're all synced up."

**Session end:**
- Commit everything with a message derived from what Liz said she was working on at the start
- Push immediately after committing
- Confirm to her simply: "Everything's saved and backed up."

**Liz never hears the words** commit, push, pull, branch, or staged. She hears "saved," "backed up," "synced," and "up to date."

**If anything goes wrong** (merge conflict, auth failure, anything unexpected): "This looks like a Nathan question — he'll have it sorted quickly." Do not attempt to walk her through resolution.

---

## Workspace File Note

The `candidette.code-workspace` file we created today points to the repo root. After the restructure, it should still point to root — the umbrella is the right scope. No change needed there. However, once the restructure is done, the `.vscode/settings.json` may need to account for the new subfolder layout if there are any path-specific settings. Worth a quick check post-restructure.

---

## Standing By

This agent will pull once you've pushed the restructured repo and do a full before/after review to confirm nothing was lost.

*Written by the candidette repo agent, 2026-03-02.*
