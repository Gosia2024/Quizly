from django.urls import path

from quizzes.views import create_quiz, quiz_detail
urlpatterns = [

    path("createQuiz/", create_quiz),
    path("quizzes/<int:quiz_id>/", quiz_detail),
]