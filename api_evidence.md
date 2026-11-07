# Lab08 REST API Evidence - Real HTTP Responses

## 1. API root
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "exams": "http://127.0.0.1:8000/quiz/exams/",
  "questions": "http://127.0.0.1:8000/quiz/questions/",
  "choices": "http://127.0.0.1:8000/quiz/choices/"
}
```

## 2. List exams
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/exams/
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "title": "Sample Exam",
      "description": "This is a sample exam for demonstration",
      "creation_date": "2026-11-06T20:02:09.064595Z",
      "questions": [
        {
          "id": 2,
          "statement": "What is Python?",
          "exam": 4,
          "score": 2,
          "choices": [
            {
              "id": 5,
              "text": "A snake",
              "is_correct": false
            },
            {
              "id": 6,
              "text": "A programming language",
              "is_correct": true
            },
            {
              "id": 7,
              "text": "A snake charmer",
              "is_correct": false
            },
            {
              "id": 8,
              "text": "A type of data",
              "is_correct": false
            }
          ]
        },
        {
          "id": 3,
          "statement": "Which keyword creates a function?",
          "exam": 4,
          "score": 3,
          "choices": [
            {
              "id": 9,
              "text": "def",
              "is_correct": true
            },
            {
              "id": 10,
              "text": "function",
              "is_correct": false
            },
            {
              "id": 11,
              "text": "import",
              "is_correct": false
            },
            {
              "id": 12,
              "text": "class",
              "is_correct": false
            }
          ]
        }
      ]
    }
  ]
}
```

## 3. List questions
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/questions/
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "statement": "What is Python?",
      "exam": 4,
      "score": 2,
      "choices": [
        {
          "id": 5,
          "text": "A snake",
          "is_correct": false
        },
        {
          "id": 6,
          "text": "A programming language",
          "is_correct": true
        },
        {
          "id": 7,
          "text": "A snake charmer",
          "is_correct": false
        },
        {
          "id": 8,
          "text": "A type of data",
          "is_correct": false
        }
      ]
    },
    {
      "id": 3,
      "statement": "Which keyword creates a function?",
      "exam": 4,
      "score": 3,
      "choices": [
        {
          "id": 9,
          "text": "def",
          "is_correct": true
        },
        {
          "id": 10,
          "text": "function",
          "is_correct": false
        },
        {
          "id": 11,
          "text": "import",
          "is_correct": false
        },
        {
          "id": 12,
          "text": "class",
          "is_correct": false
        }
      ]
    }
  ]
}
```

## 4. List choices
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/choices/
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "text": "A snake",
      "is_correct": false
    },
    {
      "id": 6,
      "text": "A programming language",
      "is_correct": true
    },
    {
      "id": 7,
      "text": "A snake charmer",
      "is_correct": false
    },
    {
      "id": 8,
      "text": "A type of data",
      "is_correct": false
    },
    {
      "id": 9,
      "text": "def",
      "is_correct": true
    },
    {
      "id": 10,
      "text": "function",
      "is_correct": false
    },
    {
      "id": 11,
      "text": "import",
      "is_correct": false
    },
    {
      "id": 12,
      "text": "class",
      "is_correct": false
    }
  ]
}
```

## 5. Create exam (POST)
- **Method:** POST
- **URL:** http://127.0.0.1:8000/quiz/exams/
- **Body:** `{"title": "Exam created from REST API", "description": "Evidence for Lab08"}`
- **Expected status:** 201
- **Actual status:** 201
- **Response:**
```json
{
  "id": 5,
  "title": "Exam created from REST API",
  "description": "Evidence for Lab08",
  "creation_date": "2026-11-06T20:02:25.706457Z",
  "questions": []
}
```

## 6. Retrieve exam detail
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/exams/5/
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "id": 5,
  "title": "Exam created from REST API",
  "description": "Evidence for Lab08",
  "creation_date": "2026-11-06T20:02:25.706457Z",
  "questions": []
}
```

## 7. Partial update exam (PATCH)
- **Method:** PATCH
- **URL:** http://127.0.0.1:8000/quiz/exams/5/
- **Body:** `{"description": "Updated description via PATCH"}`
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "id": 5,
  "title": "Exam created from REST API",
  "description": "Updated description via PATCH",
  "creation_date": "2026-11-06T20:02:25.706457Z",
  "questions": []
}
```

## 8. Create question with nested choices (POST)
- **Method:** POST
- **URL:** http://127.0.0.1:8000/quiz/questions/
- **Body:** `{"statement": "What does the DRF acronym stand for?", "exam": 5, "score": 2, "choices": [{"text": "Django REST Framework", "is_correct": true}, {"text": "Django Reactive Forms", "is_correct": false}, {"text": "Data Rendering Format", "is_correct": false}, {"text": "Dynamic Response Factory", "is_correct": false}]}`
- **Expected status:** 201
- **Actual status:** 201
- **Response:**
```json
{
  "id": 4,
  "statement": "What does the DRF acronym stand for?",
  "exam": 5,
  "score": 2,
  "choices": [
    {
      "id": 13,
      "text": "Django REST Framework",
      "is_correct": true
    },
    {
      "id": 14,
      "text": "Django Reactive Forms",
      "is_correct": false
    },
    {
      "id": 15,
      "text": "Data Rendering Format",
      "is_correct": false
    },
    {
      "id": 16,
      "text": "Dynamic Response Factory",
      "is_correct": false
    }
  ]
}
```

