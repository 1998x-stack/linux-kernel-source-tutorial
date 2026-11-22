#!/usr/bin/env python3
"""Static validation for all 28 standalone chapters, local links and SVG assets."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ISSUES = []
ALLOWED_EVIDENCE = {"verified", "derived", "illustrative", "unverified"}

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.links = []
        self.images = []
        self.sections = []
        self.ids = []
        self.details = 0
        self.cards = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "section":
            self.sections.append(a.get("id"))
        if tag == "details":
            self.details += 1
        if a.get("id"):
            self.ids.append(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])
        if tag == "img":
            self.images.append(a)
            if a.get("src"):
                self.links.append(a["src"])
        if tag == "article" and "course-card" in a.get("class", "").split():
            self.cards += 1

def bad(message):
    ISSUES.append(message)

def parse_html(path):
    parser = Inspector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser

def check_refs(path, parsed):
    for href in parsed.links:
        if not href or href.startswith(("https://", "http://", "mailto:", "data:")):
            continue
        if href.startswith(("javascript:", "//")):
            bad(f"{path}: unsafe URL {href}")
            continue
        raw, _, fragment = href.partition("#")
        raw = raw.split("?", 1)[0]
        target = path if not raw else (path.parent / raw).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.exists():
            bad(f"{path}: missing local resource {href}")
            continue
        if fragment and target.suffix == ".html":
            target_parser = parsed if target == path else parse_html(target)
            if fragment not in target_parser.ids:
                bad(f"{path}: missing anchor {href}")
    for img in parsed.images:
        if not img.get("alt", "").strip():
            bad(f"{path}: image missing alt text: {img.get('src')}")
    if len(parsed.ids) != len(set(parsed.ids)):
        bad(f"{path}: duplicated HTML IDs")

def main():
    courses = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
    if len(courses.get("chapters", [])) != 28:
        bad("courses.json: expected 28 chapters")

    for i in range(1, 29):
        num = f"{i:02d}"
        path = ROOT / "chapters" / f"{num}.html"
        if not path.exists():
            bad(f"missing {path}")
            continue
        data = path.read_text(encoding="utf-8")
        parsed = parse_html(path)
        if parsed.h1 != 1:
            bad(f"{path}: expected exactly one H1, got {parsed.h1}")
        if len(parsed.sections) < 5:
            bad(f"{path}: requires at least five self-contained sections")
        if not parsed.images:
            bad(f"{path}: visual explanation missing")
        if i >= 26 and "diagram-scroll" not in data:
            bad(f"{path}: mobile diagram must use an inner horizontal scroll region")
        if parsed.details < 1:
            bad(f"{path}: missing native interactive self-check")
        if "../assets/css/site.css" not in data:
            bad(f"{path}: shared article stylesheet missing")
        if "theme.css" in data:
            bad(f"{path}: legacy stylesheet still linked")
        if "Linux 0.11" not in data and "v0.11" not in data:
            bad(f"{path}: version scope missing")
        if "Olah-style" in data or "本讲义介绍" in data:
            bad(f"{path}: workflow boilerplate found")
        check_refs(path, parsed)

        redirect = ROOT / f"{num}.html"
        if not redirect.exists() or f"chapters/{num}.html" not in redirect.read_text(encoding="utf-8"):
            bad(f"{redirect}: legacy redirect missing")
        meta = courses["chapters"][i - 1]
        if meta.get("file") != f"chapters/{num}.html":
            bad(f"courses.json: chapter {num} has incorrect file")

    home_path = ROOT / "index.html"
    home_data = home_path.read_text(encoding="utf-8")
    home = parse_html(home_path)
    if home.h1 != 1:
        bad("index.html: expected exactly one H1")
    if home.cards != 28:
        bad(f"index.html: expected 28 course cards, got {home.cards}")
    if home_data.count('data-state="reworked"') != 28:
        bad("index.html: all 28 cards must be marked reworked")
    if 'data-state="legacy"' in home_data or "待审校" in home_data:
        bad("index.html: stale pending-review status remains")
    check_refs(home_path, home)

    for n in (26, 27, 28):
        evidence_path = ROOT / "docs" / "evidence" / f"chapter-{n}.json"
        if not evidence_path.exists():
            bad(f"missing evidence ledger {evidence_path}")
            continue
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        claims = evidence.get("claims", [])
        if len(claims) < 5:
            bad(f"{evidence_path}: expected at least five claims")
        for claim in claims:
            if claim.get("status") not in ALLOWED_EVIDENCE:
                bad(f"{evidence_path}: invalid claim status {claim.get('status')}")

    for path in (ROOT / "assets" / "svg").glob("*.svg"):
        try:
            root = ET.parse(path).getroot()
            ns = "{http://www.w3.org/2000/svg}"
            if not root.attrib.get("viewBox"):
                bad(f"{path}: no viewBox")
            if root.find(ns + "title") is None or root.find(ns + "desc") is None:
                bad(f"{path}: accessible title/desc missing")
        except ET.ParseError as exc:
            bad(f"{path}: XML not parseable: {exc}")

    required = {
        "11": ("copy_process", "TASK_ZOMBIE", "waitpid"),
        "12": ("SA_ONESHOT", "SA_NOMASK", "restorer"),
        "13": ("LOW_MEM", "0x100000", "get_free_page"),
        "14": ("do_wp_page", "do_no_page", "CR2"),
        "15": ("BLOCK_SIZE", "1024", "BADNESS"),
        "16": ("SUPER_MAGIC", "i_zone", "read_super"),
        "17": ("dir_namei", "filp", "open_namei"),
        "18": ("PIPE_SIZE", "SIGPIPE", "ZMAGIC"),
        "19": ("NR_REQUEST", "IN_ORDER", "nr_sectors"),
        "20": ("CHS", "IRQ14", "ramdisk"),
        "21": ("TTY_BUF_SIZE", "copy_to_cooked", "secondary"),
        "22": ("0x24", "0x23", "2400"),
        "23": ("tty_write(0", "Magic SysRq", "do_no_page"),
        "24": ("tools/system.debug", "0x10000", "-s -S"),
        "25": ("__NR_hello", "sys_call_table", "ZMAGIC"),
        "26": ("swap_out", "0.96c", "0.98-pl1", "tss.cr3", "768–1023"),
        "27": ("mem_map[]", "2.6.23", "EEVDF", "bounded loops", "XDP_PASS", "module_init()"),
        "28": ("rd_init", "RAMDISK", "MINOR(CURRENT-&gt;dev) != 1", "sector &lt;&lt; 9", "0x0101"),
    }
    for n, terms in required.items():
        article = (ROOT / "chapters" / f"{n}.html").read_text(encoding="utf-8")
        for term in terms:
            if term not in article:
                bad(f"chapter {n}: missing expected source invariant {term}")

    theme = ROOT / "chapters" / "theme.css"
    if theme.exists() and theme.read_text(encoding="utf-8").startswith("<!--"):
        bad("chapters/theme.css: invalid HTML comment")
    if not (ROOT / "AGENTS.md").is_file():
        bad("missing AGENTS.md")

    if ISSUES:
        for issue in ISSUES:
            print("FAIL", issue)
        return 1
    print("PASS static validation: 28 standalone chapters, redirects, evidence ledgers, local links and SVGs.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
