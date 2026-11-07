"""Re-capture the pagination pages at readable scale (viewport only)."""
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
OUT = "docs/capturas"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1150})

    page.goto(f"{BASE}/quiz/exams/?page=1")
    page.wait_for_load_state("load")
    page.screenshot(path=f"{OUT}/07_pagination.png")
    print("saved 07_pagination.png")

    page.goto(f"{BASE}/quiz/exams/?page=2")
    page.wait_for_load_state("load")
    page.screenshot(path=f"{OUT}/15_pagination_page2.png")
    print("saved 15_pagination_page2.png")

    browser.close()
