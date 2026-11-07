# Lab08 - API RESTful con Django REST Framework

## Recursos expuestos

Base URL: `http://127.0.0.1:8000`

| Recurso | Direccion | Metodo | Cuerpo de ejemplo | Respuesta esperada |
|---------|-----------|--------|-------------------|--------------------|
| Raiz API | `/quiz/` | GET | - | 200 OK |
| Examenes | `/quiz/exams/` | GET | - | 200 OK (lista paginada) |
| Examenes | `/quiz/exams/{id}/` | GET | - | 200 OK (con preguntas anidadas) |
| Examenes | `/quiz/exams/` | POST | `{"title": "Nuevo", "description": "..."}` | 201 Created |
| Examenes | `/quiz/exams/{id}/` | PATCH | `{"description": "Actualizada"}` | 200 OK |
| Examenes | `/quiz/exams/{id}/` | DELETE | - | 204 No Content |
| Preguntas | `/quiz/questions/` | GET | - | 200 OK (con opciones anidadas) |
| Preguntas | `/quiz/questions/` | POST | `{"statement": "...", "exam": 1, "score": 2, "choices": [{"text": "A", "is_correct": true}, ...]}` | 201 Created |
| Preguntas | `/quiz/questions/{id}/` | DELETE | - | 204 No Content |
| Opciones | `/quiz/choices/` | GET | - | 200 OK |
| Opciones | `/quiz/choices/` | POST | `{"text": "Opcion", "is_correct": true}` | 201 Created |

## Errores controlados

| Caso | Cuerpo | Codigo | Mensaje |
|------|--------|--------|---------|
| Campo obligatorio ausente | `{"description": "..."}` sin `title` | 400 | `This field is required.` |
| Tipo incorrecto | `{"title": {"not": "a string"}}` | 400 | `Not a valid string.` |
| Opcion correcta invalida | pregunta con 0 o 2 opciones `is_correct=true` | 400 | `Exactly one choice must be marked as correct.` |

## Relaciones

- Las **opciones** (`Choice`) viajan **anidadas** dentro de la **pregunta** (`Question.choices`).
- El **examen** (`Exam`) se referencia por **identificador** dentro de la pregunta (`exam: <id>`).
- El detalle de un examen incluye sus preguntas anidadas y sus opciones.

## Filtrado y paginacion

- Filtrado por examen: `/quiz/questions/?exam=6`
- Busqueda por enunciado: `/quiz/questions/?search=Python`
- Busqueda de examenes por titulo: `/quiz/exams/?search=Sample`
- Paginacion: `/quiz/exams/?page=1` y `/quiz/exams/?page=2` (PAGE_SIZE = 10; con mas de
  10 examenes la respuesta incluye `next` y `previous`)

## Estructura del proyecto

```
src/
  config/        settings.py, urls.py, wsgi.py, asgi.py
  quiz/          models.py, serializers.py, views.py, urls.py, migrations/
  docs/          capturas/ (evidencias del laboratorio), lab08_api.md
  templates/     plantillas de la aplicacion
  library/       aplicacion de biblioteca del curso
  media/         archivos subidos
  movies/        aplicacion de peliculas del curso
  news/          aplicacion de noticias del curso
  manage.py      punto de entrada de Django
```

## Configuracion

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}
```
