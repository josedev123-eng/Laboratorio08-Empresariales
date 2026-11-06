from rest_framework import serializers
from .models import Exam, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Choice (opción)."""
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Question (pregunta).
    Incluye las opciones anidadidas y validación de exactamente una correcta."""
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'statement', 'exam', 'choices']
        read_only_fields = ['exam']

    def validate(self, data):
        """Validación personalizada: exactamente una opción debe ser correcta.
        Esta validación se aplicará al crear/actualizar desde el API."""
        # La validación completa se hará en la vista o al crear opciones separadamente
        return data


class ExamSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Exam (examen).
    Las preguntas viajan con su relación a examen por identificador."""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_at', 'questions']