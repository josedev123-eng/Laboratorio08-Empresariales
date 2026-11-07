from rest_framework import viewsets
from .models import Exam, Question, Choice
from .serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Choice."""

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Question.

    Permite filtrar por examen con ``?exam=<id>`` y buscar por texto del
    enunciado con ``?search=<texto>``.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        exam = self.request.query_params.get("exam")
        search = self.request.query_params.get("search")

        if exam:
            try:
                queryset = queryset.filter(exam_id=int(exam))
            except (TypeError, ValueError):
                queryset = queryset.none()

        if search:
            queryset = queryset.filter(statement__icontains=search)

        return queryset


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Exam.

    Permite buscar exámenes por título con ``?search=<texto>``.
    """

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset
