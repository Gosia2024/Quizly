from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegisterUserTests(APITestCase):

    def test_register_user_success(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "test@test.com",
                "password": "test1234",
                "confirmed_password": "test1234"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_password_mismatch(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "test@test.com",
                "password": "test1234",
                "confirmed_password": "wrong"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test1234"
        )

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "test1234"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "wrong"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutUserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test1234"
        )

        login = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "test1234"
            },
            format="json"
        )

        self.client.cookies = login.cookies

    def test_logout_success(self):
        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RefreshTokenTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test1234"
        )

        login = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "test1234"
            },
            format="json"
        )

        self.client.cookies = login.cookies

    def test_refresh_token_success(self):
        response = self.client.post(reverse("token_refresh"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)

