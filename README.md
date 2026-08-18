# 🐧 Linux 源码分析

> 🐧 28章 实战体系

一套完整的 **Linux 源码分析** 全中文实战课程体系，共 **28 章**。本课程以 HTML 可视化的形式呈现，从基础原理到工程实践循序渐进，适合系统性学习与复习。

## 🚀 快速开始

无需安装任何依赖，直接用浏览器打开 `index.html` 即可在线阅读全部章节：

```bash
open index.html   # macOS
# 或在浏览器中直接打开 index.html
```

## 📖 章节目录

| # | 章节 | 核心主题 |
|---|------|----------|
| 01 | Linux的诞生 | UNIX/MINIX/GNU背景、从0.00到1.0版本演进、关键人物与趣闻、为什么从0.11学起 |
| 02 | 内核架构总览 | 14个源码目录解读、宏内核vs微内核、编译产物vmlinux、RTFSC读源码方法论 |
| 03 | 开发环境搭建 | Bochs模拟器安装配置、内核镜像与磁盘准备、bochsrc逐行解读、QEMU+GDB备选方案 |
| 04 | 引导启动(上) | CPU加电与BIOS流程、bootsect.S源码精读、实模式编程要点、INT 0x13踩坑故事 |
| 05 | 引导启动(下) | setup.S获取硬件信息、进入保护模式CR0.PE、head.S分页初始化、A20门历史包袱 |
| 06 | 内核初始化 | main.c初始化全景图、各子系统初始化顺序、move_to_user_mode、init()第一个进程 |
| 07 | x86保护模式精要 | 段描述符与GDT/LDT、Ring0-3特权级保护、两级页表地址翻译、TSS硬件任务切换 |
| 08 | 中断与异常 | x86中断向量表、IDT与门描述符、8259A中断控制器、asm.s通用中断入口 |
| 09 | 系统调用 | int 0x80全流程追踪、system_call.s源码、sys_call_table调用表、参数传递与安全拷贝 |
| 10 | 进程调度 | task_struct数据结构、schedule()调度算法、switch_to()任务切换、jiffies时钟滴答 |
| 11 | 进程生命周期 | fork()写时复制机制、execve()加载程序、exit()与wait()回收、僵尸进程踩坑故事 |
| 12 | 信号机制 | 信号数据结构与位图、发送/递送/处理流程、sigframe用户栈帧、sigaction可移植性 |
| 13 | 内存管理(上) | 物理内存布局分区、mem_map页框管理、get_free_page分配、线性地址空间布局 |
| 14 | 内存管理(下) | 两级页表结构详解、线性地址翻译示例、do_wp_page写时复制、页表不一致幽灵Bug |
| 15 | 缓冲区管理 | buffer_head数据结构、LRU缓冲区淘汰策略、getblk/brelse源码、bread/bwrite块读写 |
| 16 | MINIX文件系统(上) | 磁盘六区布局、超级块super_block、inode结构与寻址、位图分配/释放算法 |
| 17 | MINIX文件系统(下) | namei()路径解析、file_table与fd映射、文件读写完整链路、open/close引用计数 |
| 18 | 管道与exec | 管道环形缓冲区实现、read_pipe/write_pipe、a.out可执行格式、shell管道链时序 |
| 19 | 块设备驱动(上) | 块设备抽象层设计、request请求队列、电梯调度算法、ll_rw_block读写入口 |
| 20 | 块设备驱动(下) | IDE控制器寄存器编程、CHS寻址与LBA、硬盘中断处理流程、RAM虚拟盘rd.c |
| 21 | 字符设备驱动(上) | tty三队列模型、tty_struct数据结构、控制台VGA显存操作、行规程line discipline |
| 22 | 字符设备驱动(下) | 键盘扫描码→ASCII、8042控制器编程、16550 UART寄存器、串口中断处理 |
| 23 | 内核调试技术 | printk日志级别策略、Bochs内置调试器、Magic SysRq键、常见内核Bug分类 |
| 24 | GDB单步跟踪 | QEMU+GDB远程调试、战略断点设置、跟踪系统调用全程、内存检查技巧 |
| 25 | 动手写系统调用 | 编写sys_hello函数、注册系统调用号、重新编译内核、用户态测试验证 |
| 26 | 从0.11到1.0 | 0.12虚拟内存与交换、0.95 VFS框架、0.98 TCP/IP网络栈、0.99 4GB线性空间 |
| 27 | 现代内核对比 | Buddy/Slab/SLUB演进、CFS→EEVDF调度器、LKM内核模块、eBPF/XDP可编程 |
| 28 | 综合项目 | 实现ramdisk驱动、简单procfs(备选)、完整开发流程、RTFSC开始旅程 |

## 📂 项目结构

```text
linux-kernel-source-tutorial/
├── index.html      # 课程主入口（在线阅读全部章节）
├── 01.html ~ 28.html   # 各章节正文
├── courses.json    # 课程元数据（标题/章节/主题）
└── theme.css       # 统一主题样式
```

## ✨ 课程特色

- **全中文实战体系**：面向中文读者，由浅入深，覆盖原理与工程实践
- **28 章完整内容**：系统化章节编排，形成完整知识闭环
- **可视化呈现**：HTML 图文并茂，适合快速浏览与重点回顾
- **即开即用**：无需构建、无需服务器，纯静态页面随开随看

---
*本课程由 `linux-kernel-source-tutorial/` 项目维护。*