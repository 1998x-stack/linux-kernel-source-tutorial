# 0.11 源码研究与证据账本（第 01–28 章）

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
- 21–28 已在第五批（见下文“第五批 21–26”及 27/28 表）重写为源码锚定稿，命题逐一对应 v0.11 文件。

## 尚需继续的核验

21–28 已完成本轮重写与源码锚定，但事实复审仍须逐章针对具体寄存器、字段与返回分支继续交叉核对（`mem_init`、系统调用、8259、fork、MINIX 文件系统、TTY、驱动接口与现代内核对比）。每次实质改动都应先扩充本账本，再生成插图。

## 第二批 06–10 的逐篇事实审计

| 文章 | 源码锚点 | 核对结论与已修正误区 |
|---|---|---|
| 06 | [init/main.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/init/main.c) | `main()` 在 `sti(); move_to_user_mode()` 后第一次 `fork()`；父任务 0 调用 `pause()`，子任务 1 执行 `init()`，而不是 `init()` 负责第一次 fork |
| 06 | [mm/memory.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/memory.c) | `mem_map` 按 `USED=100` 初始化后将指定可分配页归零，不是位图与 255 初始化 |
| 06 | [kernel/sched.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/sched.c) | `sched_init()` 配置任务 0 TSS/LDT、PIT 与两个门；`time_init` 是 CMOS 时间初始化 |
| 07 | [kernel/fork.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/fork.c), [include/linux/sched.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/sched.h) | 每个进程有 LDT，`copy_mem` 设 `nr*0x4000000` 用户段基址；用户段不等于恒定零基址 |
| 07 | [include/asm/system.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/asm/system.h) | `0x0f` / `0x17` 中 TI=1，引用 LDT；`set_system_gate` 是 type 15 / DPL 3 |
| 07 / 10 | [include/linux/sched.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/sched.h) | `switch_to` 是内联宏，包含 `ljmp` 到 TSS；不是 `system_call.s` 中的普通汇编函数 |
| 08 | [boot/head.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/head.s), [kernel/asm.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/asm.s) | `head.s` 安装 256 个默认 IDT 门，`asm.s` 主要处理异常和错误码，不能写成每次 IRQ 的通用处理入口 |
| 08 | [boot/setup.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/setup.s) | 8259 IRQ 重映射在 setup.s，向量 0x20–0x2F，非 `init/main.c:init_8259A` |
| 08 / 10 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s) | timer_interrupt 在本文件，入口递增 `_jiffies`、向 PIC 发 EOI、调用 `_do_timer`，而非 `asm.s → _do_IRQ` |
| 09 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s), [include/linux/sys.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/sys.h) | 实际是 `nr_system_calls=72`，编号 0..71；写成 `NR_syscalls=82` 属不同版本混用；逐项解释入栈和返回栈帧 |
| 10 | [kernel/sched.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/sched.c) | `schedule()` 先处理可唤醒信号，再选择最大 counter，零耗尽时重算；`do_timer` 在 CPL0 时不会因 tick 直接 schedule |

**视觉证据**：`assets/svg/06-*.svg` 至 `assets/svg/10-*.svg` 共 10 张可独立解析的示意图，每个框与连接由以上源码中的调用或状态变化支持，图中教学数字与真实运行测量严格区分。

**第二批质量门禁**：重构稿包含明确版本范围、图标题/说明、叙事、直接原始源码链接、校验命令、可展开自测和前后章导航。CI 验证静态结构、SVG XML 与 1440/390/360 像素宽度下的基本交互；单独的源代码事实复审仍需针对每个细节持续开展。

## 第三批 11–15 真实源码依据与纠错

| 章节 | v0.11 文件 | 可以逐项复核的结论 |
|---|---|---|
| 11 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s) | _sys_fork 专用入口调用 find_empty_process / copy_process；原稿把其错误写为完整 C 版 sys_fork |
| 11 | [kernel/fork.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/fork.c) | copy_mem 调 copy_page_tables(from,to,size)，共享写保护页；任务页仅复制 task_struct，不直接复制旧内核栈 |
| 11 | [fs/exec.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/exec.c) | a.out ZMAGIC、#! 和 executable inode 按需装入；execve 保留 PID，不是 fork |
| 11 | [kernel/exit.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/exit.c) | do_exit 先 TASK_ZOMBIE + SIGCHLD；waitpid 取状态后调用 release 回收，支持 WNOHANG |
| 12 | [kernel/signal.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/signal.c) | sys_signal 使用 SA_ONESHOT\|SA_NOMASK，do_signal 准备 7 或 8 个 long 的用户栈帧并写 restorer |
| 12 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s) | 返回用户态的系统调用/时钟路径识别 signal & ~blocked，不是任意硬件中断即时执行 handler |
| 13 | [mm/memory.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/memory.c) | LOW_MEM=0x100000、PAGING_PAGES=3840、USED=100；get_free_page 反向扫描并清零 4KiB，非 256KiB 起始 |
| 13 | [init/main.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/init/main.c) | buffer_memory_end/main_memory_start 依 RAM 容量分段选择；不是 1–16MiB 全部直接可分配 |
| 14 | [mm/memory.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/memory.c) | un_wp_page 单引用恢复可写，多引用复制，TLB 失效；do_no_page 尝试 share_page 或 bread_page 4×1KiB |
| 14 | [mm/page.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/page.s) | 页故障低级入口读取 CR2 和 CPU 错误码 bit0；按 present 分支选择 do_no_page/do_wp_page |
| 15 | [include/linux/fs.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/fs.h) | BLOCK_SIZE=1024、NR_HASH=307，buffer_head 不存在旧文所写的 b_req 字段 |
| 15 | [fs/buffer.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/buffer.c) | hash/free_list 双链、BADNESS(dirt,lock) 选择候选，非严格 LRU；brelse 仅减 b_count，sys_sync/sync_dev 负责写回 |

本轮新增 `assets/svg/11-*.svg` 至 `15-*.svg` 共 10 张原创 SVG。各图只展示对应版本支持的因果路径；图中示例计数/页地址为教学演算而非模拟器测量。该批 CI 覆盖当时已重构章节的 HTML/链接/SVG XML 与三宽度浏览器验收；21–28 已在后续第五批完成重写与源码锚定。

## 第四批 16–20：MINIX、路径、管道和块 I/O 的源码事实审计

| 章节 | v0.11 真实源码 | 已修正的技术事实 |
|---|---|---|
| 16 | [include/linux/fs.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/fs.h) | SUPER_MAGIC=0x137F、BLOCK_SIZE=1024、d_inode=32B、i_zone[9]、d_super_block 的 s_log_zone_size 指“区大小位移”而非日志 |
| 16 | [fs/super.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/super.c) | read_super 从块 1 读取超级块，随后缓存 inode 与 zone 两类 bitmap；mount_root 还要关联根 inode |
| 16 | [fs/bitmap.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/bitmap.c) | new_inode、free_inode、new_block、free_block 实际定义于 bitmap.c；位图位序与 s_firstdatazone−1 存在偏移 |
| 16 | [fs/inode.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/inode.c) | _bmap 采用 7 个直接、512 个一级、512² 个二级间接区号；read_inode 用 (num−1)/32 算磁盘块 |
| 17 | [fs/namei.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/namei.c) | get_dir/dir_namei/namei/open_namei 分工；find_entry 为挂载点与 .. 特殊处理；NAME_LEN=14 |
| 17 | [include/linux/fs.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/fs.h) | dir_entry 为 16B、NR_OPEN=20、NR_FILE=64；f_pos 位于 struct file，非 inode 全局位置 |
| 17 | [fs/file_dev.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/file_dev.c) | file_read 通过 bmap 和 bread 从 1KiB 缓冲块读取，非 fs/minix/file.c 或现代 VFS |
| 18 | [fs/pipe.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/pipe.c) | sys_pipe 在 fs/pipe.c，两个 file 引用一个匿名 m_inode；read_pipe/write_pipe 使用 4KiB 环形页，容量 4095B、无读者触发 SIGPIPE |
| 18 | [fs/exec.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/fs/exec.c) | do_execve 使用 a.out ZMAGIC 与 #!；demand-loading 指令页在缺页时读 executable inode，而非一次将全部程序复制进内存 |
| 19 | [kernel/blk_drv/blk.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/blk_drv/blk.h) | NR_REQUEST=32、IN_ORDER 比较 cmd/dev/sector；静态链表不是自动请求合并 |
| 19 | [kernel/blk_drv/ll_rw_blk.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/blk_drv/ll_rw_blk.c) | WRITE 只可使用 request[0..20]；READ 可扫描 [0..31]；每个 1KiB buffer_block 对应 2×512B 扇区 |
| 20 | [kernel/blk_drv/hd.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/blk_drv/hd.c) | 使用分区 start_sect 后计算 CHS，read_intr 每 IRQ 取 256 words，并更新 sector/buffer/nr_sectors |
| 20 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s) | hd_interrupt 是汇编 IRQ14 入口，使用 do_hd 指针分派 read_intr/write_intr，不是普通 C 版 do_IRQ |
| 20 | [kernel/blk_drv/ramdisk.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/blk_drv/ramdisk.c) | rd_init 预留一段内存，do_rd_request 使用 memcpy 和 (sector<<9) 定位；没有运行时 malloc(2MiB) |

本批新增十张 `assets/svg/16-*.svg` 至 `assets/svg/20-*.svg` 原创源码流程图；图中路径、字段和返回分支均可对照上述原版源码，标注的数值例子为教学演算而非运行实验。该批 CI 目标覆盖当时已重构章节的静态结构和 1440/390/360px 浏览器基本交互验收；21–28 随后在第五批重写，故本批不声称已完成其源码审计。

