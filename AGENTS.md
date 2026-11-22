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
- `chapters/theme.css`: retained only for historical compatibility; rewritten chapters 01–28 use `assets/css/site.css`.
- `assets/svg/*.svg`: standalone, original, accurate diagrams; `docs/research-sources.md`: evidence ledger.
- Preserve all 28 lessons and legacy redirects. All 28 pages now follow the shared article system; source-audit and runtime-test claims must still be supported by the evidence ledger and actual logs.

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


## Linux 0.11 历史版本约束（第 21–25 章）

- TTY 只按 v0.11 的 `tty_table[0..2]`、三个 `tty_queue` 和 `copy_to_cooked()` 解释；源码明确指出 pseudo-TTY 尚未实现，不得写入现代 PTY / 可插拔 `tty_ldisc` 结构。
- 串口默认 2400 baud、8N1；`serial.c` 未启用 16550A FIFO。区分 IIR 读偏移与 FCR 写偏移，保留 IRQ3/IRQ4 和向量 0x23/0x24 的实际映射。
- `printk` 只有静态 1024B 格式化缓冲区并调用 `tty_write(0,...)`；不要虚构现代 log ring buffer、syslog 读取路径或 Magic SysRq。
- 0.11 的 `Image` 是 `tools/build` 拼接的 bootsect/setup/system 原始启动镜像；QEMU 以磁盘/软盘启动，不能假设它是现代 bzImage 并使用 `-kernel`。默认链接 `-s -x` 会剥离符号。
- 新系统调用要同步 `include/unistd.h` 编号、`include/linux/sys.h` 函数表、C 实现和 `system_call.s` 的 `nr_system_calls`。该版本用户程序由 `fs/exec.c` 按 ZMAGIC a.out 规则装载，不要用现代 ELF 示例替代。

## Historical version constraints (chapters 26–28)

- v0.12 mm/memory.c records demand-loading (1991-12-01), shared pages (12-02), and real disk paging (12-18). get_free_page() calls swap_out() on allocation failure; do not invent a swapd daemon or call the scan a second-chance/CLOCK algorithm.
- v0.12 page-table helpers explicitly use the global _pg_dir = 0. Do not attribute the later per-task CR3 layout to v0.12.
- v0.95a include/linux/fs.h has file_operations and inode_operations, but does not yet show the later file_system_type / super_operations registry model. v0.96c adds sys/vfs.h, superblock operations and fs/super.c:file_systems[]; the extfs release note still calls it alpha.
- v0.98-pl1 README says TCP/IP sources were present but not compiled into the normal binary. SCSI, extfs, dosfs and proc-fs had testing caveats; do not describe them as production-ready or default-enabled.
- v0.99-pl11 mm/memory.c uses each task's tss.cr3; clear_page_tables() handles entries 0–767 separately from shared high entries 768–1023. Explain 4GiB as the 32-bit linear-address range, not 4GiB of user RAM per process.
- v1.0 is dated 1994-03-14; its announcement describes the change from 0.99-pl15 as primarily bug fixes, not a sudden subsystem rewrite.
- In modern comparisons, distinguish buddy page allocation from SLUB object caches. Upstream v2.6.22 init/Kconfig defaults to SLAB; v2.6.23 defaults to SLUB. CFS was introduced in 2.6.23; Linux 6.6 began the fair-class transition to EEVDF. EEVDF is not the real-time deadline scheduling class.
- Bounded eBPF loops are supported since Linux 5.3 (upstream commit 2589726d12a1); they must still be proven bounded and pass verifier complexity/safety checks. XDP native, generic/SKB and hardware-offload modes have different driver/device constraints.
- Linux v0.11 already contains kernel/blk_drv/ramdisk.c; kernel/blk_drv/Makefile includes ramdisk.o. Top-level RAMDISK is measured in 1KiB blocks and init/main.c reserves the region by calling rd_init(main_memory_start, RAMDISK*1024) before mem_init(). There is no kmalloc/GFP_KERNEL path in this driver.
- The v0.11 RAM Disk uses major 1, minor 1; request sector and nr_sectors are in 512-byte sectors and are converted with << 9. rd_load() is called from hd.c:sys_setup() before mount_root(), and a successful floppy image load sets ROOT_DEV=0x0101.
- Any subtraction-based range check in chapter 28 is a proposed hardening exercise, not original upstream source. The read/write command sequence is a lab recipe; never claim it passed without an actual v0.11 toolchain + emulator run.
