# 0.11 源码研究与证据账本（第一、二批 01–10）

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
- 11–28 目前为迁移保存，不属于这轮事实审计已通过范围。

## 未来核验任务

逐篇验证 11–28 中实际代码、API、数据结构和边界条件；尤其注意 `mem_init`、系统调用、8259、fork、MINIX 文件系统、TTY、驱动接口和现代内核对比。每次重写要先扩充此账本，再生成插图。

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
