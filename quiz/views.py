from rest_framework import viewsets
from .models import Exam, Question, Choice
from .serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Choice."""
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Question."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Exam."""
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer