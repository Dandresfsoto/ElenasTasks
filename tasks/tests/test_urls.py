from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .factories.users import UserFactory


class TestUrls(TestCase):
    TASK_HEALTH_CHECK_URL = reverse("tasks:health_check")
    TAGS_API_URL = reverse("tasks:tags_api")
    TASKS_API_URL = reverse("tasks:tasks_api")
    OBTAIN_AUTH_TOKEN_URL = reverse("tasks:obtain_auth_token")

    def setUp(self):
        self.password = 'ArPg44628/**/'
        self.user = self.user_1 = UserFactory()
        self.user.set_password(self.password)
        self.user.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user.username,
            "password": self.password
        })
        self.token = response.data.get("token")

    def test_health_check_url_response(self):
        response = self.client.get(self.TASK_HEALTH_CHECK_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_tags_api_url_response_unauthorized(self):
        response = self.client.get(self.TAGS_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_api_url_response_authorized(self):
        response = self.client.get(self.TAGS_API_URL, {}, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_tasks_api_url_response_unauthorized(self):
        response = self.client.get(self.TASKS_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tasks_api_url_response_authorized(self):
        response = self.client.get(self.TASKS_API_URL, {}, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
