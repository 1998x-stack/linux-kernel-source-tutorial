#!/usr/bin/env python3
"""Playwright smoke check; requires a running HTTP server and installed Chromium."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip('/') if len(sys.argv)>1 else 'http://127.0.0.1:8000'
def main():
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for width in (1440,390,360):
            page=browser.new_page(viewport={'width':width,'height':900}, device_scale_factor=1)
            page.on('pageerror',lambda e: errors.append(str(e)))
            page.goto(URL+'/', wait_until='networkidle')
            assert page.locator('h1').count()==1
            assert page.locator('.course-card').count()==28
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'home overflow at {width}'
            page.locator('#lesson-search').fill('head.s')
            assert page.locator('.course-card:visible').count()>=1
            page.locator('#lesson-search').fill('')
            page.get_by_role('button',name='已重构').click()
            assert page.locator('.course-card:visible').count()==5
            page.get_by_role('button',name='全部').click()
            assert page.locator('.course-card:visible').count()==28
            for n in range(1,6):
                path=f'{n:02d}.html'
                page.goto(URL+'/chapters/'+path, wait_until='networkidle')
                assert page.locator('h1').count()==1,f'{path} H1'
                assert page.locator('section').count()>=5,f'{path} sections'
                assert page.locator('details').count()>=1
                page.locator('details').first.locator('summary').click()
                assert page.locator('details').first.evaluate('(el)=>el.open')
                assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'{path} overflow at {width}'
                for img in page.locator('figure img').all():
                    assert img.evaluate('(el)=>el.complete && el.naturalWidth>0'),f'{path} image broken'
            page.close()
        browser.close()
    assert not errors,f'JavaScript errors: {errors}'
    print('PASS browser smoke: 1440/390/360; 28 cards; 5 chapters; filtering, details, images, overflow')
if __name__=='__main__':
    main()