## 9. Exam detail shows nested question and choices
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/exams/5/
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "id": 5,
  "title": "Exam created from REST API",
  "description": "Updated description via PATCH",
  "creation_date": "2026-11-06T20:02:25.706457Z",
  "questions": [
    {
      "id": 4,
      "statement": "What does the DRF acronym stand for?",
      "exam": 5,
      "score": 2,
      "choices": [
        {
          "id": 13,
          "text": "Django REST Framework",
          "is_correct": true
        },
        {
          "id": 14,
          "text": "Django Reactive Forms",
          "is_correct": false
        },
        {
          "id": 15,
          "text": "Data Rendering Format",
          "is_correct": false
        },
        {
          "id": 16,
          "text": "Dynamic Response Factory",
          "is_correct": false
        }
      ]
    }
  ]
}
```

## 10. Error - missing required field (POST)
- **Method:** POST
- **URL:** http://127.0.0.1:8000/quiz/exams/
- **Body:** `{"description": "Missing title"}`
- **Expected status:** 400
- **Actual status:** 400
- **Response:**
```json
{
  "title": [
    "This field is required."
  ]
}
```

## 11. Error - wrong type (POST)
- **Method:** POST
- **URL:** http://127.0.0.1:8000/quiz/exams/
- **Body:** `{"title": {"not": "a string"}, "description": "Wrong type"}`
- **Expected status:** 400
- **Actual status:** 400
- **Response:**
```json
{
  "title": [
    "Not a valid string."
  ]
}
```

## 12. Error - question must have exactly one correct choice (POST)
- **Method:** POST
- **URL:** http://127.0.0.1:8000/quiz/questions/
- **Body:** `{"statement": "Question with two correct choices", "exam": 5, "score": 1, "choices": [{"text": "Option A", "is_correct": true}, {"text": "Option B", "is_correct": true}, {"text": "Option C", "is_correct": false}, {"text": "Option D", "is_correct": false}]}`
- **Expected status:** 400
- **Actual status:** 400
- **Response:**
```json
{
  "choices": [
    "Exactly one choice must be marked as correct."
  ]
}
```

## 13. Delete question
- **Method:** DELETE
- **URL:** http://127.0.0.1:8000/quiz/questions/4/
- **Expected status:** 204
- **Actual status:** 204
- **Response:**
```json
(empty body)
```

## 14. Delete exam
- **Method:** DELETE
- **URL:** http://127.0.0.1:8000/quiz/exams/5/
- **Expected status:** 204
- **Actual status:** 204
- **Response:**
```json
(empty body)
```

## 15. Search questions by text
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/questions/?search=Python
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "statement": "What is Python?",
      "exam": 4,
      "score": 2,
      "choices": [
        {
          "id": 5,
          "text": "A snake",
          "is_correct": false
        },
        {
          "id": 6,
          "text": "A programming language",
          "is_correct": true
        },
        {
          "id": 7,
          "text": "A snake charmer",
          "is_correct": false
        },
        {
          "id": 8,
          "text": "A type of data",
          "is_correct": false
        }
      ]
    }
  ]
}
```

## 16. Pagination check
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/exams/?page=1
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "title": "Sample Exam",
      "description": "This is a sample exam for demonstration",
      "creation_date": "2026-11-06T20:02:09.064595Z",
      "questions": [
        {
          "id": 2,
          "statement": "What is Python?",
          "exam": 4,
          "score": 2,
          "choices": [
            {
              "id": 5,
              "text": "A snake",
              "is_correct": false
            },
            {
              "id": 6,
              "text": "A programming language",
              "is_correct": true
            },
            {
              "id": 7,
              "text": "A snake charmer",
              "is_correct": false
            },
            {
              "id": 8,
              "text": "A type of data",
              "is_correct": false
            }
          ]
        },
        {
          "id": 3,
          "statement": "Which keyword creates a function?",
          "exam": 4,
          "score": 3,
          "choices": [
            {
              "id": 9,
              "text": "def",
              "is_correct": true
            },
            {
              "id": 10,
              "text": "function",
              "is_correct": false
            },
            {
              "id": 11,
              "text": "import",
              "is_correct": false
            },
            {
              "id": 12,
              "text": "class",
              "is_correct": false
            }
          ]
        }
      ]
    }
  ]
}
```

## 17. Filter questions by exam
- **Method:** GET
- **URL:** http://127.0.0.1:8000/quiz/questions/?exam=6
- **Expected status:** 200
- **Actual status:** 200
- **Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "statement": "¿En qué lenguaje está escrito Django?",
      "exam": 6,
      "score": 1,
      "choices": [
        {
          "id": 17,
          "text": "Python",
          "is_correct": true
        },
        {
          "id": 18,
          "text": "Java",
          "is_correct": false
        },
        {
          "id": 19,
          "text": "PHP",
          "is_correct": false
        },
        {
          "id": 20,
          "text": "C#",
          "is_correct": false
        }
      ]
    }
  ]
}
```
