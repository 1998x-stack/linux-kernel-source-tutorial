#!/usr/bin/env python3
"""Static link, structure, article and standalone SVG checks. No dependencies."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ISSUES = []
class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.links = []
        self.images = []
        self.sections = []
        self.ids = []
        self.svgs = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h1': self.h1 += 1
        if tag == 'section': self.sections.append(a.get('id'))
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'link' and a.get('href'): self.links.append(a['href'])
        if tag == 'script' and a.get('src'): self.links.append(a['src'])
        if tag == 'img':
            self.images.append(a)
            if a.get('src'): self.links.append(a['src'])
        if tag == 'svg': self.svgs += 1

def bad(message):
    ISSUES.append(message)

def check_refs(path, parsed):
    for href in parsed.links:
        if not href or href.startswith(('#','https://','http://','mailto:','data:')):
            continue
        if href.startswith(('javascript:','//')):
            bad(f'{path}: unsafe or protocol-relative URL {href}')
            continue
        target = (path.parent / href.split('#',1)[0].split('?',1)[0]).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.exists():
            bad(f'{path}: missing local resource {href}')
    for img in parsed.images:
        if not img.get('alt'):
            bad(f'{path}: image missing meaningful alt: {img.get("src")}')
    if len(parsed.ids) != len(set(parsed.ids)):
        bad(f'{path}: duplicated HTML IDs')

def main():
    courses = json.loads((ROOT/'courses.json').read_text(encoding='utf-8'))
    if len(courses.get('chapters',[])) != 28: bad('courses.json: expected 28 chapters')
    for i in range(1,29):
        num=f'{i:02d}'
        path=ROOT/'chapters'/f'{num}.html'
        if not path.exists(): bad(f'missing {path}'); continue
        h=Inspector()
        data=path.read_text(encoding='utf-8')
        h.feed(data)
        if i <= 10:
            if h.h1!=1: bad(f'{path}: expected 1 H1, got {h.h1}')
            if len(h.sections)<5: bad(f'{path}: requires >= 5 self-contained sections')
            if not h.images: bad(f'{path}: visual explanation missing')
            if 'v0.11' not in data and 'Linux 0.11' not in data: bad(f'{path}: version scope missing')
            if 'Olah-style' in data or '本讲义介绍' in data: bad(f'{path}: workflow boilerplate found')
            if '<details' not in data: bad(f'{path}: missing native interactive self-check')
        if i>10 and 'theme.css' not in data: bad(f'{path}: legacy stylesheet unexpectedly missing')
        check_refs(path,h)
        redirect=ROOT/f'{num}.html'
        if not redirect.exists() or f'chapters/{num}.html' not in redirect.read_text(encoding='utf-8'):
            bad(f'{redirect}: legacy redirect missing')
        meta=courses['chapters'][i-1]
        if meta.get('file')!=f'chapters/{num}.html':
            bad(f'courses.json: chapter {num} has incorrect file')
    home=Inspector()
    home.feed((ROOT/'index.html').read_text(encoding='utf-8'))
    if home.h1!=1: bad('index.html: expected one H1')
    check_refs(ROOT/'index.html',home)
    for p in (ROOT/'assets/svg').glob('*.svg'):
        try:
            tree=ET.parse(p)
            r=tree.getroot()
            if not r.attrib.get('viewBox'): bad(f'{p}: no viewBox')
            ns='{http://www.w3.org/2000/svg}'
            if r.find(ns+'title') is None or r.find(ns+'desc') is None:
                bad(f'{p}: accessible title/desc missing')
        except ET.ParseError as exc: bad(f'{p}: XML not parseable: {exc}')
    if (ROOT/'chapters/theme.css').read_text(encoding='utf-8').startswith('<!--'):
        bad('chapters/theme.css: invalid HTML comment')
    if not (ROOT/'AGENTS.md').is_file(): bad('missing AGENTS.md')
    if ISSUES:
        for issue in ISSUES: print('FAIL',issue)
        return 1
    print('PASS static validation: 28 chapters, 28 redirects, 10 redesigned articles, links and SVGs.')
    return 0
if __name__=='__main__':
    sys.exit(main())
