from rest_framework import serializers
from .models import Quiz, Question, QuestionOption

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["option_text"]

class QuestionSerializer(serializers.ModelSerializer):
    question_options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id","title","description","created_at","updated_at","video_url","questions"]
