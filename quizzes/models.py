"""
Models for the Quizly application.
Defines the structure for Quizzes, Questions, and their respective Options.
"""
from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    """
    Represents a single quiz created by a user.
    Linked to a video URL and contains multiple questions.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Represents a specific question within a quiz.
    Each question has a title and a correct answer.
    """
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_title = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionOption(models.Model):
    """
    Represents multiple-choice options for a given question.
    """
    question = models.ForeignKey(Question, related_name="question_options", on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)