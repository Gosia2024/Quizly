"""
Serializers for the Quizly API.
Handles the conversion between Quiz/Question models and JSON format,
including nested options and questions.
"""
from rest_framework import serializers
from .models import Quiz, Question, QuestionOption

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model.
    
    Includes 'question_options' as a list of strings using SlugRelatedField,
    providing a flat representation of available choices.
    """
    question_options = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="option_text"
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
        ]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quiz model.
    
    Nested Relationship:
    Includes all related 'questions' using the QuestionSerializer.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions"
        ]
