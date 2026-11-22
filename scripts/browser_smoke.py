#!/usr/bin/env python3
"""Playwright smoke check for all 28 chapters; requires local HTTP server and Chromium."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"

def verify_images(page, path):
    images = page.locator("figure img")
    assert images.count() >= 1, f"{path}: no figures"
    for img in images.all():
        img.scroll_into_view_if_needed()
        img.evaluate("(el) => { el.loading = 'eager'; }")
        handle = img.element_handle()
        page.wait_for_function(
            "(el) => el.complete && el.naturalWidth > 0",
            arg=handle,
            timeout=10000,
        )
        assert img.evaluate("(el) => el.naturalWidth > 0"), (
            f"{path}: broken image {img.get_attribute('src')}"
        )

def main():
    errors = []
    reports = Path("reports/browser-qa")
    reports.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for width in (1440, 390, 360):
            page = browser.new_page(
                viewport={"width": width, "height": 900},
                device_scale_factor=1,
            )
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(URL + "/", wait_until="networkidle")
            assert page.locator("h1").count() == 1
            assert page.locator(".course-card").count() == 28
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (
                f"home overflow at {width}"
            )
            page.keyboard.press("Tab")
            assert page.locator(".skip").evaluate("(el) => document.activeElement === el"), (
                "homepage skip link is not the first keyboard target"
            )
            page.screenshot(path=str(reports / f"home-{width}.png"), full_page=True)
            page.locator("#lesson-search").fill("head.s")
            assert page.locator(".course-card:visible").count() >= 1
            page.locator("#lesson-search").fill("")
            page.get_by_role("button", name="已重构").click()
            assert page.locator(".course-card:visible").count() == 28
            page.get_by_role("button", name="全部").click()
            assert page.locator(".course-card:visible").count() == 28

            for number in range(1, 29):
                chapter = f"{number:02d}.html"
                page.goto(URL + "/chapters/" + chapter, wait_until="networkidle")
                assert page.locator("h1").count() == 1, f"{chapter}: H1"
                assert page.locator("section").count() >= 5, f"{chapter}: sections"
                assert page.locator("details").count() >= 1, f"{chapter}: self-check"
                page.locator("details").first.locator("summary").click()
                assert page.locator("details").first.evaluate("(el) => el.open")
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (
                    f"{chapter}: document overflow at {width}"
                )
                verify_images(page, chapter)
                if number in (21, 22, 23, 24, 25, 26, 27, 28):
                    page.screenshot(
                        path=str(reports / f"chapter-{number:02d}-{width}.png"),
                        full_page=True,
                    )
                if number == 28 and width == 1440:
                    page.emulate_media(media="print")
                    assert page.locator("h1").is_visible(), "chapter 28 print H1"
                    page.emulate_media(media="screen")
            page.close()
        browser.close()
    assert not errors, f"JavaScript errors: {errors}"
    print(
        "PASS browser smoke: 1440/390/360; 28 cards and chapters; "
        "filter, keyboard skip, details, figures, print and overflow"
    )

if __name__ == "__main__":
    main()
