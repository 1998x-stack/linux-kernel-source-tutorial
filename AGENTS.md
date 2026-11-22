# AGENTS.md — Linux 0.11 source tutorial

## Mission and scope
Maintain a self-contained, Chinese-language Linux 0.11 source-reading course. Every page must be useful to a first-time visitor arriving directly from search, not just to a reader who has seen earlier chapters. The goal is a causal explanation from problem → machine state → source trace → verification → limitations, inspired by the *Olah-style-posts* explanatory design approach without copying its diagrams, copy or branding.

## Source authority and version discipline
- Historical code baseline: `https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/`.
- Historical tarball: `https://www.kernel.org/pub/linux/kernel/Historic/old-versions/impure/`. Check exact source filename, syntax and behavior against v0.11 before writing.
- Critical invariants: `boot/bootsect.s`, `boot/setup.s`, `boot/head.s`; BIOS `INT 15h AH=0x88` in this version; original `Makefile` produces `Image`; `head.s` sets `CR3` and `CR0.PG`.
- The old `as86` syntax differs from modern GNU assembly. Do not silently modernize quotations or present illustrative pseudocode as verbatim source.
- Explicitly distinguish historical 0.11, generic x86/BIOS facts, modern Linux and unverified engineering assumptions. Never transplant modern UEFI, 64-bit, syscall, VFS or scheduler details into 0.11 without an explicit contrast.
- Never invent benchmark data, screenshots, emulator results, command output, source line numbers, configuration, version history, or working build status.

## Content contract (each standalone chapter)
1. Open with the concrete problem and the version being studied; do not write “本讲义介绍了” or rely on prior chapter context.
2. Show the minimal state or data-flow graph that answers the problem. Every diagram needs a question, labels, source-backed topology, title/desc, alt and figcaption.
3. Explain actual program order, register/memory state, invariants and error branches before introducing abstractions.
4. Use short accurately quoted source excerpts (never long copied passages) with exact versioned links; annotate how input becomes output.
5. Include at least one reproducible read-only exercise or conditional experiment, a specified expected observation, and a clearly labeled limitation.
6. Close with the next conceptual dependency and canonical sources. Keep production notes and AI workflow commentary outside the article.

## Files and public URLs
- `index.html`: GitHub Pages homepage (root source). `courses.json`: canonical chapter metadata.
- `chapters/01.html`–`chapters/28.html`: canonical chapter pages. Root `01.html`–`28.html` are permanent redirect stubs for legacy URLs; never remove them without a link migration plan.
- `assets/css/site.css`: single design system for the homepage and rewritten lessons. `assets/js/site.js`: only progressively enhanced UI.
- `chapters/theme.css`: intentionally preserved for legacy 06–28 until individually redesigned.
- `assets/svg/*.svg`: standalone, original, accurate diagrams; `docs/research-sources.md`: evidence ledger.
- Preserve all 28 lessons and do not claim non-rewritten lessons passed a source audit.

## Visual system
Use warm paper, high-contrast ink, teal for control/data paths, terracotta for hardware/transform operations, violet for alternative state and amber for warnings. Color may supplement, never replace, text labels and visible path direction. Article measure around 820px, sticky TOC on desktop, fluid figures, readable mobile at 360/390px, print and reduced-motion CSS. Use semantic `main > article`, exactly one H1, ordered H2 sections, keyboard-operable `details` / controls, visible `:focus-visible`; no CDN, external fonts, SVG text smaller than legible nominal 13px, scripts inside diagrams, or HTML comments inside CSS.

## Evidence and testing gates
- Before edits, inspect source tag, module dependencies, current chapter HTML and `courses.json`.
- After edits, run `python scripts/check_site.py`. If browser tooling exists, run `python scripts/browser_smoke.py http://127.0.0.1:8000` with a local HTTP server on 8000.
- Browser acceptance must cover 1440 / 390 / 360 widths, no horizontal body overflow, links/images, JS console errors, focusable controls, active filtering, expandable self-check and each standalone SVG render.
- Claim actual tests passed **only** after reading real logs. CI configured or job created does not equal browser QA passed or Pages deployed.
- Review visual semantics and technically sensitive register/code excerpts one by one, not just page count.

## Publishing
Prefer a reviewed topic branch and PR; inspect changes and workflow statuses before merging. GitHub Pages root must continue to expose the root `index.html` unless repository Pages settings are separately changed and verified. Avoid breaking historical deep links and keep the repo navigable even with JavaScript disabled.
