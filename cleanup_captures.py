"""Remove the temporary pagination exams, keeping Sample Exam and Segundo Examen."""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from quiz.models import Exam

deleted, _ = Exam.objects.filter(title__startswith="Examen de paginación").delete()
Exam.objects.filter(title="Examen creado desde la API").delete()

print("Registros eliminados:", deleted)
for exam in Exam.objects.all():
    print(f"  {exam.id}: {exam.title} ({exam.questions.count()} preguntas)")