## 第五批 21–26：tty、驱动、调试、构建与演进边界

本批在保留仓库结构的前提下把 21–26 从旧稿重写为源码锚定稿。以下命题均对应 v0.11 文件，图中数值与版本归属不确定处已在正文显式标注。

| 章节 | v0.11 真实源码 | 已修正的技术事实 |
|---|---|---|
| 21 | [include/linux/tty.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/tty.h) | `TTY_BUF_SIZE=1024`，`tty_queue` 为 `char buf[1024]`+head/tail+proc_list；旧稿的 `unsigned long data[128]` 与 16 位解释均错误 |
| 21 | [kernel/chr_drv/tty_io.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/chr_drv/tty_io.c) | `tty_table[]` 只有 console/rs1(0x3f8)/rs2(0x2f8)；`copy_to_cooked` 按 ICANON/ISIG/ECHO 分支；`tty_read` 用 `secondary.data` 判断整行 |
| 21 | [kernel/chr_drv/console.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/chr_drv/console.c) | 彩色显存 `video_mem_start=0xb8000`、端口 0x3d4/0x3d5、`video_erase_char=0x0720`；光标 14/15 号寄存器；`con_write` 为有限转义子集 |
| 22 | [kernel/chr_drv/keyboard.S](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/chr_drv/keyboard.S) | 入口读端口 0x60，用 `key_table(,%eax,4)` 分派，无 `testb $0x80` 分支；`do_self` 依 mode 选 alt/shift/key_map；`put_queue` 写控制台 read_q |
| 22 | [kernel/chr_drv/serial.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/chr_drv/serial.c), [rs_io.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/chr_drv/rs_io.s) | IER/LCR/MCR 分频 0x30→2400bps；`rs_int` 循环读 IIR 经 `jmp_table` 分派 read_char/write_char，`startup=256` |
| 23 | [kernel/printk.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/printk.c) | printk 仅 `vsprintf` 到静态 `buf[1024]` 后 `_tty_write(0,...)`；无日志级别、无环形缓冲；更正旧稿的 Magic SysRq 与级别策略 |
| 23 | [kernel/traps.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/traps.c), [mm/page.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/page.s) | `die()` 打印陷阱号与寄存器，`trap_init()` 用 `set_trap_gate` 挂 0–16 号；页故障入口读 CR2 再调 do_no_page/do_wp_page |
| 24 | [kernel/system_call.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/system_call.s) | `_system_call` 越界检查、换段、`_sys_call_table(,%eax,4)` 分派；`_ret_from_sys_call` 才处理 signals 并 `iret` |
| 25 | [include/linux/sys.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/sys.h), [include/unistd.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/unistd.h) | 最高调用号为 `__NR_setregid 71`，`nr_system_calls=72`；新调用应占 72，`nr_system_calls` 改 73；`_syscall0` 生成含 `int $0x80` 的存根 |
| 25 | [Makefile](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/Makefile) | `all: Image`；`tools/system` 生成 `System.map`；本章的构建步骤明确标注为未执行 |
| 26 | [mm/memory.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/memory.c), [boot/head.s](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/boot/head.s), [include/linux/fs.h](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/include/linux/fs.h) | 0.11 无换出、只有 MINIX 文件系统、无网络；内核恒等映射前 16MiB，用户段基址 nr×0x4000000（每进程 64MiB） |
| 26 | 后续版本 | 仅描述方向（交换、文件系统抽象层、协议栈），不声明具体版本归属；以 kernel.org 历史目录为准 |

| 27 | [mm/memory.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/mm/memory.c), [kernel/sched.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/sched.c) | 0.11 为 mem_map 字节计数与 counter 轮转；现代伙伴/slab、CFS/EEVDF、LKM/eBPF 均标注为“仅对照”，不回填历史 |
| 28 | [kernel/blk_drv/ramdisk.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/kernel/blk_drv/ramdisk.c), [Makefile](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/Makefile) | ramdisk 自 0.11 即存在；do_rd_request 用 `rd_start+(sector<<9)` 与 memcpy；procfs 不在 0.11；构建/启动步骤均标注未执行 |

**视觉证据**：`assets/svg/21-*.svg` 至 `assets/svg/28-*.svg` 共 16 张原创 SVG，均可独立解析（viewBox + title/desc）；图中数值为教学演算，非模拟器测量；现代内核侧内容均在正文与图中显式标为“对照”，未与 0.11 混用。

**质量门禁边界**：`scripts/check_site.py` 与 `scripts/browser_smoke.py` 已改为按 `data-state="reworked"` / `assets/css/site.css` 动态识别已重构章节，因此不再硬编码“前 20 章”。事实复审仍应逐章针对具体寄存器/字段继续开展；21–28 已完成本轮重写与源码锚定，但后续仍应对细节做交叉复核。
