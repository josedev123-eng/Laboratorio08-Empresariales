import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from quiz.models import Exam, Question, Choice

# Clean existing quiz data
Choice.objects.all().delete()
Question.objects.all().delete()
Exam.objects.all().delete()

exam = Exam.objects.create(
    title="Sample Exam",
    description="This is a sample exam for demonstration",
)

q1 = Question.objects.create(exam=exam, statement="What is Python?", score=2)
Choice.objects.create(question=q1, text="A snake", is_correct=False)
Choice.objects.create(question=q1, text="A programming language", is_correct=True)
Choice.objects.create(question=q1, text="A snake charmer", is_correct=False)
Choice.objects.create(question=q1, text="A type of data", is_correct=False)

q2 = Question.objects.create(exam=exam, statement="Which keyword creates a function?", score=3)
Choice.objects.create(question=q2, text="def", is_correct=True)
Choice.objects.create(question=q2, text="function", is_correct=False)
Choice.objects.create(question=q2, text="import", is_correct=False)
Choice.objects.create(question=q2, text="class", is_correct=False)

print("Seeded exam id:", exam.id)
print("Questions:", exam.questions.count())
for q in exam.questions.all():
    print(f"  - {q.statement}: {q.choices.count()} choices, correct={q.choices.filter(is_correct=True).count()}")
