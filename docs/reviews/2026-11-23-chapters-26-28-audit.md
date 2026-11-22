# Chapters 26–28 technical audit and repair

Date: 2026-11-23
Repository: 1998x-stack/linux-kernel-source-tutorial
Base: 4560f6c547b331896f26b7a65bf7e651f3a410a8

## Scope

Reviewed chapters 26–28 against versioned Linux source tags and current kernel documentation, then rebuilt all three articles in the shared article design system. Added 9 standalone SVGs and 3 per-chapter evidence ledgers.

## Findings fixed

### Chapter 26 — historical version drift

- Removed the unsupported swapd daemon claim. v0.12 get_free_page() calls swap_out() when page allocation fails.
- Removed the “second-chance” characterization. The v0.12 implementation scans page-table entries and treats dirty and clean pages differently; it is not a CLOCK/second-chance implementation.
- Corrected the filesystem history: v0.95a has file_operations and inode_operations; v0.96c has sys/vfs.h, super_operations, file_system_type, file_systems[] and get_fs_type().
- Replaced unsupported extfs capacity numbers and “ext2” conflation with the v0.96c release note's actual alpha status and supported scope.
- Corrected the v0.98 network story: TCP/IP source was present but not compiled into the normal binary; README also records testing caveats for SCSI, extfs, dosfs and proc-fs.
- Replaced the ambiguous “4GB per process” claim with the exact v0.99-pl11 TSS CR3 and page-directory evidence. The 32-bit linear range is 4GiB; code handles entries 0–767 separately from shared 768–1023 entries.
- Corrected the 1.0 milestone: dated 1994-03-14 and described in the release announcement as primarily bug fixes relative to 0.99-pl15.

### Chapter 27 — modern subsystem corrections

- Clarified that mem_map[] in 0.11 is a page-use counter array, not a bitmap.
- Explained buddy physical-page allocation and SLUB object caches as different layers. Verified the default change from SLAB in upstream v2.6.22 init/Kconfig to SLUB in v2.6.23.
- Reframed CFS as the historical vruntime/RB-tree design and EEVDF as the Linux 6.6 fair-class transition; EEVDF is not the real-time deadline scheduling class.
- Corrected eBPF loop restrictions: bounded loops have been supported since Linux 5.3, but must still pass verifier safety and complexity checks.
- Distinguished XDP native, generic/SKB and hardware-offload paths and their driver/device prerequisites.

### Chapter 28 — restore the actual 0.11 RAM Disk

- Removed the fictitious new-driver implementation using kmalloc/GFP_KERNEL and modern block APIs.
- Documented the existing kernel/blk_drv/ramdisk.c and ramdisk.o build entry.
- Corrected RAMDISK to 1KiB block units and traced rd_init(main_memory_start, RAMDISK*1024) before mem_init().
- Corrected device identity to major 1, minor 1; the original handler rejects other minors.
- Explained 512-byte request sectors versus 1KiB buffer blocks, the << 9 conversion and end_request().
- Traced rd_load() from hd.c:sys_setup() before mount_root(), including the conditional MINIX floppy image load and ROOT_DEV=0x0101.
- Reclassified the subtraction-based bounds check as a proposed hardening exercise, not upstream code.
- Rejected procfs as a small 0.11 project: the required filesystem type/superblock operation registration belongs to later VFS evolution.

## Visual and engineering changes

- Chapter 26: 3 SVGs (version map, v0.12 swap flow, v0.99 address-space map).
- Chapter 27: 3 SVGs (memory allocation layers, scheduler evolution, eBPF/XDP path).
- Chapter 28: 3 SVGs (boot-time reservation, request path, block/sector units).
- Added docs/evidence/chapter-26.json through chapter-28.json.
- Updated courses metadata, homepage statuses, README, AGENTS.md and the research-source ledger.
- Updated static and Playwright checks to include all 28 pages and all chapter SVGs.

## Acceptance boundary

The articles and source claims have been checked against versioned source/documentation. Static and browser workflows must still run on the PR head and their real logs must be inspected before merging. The chapter 28 RAM Disk recipe is a reproducible lab plan, not a claim that a 1991 toolchain/QEMU/rootfs combination was executed in this session. GitHub Pages deployment must be checked independently from source merge.
