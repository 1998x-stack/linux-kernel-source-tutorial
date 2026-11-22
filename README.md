# Linux 0.11 源码精读 · Visual Kernel Field Guide

[课程首页（GitHub Pages）](https://1998x-stack.github.io/linux-kernel-source-tutorial/) · [原始 Linux v0.11 源码](https://kernel.googlesource.com/pub/scm/linux/kernel/git/nico/archive/+/refs/tags/v0.11/) · [历史版本归档](https://www.kernel.org/pub/linux/kernel/Historic/old-versions/impure/)

从 BIOS 引导扇区到内核初始化、从系统调用到文件系统的 **28 章中文源码阅读路线**。先追踪具体程序的输入、机器状态、代码操作与输出，再比较系统抽象。教程定位为 **Linux 0.11 的历史实现**，不是现代 Linux 的源码参考手册。

## 目前内容

- **01–10：已深度重构**。01–05 介绍历史、源码结构、实验与启动；06–10 继续剖析内核初始化、x86 段表和硬件任务切换、IDT/IRQ、72 项系统调用与 counter 调度。前十章均包含独立 SVG、源码锚点与自检。
- **11–28：原内容迁移保留**。路径已统一，内容尚未按新设计全面审计；其中一些历史实现与现代术语仍需复核，不能视作已完成的技术验收。
- 首页提供课程路径、完整目录、搜索与筛选；无须外部 JS 库。

## 目录结构

```text
.
├── index.html                   # GitHub Pages 根目录首页
├── 01.html ... 28.html          # 旧深链兼容跳转
├── courses.json                 # 章节列表与链接的元数据
├── chapters/
│   ├── 01.html ... 10.html      # 已重构文章
│   ├── 11.html ... 28.html      # 原章节（待二次审校）
│   ├── index.html               # 兼容旧章节对首页的相对路径
│   └── theme.css                # 原章节样式（已修复错误注释）
├── assets/
│   ├── css/site.css             # 首页 + 新文章共同的设计系统
│   ├── js/site.js               # 可选交互：检索/筛选
│   └── svg/                     # 原创、可独立打开的 SVG
├── docs/research-sources.md     # 前十章的源码证据表
├── scripts/check_site.py        # 无第三方依赖的静态检查
├── scripts/browser_smoke.py     # 可选 Playwright 浏览器检查
├── .github/workflows/validate.yml
└── AGENTS.md                    # 后续维护与写作规范
```

## 本地阅读

直接打开根目录 `index.html` 即可阅读；为了让相对资源路径、跳转和后续测试与 Pages 环境一致，建议在仓库根目录启动本地服务：

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000/
python3 scripts/check_site.py
```

浏览器验收（须先安装 Playwright 与 Chromium）：

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/browser_smoke.py http://127.0.0.1:8000
```

## 发布策略

网站保持 **root `index.html` 入口**，兼容现有可能使用主分支根目录的 GitHub Pages 配置。不假设修改仓库文件会自动更改 Pages 发布源。后续如改为 Actions 发布，须先检查 Settings → Pages 的实际来源及部署工作流。

## 技术说明

0.11 原版的 `boot/bootsect.s`、`boot/setup.s`、`boot/head.s` 与 `Image` 构建目标均已在新文章中按源码核查。可编译环境与可启动镜像要分开验证；仓库不附带历史根文件系统磁盘镜像，不承诺现代工具链一键重建。

贡献前请阅读 [AGENTS.md](AGENTS.md)，每章要满足独立可读、版本界限、因果图、原始证据和验收五项要求。视觉叙事的方法参考 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts)，图解与正文均为此仓库专门编写。
