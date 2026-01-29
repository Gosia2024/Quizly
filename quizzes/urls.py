from django.urls import path

from quizzes.views import create_quiz, list_quizzes, quiz_detail
urlpatterns = [

    path("createQuiz/", create_quiz),
path("quizzes/<int:id>/", quiz_detail),
    path('quizzes/', list_quizzes),
    path('createQuiz/', create_quiz),

]