"""Capture real HTTP responses from the Quiz REST API for Lab08 evidence."""
import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"
lines = []


def record(title, method, url, payload=None, expected=None):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            status = r.status
            body = r.read().decode()
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode()

    lines.append(f"## {title}")
    lines.append(f"- **Method:** {method}")
    lines.append(f"- **URL:** {url}")
    if payload is not None:
        lines.append(f"- **Body:** `{json.dumps(payload)}`")
    lines.append(f"- **Expected status:** {expected}")
    lines.append(f"- **Actual status:** {status}")
    try:
        pretty = json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except Exception:
        pretty = body if body else "(empty body)"
    lines.append("- **Response:**")
    lines.append("```json")
    lines.append(pretty[:2000])
    lines.append("```")
    lines.append("")
    print(f"{title}: {method} {url} -> {status}")
    return status, body


def get_json(url):
    with urllib.request.urlopen(url) as r:
        return r.status, json.loads(r.read())


# 1..4 Read operations over the three resources
record("1. API root", "GET", f"{BASE}/quiz/", expected=200)
record("2. List exams", "GET", f"{BASE}/quiz/exams/", expected=200)
record("3. List questions", "GET", f"{BASE}/quiz/questions/", expected=200)
record("4. List choices", "GET", f"{BASE}/quiz/choices/", expected=200)

# 5 Create exam
_, created_exam = record(
    "5. Create exam (POST)",
    "POST",
    f"{BASE}/quiz/exams/",
    {"title": "Exam created from REST API", "description": "Evidence for Lab08"},
    expected=201,
)
exam_id = json.loads(created_exam)["id"] if created_exam else None

# 6 Retrieve detail
record("6. Retrieve exam detail", "GET", f"{BASE}/quiz/exams/{exam_id}/", expected=200)

# 7 Partial update
record(
    "7. Partial update exam (PATCH)",
    "PATCH",
    f"{BASE}/quiz/exams/{exam_id}/",
    {"description": "Updated description via PATCH"},
    expected=200,
)

# 8 Valid question with nested choices and exactly one correct
_, created_q = record(
    "8. Create question with nested choices (POST)",
    "POST",
    f"{BASE}/quiz/questions/",
    {
        "statement": "What does the DRF acronym stand for?",
        "exam": exam_id,
        "score": 2,
        "choices": [
            {"text": "Django REST Framework", "is_correct": True},
            {"text": "Django Reactive Forms", "is_correct": False},
            {"text": "Data Rendering Format", "is_correct": False},
            {"text": "Dynamic Response Factory", "is_correct": False},
        ],
    },
    expected=201,
)
question_id = json.loads(created_q)["id"] if created_q else None

# 9 Detail now shows the nested question and its choices
record(
    "9. Exam detail shows nested question and choices",
    "GET",
    f"{BASE}/quiz/exams/{exam_id}/",
    expected=200,
)

# 10 Error: missing required field
record(
    "10. Error - missing required field (POST)",
    "POST",
    f"{BASE}/quiz/exams/",
    {"description": "Missing title"},
    expected=400,
)

# 11 Error: wrong type (title must be a string)
record(
    "11. Error - wrong type (POST)",
    "POST",
    f"{BASE}/quiz/exams/",
    {"title": {"not": "a string"}, "description": "Wrong type"},
    expected=400,
)

# 12 Error: question without exactly one correct choice
record(
    "12. Error - question must have exactly one correct choice (POST)",
    "POST",
    f"{BASE}/quiz/questions/",
    {
        "statement": "Question with two correct choices",
        "exam": exam_id,
        "score": 1,
        "choices": [
            {"text": "Option A", "is_correct": True},
            {"text": "Option B", "is_correct": True},
            {"text": "Option C", "is_correct": False},
            {"text": "Option D", "is_correct": False},
        ],
    },
    expected=400,
)

# 13 Delete the created question, then the created exam
record("13. Delete question", "DELETE", f"{BASE}/quiz/questions/{question_id}/", expected=204)
record("14. Delete exam", "DELETE", f"{BASE}/quiz/exams/{exam_id}/", expected=204)

# 15 Filtering / search / pagination
record("15. Search questions by text", "GET", f"{BASE}/quiz/questions/?search=Python", expected=200)
record("16. Pagination check", "GET", f"{BASE}/quiz/exams/?page=1", expected=200)

output = "# Lab08 REST API Evidence - Real HTTP Responses\n\n" + "\n".join(lines)
with open("api_evidence.md", "w", encoding="utf-8") as f:
    f.write(output)
print("\nEvidence saved to api_evidence.md")
