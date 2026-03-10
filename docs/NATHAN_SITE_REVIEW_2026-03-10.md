# Nathan's Site Review — 2026-03-10

Feedback from Nathan reviewing the live Hugo/PaperMod site with Liz present. Organized by priority.

---

## Bugs / Broken Things (Fix First)

### 1. Top nav links are broken
The navigation links across the top of the site don't work. They may work on the deployed site but not when served locally over the network — either way, verify all nav links resolve correctly on the live Netlify deploy. Every link in the top nav needs to go somewhere.

### 2. "About" page is a 404
Typing `/about` or `/liz` returns a 404. The About link needs to point to a real page. Nathan's suggestion: the About link should go to the Liz bio page.

### 3. Hover hashtag on headings
When hovering over section headings (like "How I Work," "Our Services," "Hey There, Candidate"), a `#` symbol appears that looks like a broken link. This is a PaperMod anchor-link feature. It needs to be removed or hidden — it looks broken to visitors.

### 4. "How I Work" page URL says "services"
Navigating to "How I Work" from the menu works, but the URL shows `/services/` or similar. The URL and the page title should match. Check that the slug and menu label are consistent.

---

## Styling / Visual Cleanup

### 5. Scrollbar color
The browser scrollbar has a non-standard color (looks like it's inherited from PaperMod's theme accent). Change it to either fuchsia (to match the brand) or just leave it neutral/default.

### 6. "Go to top" button (bottom-right)
The floating "go to top" button in the bottom-right corner also has the old PaperMod default styling. Update it to match the site's brand colors, or remove it if it's not needed.

### 7. Footer: remove "Powered by Hugo and PaperMod"
Replace the default footer with just "Candidette Campaigns" (or similar). Use the footer space for something useful — contact info, a CTA, social links — not template credits.

### 8. Fuchsia accent stripes are misaligned
The small pink/fuchsia horizontal lines to the left of section headings (likely on H2 tags) are not vertically centered with their heading text. Fix the alignment so the stripe sits centered relative to the heading. Applies to:
- "How I Work" heading
- "Hey There, Candidate" heading
- Other section headings using this pattern

### 9. Responsive text on very small screens
The hero tagline "Run for office as yourself" — the word "yourself" may get clipped or break awkwardly on very small screens. Test at the narrowest phone widths (320px) and scale the font down if it breaks. If it doesn't actually break at real device sizes, this is fine to ignore.

---

## Content / UX Improvements

### 10. "How I Work" page needs a hero image
The How I Work / Services page feels bare at the top. Add a hero image to give it visual weight.

### 11. Service pills look clickable but aren't
The service category labels (Event Planning, Field Operations, Social Media, etc.) have hover states that make them look interactive, but clicking does nothing. This feels broken. Two options:
- **Quick fix**: Remove the hover effect so they look like static labels.
- **Better fix (Nathan's suggestion)**: Make each pill clickable so it reveals a paragraph of detail below it, one at a time (accordion-style). Similar to how Beat Kitchen's pill-nav or search menu works — click to show, click another to swap.

### 12. More content needed (not urgent)
Several pages need more text eventually. The site isn't embarrassing — it's clean and neat — but it needs fleshing out over time. Not a blocker for launch, but a near-term priority.

### 13. Contact form — verify Netlify handles it
The "Let's Talk" page has a contact form. Confirm that Netlify form handling is set up and working (Netlify Forms or an alternative).

---

## Summary for Liz

The site looks good — clean, not embarrassing, and a visual upgrade from the old Squarespace site. The main work is:
1. **Fix the nav links and 404s** (this is the most important — visitors can't navigate)
2. **Clean up PaperMod leftovers** (scrollbar, footer, go-to-top button, heading hashtags)
3. **Align the fuchsia accent stripes** on headings
4. **Make the service pills either static or interactive** (not fake-clickable)
5. **Add more content over time** (hero images, longer service descriptions, etc.)
