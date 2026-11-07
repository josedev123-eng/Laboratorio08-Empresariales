"""Create temporary data to demonstrate exam filtering and real pagination."""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from quiz.models import Choice, Exam, Question

# Second exam with one question, so filtering by exam is meaningful.
exam2, created = Exam.objects.get_or_create(
    title="Segundo Examen",
    defaults={"description": "Examen de apoyo para demostrar el filtrado por examen"},
)
if created:
    q, _ = Question.objects.get_or_create(
        exam=exam2,
        statement="¿En qué lenguaje está escrito Django?",
        defaults={"score": 1},
    )
    if not q.choices.exists():
        Choice.objects.create(question=q, text="Python", is_correct=True)
        Choice.objects.create(question=q, text="Java", is_correct=False)
        Choice.objects.create(question=q, text="PHP", is_correct=False)
        Choice.objects.create(question=q, text="C#", is_correct=False)

# Extra exams to force more than one page with PAGE_SIZE = 10.
for i in range(1, 12):
    Exam.objects.get_or_create(
        title=f"Examen de paginación {i:02d}",
        defaults={"description": "Dato temporal para la prueba de paginación"},
    )

print("Segundo Examen id:", exam2.id)
print("Total de exámenes:", Exam.objects.count())
print("Total de preguntas:", Question.objects.count())
