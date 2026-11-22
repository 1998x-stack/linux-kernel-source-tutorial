# 0.11 源码研究与证据账本（首轮 01–05）

本表对应 **Linux 0.11**，不将 0.12、现代 Linux 或改造后的教学 fork 混进历史断言。原始代码使用古老汇编语法，摘录前必须核对版本和文件名。

| 文章 | 待验证命题 | v0.11 直接证据 | 处理结果 / 限界 |
|---|---|---|---|
| 01 | 引导由 bootsect → setup → head → main 接力 | [bootsect.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/bootsect.s), [setup.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/setup.s), [head.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/head.s) | 明确是 16 位 BIOS / i386 历史路径 |
| 02 | 顶层 `Makefile` 产出 `Image`，依赖 bootsect/setup/tools/system | [Makefile](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/Makefile) | 纠正用现代 `vmlinux` 概念代替此版本最终产物的问题 |
| 02 | 系统调用分派与文件读写代码所在位置 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s), [fs/read_write.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/read_write.c) | 强调不同 fd 类型产生不同实际调用路径 |
| 03 | 官方历史归档提供 0.11 tarball | [kernel.org 归档目录](https://www.kernel.org/pub/linux/kernel/Historic/old-versions/impure/) | 只读源码实验可复核；未宣称当下工具链直接成功编译 |
| 03 | 原版依赖 `as86`/`ld86` 等旧工具 | [Makefile](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/Makefile) | 仿真启动依赖匹配的镜像与根设备；不伪造构建/运行结果 |
| 04 | `BOOTSEG=0x07c0`、`INITSEG=0x9000`、`SETUPSEG=0x9020`、`SYSSEG=0x1000` | [bootsect.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/bootsect.s) | 段基址 ×16，分别得 0x7C00、0x90000、0x90200、0x10000 |
| 04 | 复制 256 words = 512B；setup 为 4 扇区；system 由 `read_it` 分批装入 | [bootsect.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/bootsect.s) | 将复制、磁盘读取和远跳转分段展示 |
| 05 | 使用 `INT 0x15, AH=0x88` 把扩展内存写至 `0x90002` | [setup.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/setup.s), [init/main.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/init/main.c) | 显式修正旧文章的 `AX=0xE801` |
| 05 | `setup.s` 搬移 system、装载 GDT、打开 A20、PIC 重映射、`lmsw` 开 PE | [setup.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/setup.s) | 与 `head.s` 后面的分页严格区分 |
| 05 | 四张页表恒等映射初始 16 MiB，并设置 CR3/CR0.PG | [head.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/head.s) | 4 × 1024 × 4096 B = 16 MiB；不等同于现代页表 |
| 05 | 通过压栈入口 + `ret` 进入 `main` | [head.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/head.s) | 禁止写成“setup.s 直接调用 main” |

## 原始仓库审计发现

- 28 篇文件平铺仓库根目录；已迁至 `chapters/` 并保留根路径重定向。
- 原 `theme.css` 使用 HTML 注释作为首行，不是合法 CSS 注释；迁移版已修复。
- 原 02 章“14 个源码目录”的断言没有严格标出层级，且旧稿可能混用现代 `vmlinux` 术语。
- 原 05 章 `AX=0xE801` 与原始 0.11 源码不符；已以 `AH=0x88` 重写。
- 原 04 章含复位向量物理地址不严谨的直接算术推导；新文与 BIOS 装载 0x7C00 的事件严格分开。
- 06–28 目前为迁移保存，不属于这轮事实审计已通过范围。

## 未来核验任务

逐篇验证 06–28 中实际代码、API、数据结构和边界条件；尤其注意 `mem_init`、系统调用、8259、fork、MINIX 文件系统、TTY、驱动接口和现代内核对比。每次重写要先扩充此账本，再生成插图。
