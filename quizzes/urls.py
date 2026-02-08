"""
URL configuration for the quizzes app.

Defines endpoints for:
- Creating new quizzes with their questions.
- Listing all available quizzes.
- Retrieving detailed information about a specific quiz.
"""
from django.urls import path
from quizzes.views import create_quiz, list_quizzes, quiz_detail

urlpatterns = [
    path("createQuiz/", create_quiz),
    path("quizzes/", list_quizzes),
    path("quizzes/<int:quiz_id>/", quiz_detail),   
]
