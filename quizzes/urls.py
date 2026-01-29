from django.urls import path
from quizzes.views import create_quiz, list_quizzes, quiz_detail

urlpatterns = [
    path("createQuiz/", create_quiz),
    path("quizzes/", list_quizzes),
    path("quizzes/<int:quiz_id>/", quiz_detail),
    # path('quizzes/<int:quiz_id>/delete/', quiz_delete),

]
