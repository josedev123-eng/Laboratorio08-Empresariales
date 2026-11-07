"""Capture POST, PATCH, DELETE, filter, search and pagination from the real API."""
import json

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
OUT = "docs/capturas"


def shot(page, name):
    page.screenshot(path=f"{OUT}/{name}", full_page=True)
    print(f"  saved {name}")


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    # ---------------------------------------------------------------- POST
    print("POST /quiz/exams/")
    page.goto(f"{BASE}/quiz/exams/")
    page.fill("#post-object-form input[name=title]", "Examen creado desde la API")
    page.fill(
        "#post-object-form textarea[name=description]",
        "Creado desde la API navegable para la evidencia del laboratorio",
    )
    with page.expect_response(
        lambda r: r.request.method == "POST" and r.url.rstrip("/").endswith("/quiz/exams")
    ) as info:
        page.click("#post-object-form button")
    print("  status:", info.value.status)
    page.wait_for_timeout(800)
    print("  page shows 201:", "201 Created" in page.content())
    shot(page, "11_post_create.png")

    # Find the created exam id through the API.
    resp = page.request.get(f"{BASE}/quiz/exams/?search=Examen creado desde la API")
    created_id = resp.json()["results"][0]["id"]
    print("  created id:", created_id)

    # --------------------------------------------------------------- PATCH
    print(f"PATCH /quiz/exams/{created_id}/")
    page.goto(f"{BASE}/quiz/exams/{created_id}/")
    page.click("a[name='raw-tab']")
    page.wait_for_selector("#id__content", state="visible")
    page.fill(
        "#id__content",
        json.dumps(
            {"description": "Descripción actualizada mediante PATCH"},
            ensure_ascii=False,
        ),
    )
    with page.expect_response(
        lambda r: r.request.method == "PATCH" and f"/quiz/exams/{created_id}/" in r.url
    ) as info:
        page.click("#put-generic-content-form button[data-method='PATCH']")
    print("  status:", info.value.status)
    page.wait_for_timeout(800)
    print("  page shows 200:", "200 OK" in page.content())
    shot(page, "12_patch_update.png")

    # -------------------------------------------------------------- DELETE
    print(f"DELETE /quiz/exams/{created_id}/")
    page.goto(f"{BASE}/quiz/exams/{created_id}/")
    page.click("button[data-target='#deleteModal']")
    page.wait_for_selector("#deleteModal", state="visible")
    with page.expect_response(
        lambda r: r.request.method == "DELETE" and f"/quiz/exams/{created_id}/" in r.url
    ) as info:
        page.click("#deleteModal .btn-danger")
    print("  status:", info.value.status)
    page.wait_for_timeout(1000)
    print("  page shows 204:", "204 No Content" in page.content())
    shot(page, "13_delete.png")

    # -------------------------------------------------- FILTER BY EXAM (id 6)
    print("GET /quiz/questions/?exam=6")
    page.goto(f"{BASE}/quiz/questions/?exam=6")
    page.wait_for_load_state("load")
    shot(page, "14_filter_exam.png")

    # -------------------------------------------------------------- SEARCH
    print("GET /quiz/questions/?search=Python")
    page.goto(f"{BASE}/quiz/questions/?search=Python")
    page.wait_for_load_state("load")
    shot(page, "06_search_python.png")

    # ----------------------------------------------------- PAGINATION PAGES
    print("GET /quiz/exams/?page=1")
    page.goto(f"{BASE}/quiz/exams/?page=1")
    page.wait_for_load_state("load")
    shot(page, "07_pagination.png")

    print("GET /quiz/exams/?page=2")
    page.goto(f"{BASE}/quiz/exams/?page=2")
    page.wait_for_load_state("load")
    shot(page, "15_pagination_page2.png")

    browser.close()

print("done")
