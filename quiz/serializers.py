from rest_framework import serializers
from .models import Exam, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for the Choice model (answer option)."""

    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for the Question model.

    Choices travel nested inside the question, while the exam travels as an
    identifier (PrimaryKeyRelatedField). A private validation guarantees that
    every question has exactly one correct choice.
    """

    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "statement", "exam", "score", "choices"]

    def validate(self, data):
        choices = data.get("choices", [])
        correct = sum(1 for choice in choices if choice.get("is_correct"))
        if correct != 1:
            raise serializers.ValidationError(
                {"choices": "Exactly one choice must be marked as correct."}
            )
        return data

    def create(self, validated_data):
        choices_data = validated_data.pop("choices")
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop("choices", None)
        instance.statement = validated_data.get("statement", instance.statement)
        instance.score = validated_data.get("score", instance.score)
        instance.exam = validated_data.get("exam", instance.exam)
        instance.save()
        if choices_data is not None:
            instance.choices.all().delete()
            for choice_data in choices_data:
                Choice.objects.create(question=instance, **choice_data)
        return instance


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for the Exam model.

    Questions travel nested (read-only); new questions are created through the
    question endpoint so the exam is always referenced by identifier.
    """

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "title", "description", "creation_date", "questions"]
        read_only_fields = ["creation_date"]
