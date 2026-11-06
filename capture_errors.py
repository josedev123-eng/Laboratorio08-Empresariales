"""Capture the real 400 HTML responses rendered by the DRF browsable API."""
import json
import os
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"
OUT = os.path.join("quiz", "static", "capturas")
os.makedirs(OUT, exist_ok=True)

cases = [
    (
        "error_missing_title.html",
        f"{BASE}/quiz/exams/",
        {"description": "Falta el campo title"},
    ),
    (
        "error_wrong_type.html",
        f"{BASE}/quiz/exams/",
        {"title": {"not": "a string"}, "description": "Tipo incorrecto"},
    ),
    (
        "error_two_correct.html",
        f"{BASE}/quiz/questions/",
        {
            "statement": "Pregunta con dos opciones correctas",
            "exam": 4,
            "score": 1,
            "choices": [
                {"text": "Opcion A", "is_correct": True},
                {"text": "Opcion B", "is_correct": True},
                {"text": "Opcion C", "is_correct": False},
                {"text": "Opcion D", "is_correct": False},
            ],
        },
    ),
]

for filename, url, payload in cases:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "text/html"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            status, body = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read().decode()

    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"{filename}: HTTP {status} -> {path} ({len(body)} bytes)")
