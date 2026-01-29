from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

from quizzes.models import Quiz

class QuizTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # login (ustawia cookies!)
        self.client.post(
            "/api/login/",
            {"username": "testuser", "password": "testpass123"},
            format="json"
        )

    def test_create_quiz(self):
        response = self.client.post(
            "/api/createQuiz/",
            {"url": "https://www.youtube.com/watch?v=abc123"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(response.data["video_url"], "https://www.youtube.com/watch?v=abc123")

    def test_quiz_detail(self):
        quiz = Quiz.objects.create(
            title="Quiz Detail",
            description="desc",
            video_url="https://youtube.com/2",
            owner=self.user
        )

        response = self.client.get(f"/api/quizzes/{quiz.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Quiz Detail")

    def test_quiz_forbidden_for_other_user(self):
        other_user = User.objects.create_user(
            username="other",
            password="pass123"
        )

        quiz = Quiz.objects.create(
            title="Other quiz",
            description="desc",
            video_url="https://youtube.com/3",
            owner=other_user
        )

        response = self.client.get(f"/api/quizzes/{quiz.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_quiz(self):
        quiz = Quiz.objects.create(
            title="To delete",
            description="desc",
            video_url="https://youtube.com/4",
            owner=self.user
        )

        response = self.client.delete(f"/api/quizzes/{quiz.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)
