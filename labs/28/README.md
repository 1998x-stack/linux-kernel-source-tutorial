# Chapter 28 lab bundle

This directory contains two intentionally separate tracks.

## Track A — Linux 0.11 RAM Disk

- `ramdisk_range_check.diff`: a historical-source patch for overflow-safe sector range checks in `kernel/blk_drv/ramdisk.c`, plus a NULL-`bh` guard in the common request error log.
- `ramdisk_selftest.c`: a guest-side read/write round-trip test for block device `/dev/ram1` (major 1, minor 1).
- Enable the historical RAM Disk build option in the v0.11 top-level Makefile: `RAMDISK = -DRAMDISK=512`. The call site reserves `RAMDISK * 1024` bytes before `mem_init()`.
- Create the device node in the guest root filesystem: `mknod /dev/ram1 b 1 1`.
- Build the test with a toolchain that emits the a.out ZMAGIC format accepted by the v0.11 `fs/exec.c`. A modern default ELF binary is not a valid substitute.
- Apply the patch to a disposable v0.11 source copy, rebuild the kernel with the matching historical toolchain, and test in an emulator. The repository CI does not claim to perform this historical build or boot.

The host-side reference arithmetic test lives in `tests/test_ramdisk_bounds.py` and runs with Python's standard library:

```sh
python3 -m unittest discover -s tests -v
```

## Track B — modern procfs module (optional)

- `kernel_lab_proc.c` creates a read-only `/proc/kernel_lab` using modern `proc_ops` and `seq_file`.
- `Kbuild` and `Makefile` build it against the currently running kernel's configured build tree:

```sh
make -C /lib/modules/$(uname -r)/build M=$PWD/labs/28 modules
sudo insmod labs/28/kernel_lab_proc.ko
cat /proc/kernel_lab
sudo rmmod kernel_lab_proc
```

This second track is deliberately modern and is not source-compatible with Linux 0.11. Test only in a disposable VM; kernel modules execute with kernel privilege.
