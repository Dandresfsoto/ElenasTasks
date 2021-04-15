import random
from typing import (
    Iterable,
    Union,
    List
)

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .factories.tags import TagFactory
from .factories.tasks import TaskFactory
from .factories.users import UserFactory


class TestTagsViews(TestCase):
    TAGS_API_URL = reverse("tasks:tags_api")
    OBTAIN_AUTH_TOKEN_URL = reverse("tasks:obtain_auth_token")

    def setUp(self):
        self.password = 'ArPg44628/**/'

        self.user_1 = UserFactory()
        self.user_1.set_password(self.password)
        self.user_1.save()

        self.user_2 = UserFactory()
        self.user_2.set_password(self.password)
        self.user_2.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user_1.username,
            "password": self.password
        })
        self.token_user_1 = response.data.get("token")

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user_2.username,
            "password": self.password
        })
        self.token_user_2 = response.data.get("token")

    @staticmethod
    def create_multiple_tags_to_user(user: UserFactory) -> List:
        return [TagFactory(user=user) for _ in range(0, random.randint(1, 100))]

    @staticmethod
    def get_http_authorization(token):
        return f"Bearer {token}"

    def check_asserts_pagination_structure(self, response):
        self.assertIn("count", response.data.keys())
        self.assertIsInstance(response.data.get("count"), int)

        self.assertIn("next", response.data.keys())
        self.assertIsInstance(response.data.get("next"), Union[str, None].__args__)

        self.assertIn("previous", response.data.keys())
        self.assertIsInstance(response.data.get("previous"), Union[str, None].__args__)

        self.assertIn("results", response.data.keys())
        self.assertIsInstance(response.data.get("results"), Iterable)

    @staticmethod
    def get_url_with_pk(name: str, pk: str):
        return reverse(name, kwargs={"pk": pk})

    def test_get_tags_of_auth_users(self):
        tags_user_1 = self.create_multiple_tags_to_user(self.user_1)
        tags_user_2 = self.create_multiple_tags_to_user(self.user_2)

        response_user_1 = self.client.get(
            path=self.TAGS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        response_user_2 = self.client.get(
            path=self.TAGS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_2)
        )

        self.assertEquals(tags_user_1.__len__(), response_user_1.data.get("count"))
        self.assertEquals(tags_user_2.__len__(), response_user_2.data.get("count"))

    def test_get_tags_pagination_structure(self):
        self.create_multiple_tags_to_user(self.user_1)
        response = self.client.get(
            path=self.TAGS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.check_asserts_pagination_structure(response=response)

    def test_create_user_tag(self):

        user_1_tags_list = self.client.get(
            path=self.TAGS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data.get("results")
        self.assertEquals(user_1_tags_list.__len__(), 0)

        json_tag = {"name": "TAG"}
        response = self.client.post(
            path=self.TAGS_API_URL,
            data=json_tag,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        user_1_tags_list = self.client.get(
            path=self.TAGS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data.get("results")
        self.assertEquals(user_1_tags_list.__len__(), 1)

    def test_filter_tag_by_name_and_check_response(self):

        self.client.post(
            path=self.TAGS_API_URL,
            data={"name": "QA"},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.client.post(
            path=self.TAGS_API_URL,
            data={"name": "DEVOPS"},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )

        user_1_tags_list = self.client.get(
            path=self.TAGS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data.get("results")
        self.assertEquals(user_1_tags_list.__len__(), 2)

        tag_name_to_filter = "QA"

        user_1_filter_tags_response = self.client.get(
            path=f"{self.TAGS_API_URL}?name={tag_name_to_filter}",
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        user_1_filter_tags_list = user_1_filter_tags_response.data.get("results")
        self.assertEquals(user_1_filter_tags_list.__len__(), 1)
        self.check_asserts_pagination_structure(user_1_filter_tags_response)

    def test_retrieve_tag(self):
        tag = self.client.post(
            path=self.TAGS_API_URL,
            data={"name": "QA"},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data
        self.assertIn("id", tag)

        tag_retrieve_response = self.client.get(
            path=self.get_url_with_pk("tasks:tag_detail_api", tag["id"]),
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        tag_retrieve = tag_retrieve_response.data

        self.assertEquals(tag_retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIn("id", tag_retrieve)
        self.assertEquals(tag["id"], tag_retrieve["id"])

    def test_update_tag(self):
        tag = self.client.post(
            path=self.TAGS_API_URL,
            data={"name": "QA"},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data

        new_tag_name = "DEVOPS"

        tag_update_response = self.client.put(
            path=self.get_url_with_pk("tasks:tag_detail_api", tag["id"]),
            data={"name": new_tag_name},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1),
            content_type='application/json'
        )
        tag_update = tag_update_response.data

        self.assertEquals(tag_update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(tag["id"], tag_update["id"])

        tag_retrieve = self.client.get(
            path=self.get_url_with_pk("tasks:tag_detail_api", tag["id"]),
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1),
        ).data
        self.assertEquals(tag_retrieve["name"], new_tag_name)

    def test_delete_tag(self):
        tag = self.client.post(
            path=self.TAGS_API_URL,
            data={"name": "QA"},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data

        tag_delete_response = self.client.delete(
            path=self.get_url_with_pk("tasks:tag_detail_api", tag["id"]),
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.assertEquals(tag_delete_response.status_code, status.HTTP_200_OK)
        self.assertIn("status", tag_delete_response.data)
        self.assertEquals("deleted", tag_delete_response.data.get("status"))


class TestTasksViews(TestCase):
    TASKS_API_URL = reverse("tasks:tasks_api")
    OBTAIN_AUTH_TOKEN_URL = reverse("tasks:obtain_auth_token")

    def setUp(self):
        self.password = 'ArPg44628/**/'

        self.user_1 = UserFactory()
        self.user_1.set_password(self.password)
        self.user_1.save()

        self.user_2 = UserFactory()
        self.user_2.set_password(self.password)
        self.user_2.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user_1.username,
            "password": self.password
        })
        self.token_user_1 = response.data.get("token")

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user_2.username,
            "password": self.password
        })
        self.token_user_2 = response.data.get("token")

    @staticmethod
    def create_multiple_task_to_user(user: UserFactory) -> List:
        return [TaskFactory(user=user) for _ in range(0, random.randint(1, 100))]

    @staticmethod
    def create_multiple_tags_to_user(user: UserFactory) -> List:
        return [TagFactory(user=user).id for _ in range(0, random.randint(1, 100))]

    @staticmethod
    def get_http_authorization(token):
        return f"Bearer {token}"

    def check_asserts_pagination_structure(self, response):
        self.assertIn("count", response.data.keys())
        self.assertIsInstance(response.data.get("count"), int)

        self.assertIn("next", response.data.keys())
        self.assertIsInstance(response.data.get("next"), Union[str, None].__args__)

        self.assertIn("previous", response.data.keys())
        self.assertIsInstance(response.data.get("previous"), Union[str, None].__args__)

        self.assertIn("results", response.data.keys())
        self.assertIsInstance(response.data.get("results"), Iterable)

    @staticmethod
    def get_url_with_pk(name: str, pk: str):
        return reverse(name, kwargs={"pk": pk})

    def check_asserts_query_params(self, token, query_param: str, query_param_value: str, response_len: int):

        user_filter_list_response = self.client.get(
            path=f"{self.TASKS_API_URL}?{query_param}={query_param_value}",
            HTTP_AUTHORIZATION=self.get_http_authorization(token)
        ).data.get("results")
        self.assertEquals(user_filter_list_response.__len__(), response_len)

    def test_get_tasks_of_auth_users(self):
        tasks_user_1 = self.create_multiple_task_to_user(self.user_1)
        tasks_user_2 = self.create_multiple_task_to_user(self.user_2)

        response_user_1 = self.client.get(
            path=self.TASKS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        response_user_2 = self.client.get(
            path=self.TASKS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_2)
        )

        self.assertEquals(tasks_user_1.__len__(), response_user_1.data.get("count"))
        self.assertEquals(tasks_user_2.__len__(), response_user_2.data.get("count"))

    def test_get_tasks_pagination_structure(self):
        self.create_multiple_task_to_user(self.user_1)
        response = self.client.get(
            path=self.TASKS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.check_asserts_pagination_structure(response=response)

    def test_create_user_task(self):

        user_1_tasks_list = self.client.get(
            path=self.TASKS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data.get("results")
        self.assertEquals(user_1_tasks_list.__len__(), 0)

        json_task = {
            "name": "Task Name",
            "tags": self.create_multiple_tags_to_user(user=self.user_1),
            "description": "Task description",
            "priority": "LOW"
        }
        response = self.client.post(
            path=self.TASKS_API_URL,
            data=json_task,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        user_1_tasks_list = self.client.get(
            path=self.TASKS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data.get("results")
        self.assertEquals(user_1_tasks_list.__len__(), 1)

    def test_filter_task_by_query_params(self):

        self.client.post(
            path=self.TASKS_API_URL,
            data={
                "name": "Task Name_1",
                "tags": self.create_multiple_tags_to_user(user=self.user_1),
                "description": "Task description_1",
                "priority": "LOW"
            },
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.client.post(
            path=self.TASKS_API_URL,
            data={
                "name": "Task Name_2",
                "tags": self.create_multiple_tags_to_user(user=self.user_1),
                "description": "Task description_2",
                "priority": "LOWEST"
            },
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )

        user_1_tags_list = self.client.get(
            path=self.TASKS_API_URL,
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data.get("results")
        self.assertEquals(user_1_tags_list.__len__(), 2)

        self.check_asserts_query_params(
            token=self.token_user_1, query_param="name", query_param_value="Name_1", response_len=1
        )
        self.check_asserts_query_params(
            token=self.token_user_1, query_param="description", query_param_value="description_2", response_len=1
        )
        self.check_asserts_query_params(
            token=self.token_user_1, query_param="priority", query_param_value="LOW", response_len=1
        )
        self.check_asserts_query_params(
            token=self.token_user_1, query_param="is_completed", query_param_value="false", response_len=2
        )

    def test_retrieve_task(self):
        task = self.client.post(
            path=self.TASKS_API_URL,
            data={
                "name": "Task Name",
                "tags": self.create_multiple_tags_to_user(user=self.user_1),
                "description": "Task description",
                "priority": "LOW"
            },
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data
        self.assertIn("id", task)

        task_retrieve_response = self.client.get(
            path=self.get_url_with_pk("tasks:tasks_detail_api", task["id"]),
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        task_retrieve = task_retrieve_response.data

        self.assertEquals(task_retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIn("id", task_retrieve)
        self.assertEquals(task["id"], task_retrieve["id"])

    def test_update_partial_task(self):
        task = self.client.post(
            path=self.TASKS_API_URL,
            data={
                "name": "Task Name",
                "tags": self.create_multiple_tags_to_user(user=self.user_1),
                "description": "Task description",
                "priority": "LOW"
            },
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data

        new_task_name = "Task Name updated"

        task_update_response = self.client.put(
            path=self.get_url_with_pk("tasks:tasks_detail_api", task["id"]),
            data={"name": new_task_name},
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1),
            content_type='application/json'
        )
        task_updated = task_update_response.data

        self.assertEquals(task_update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(task["id"], task_updated["id"])

        task_retrieve = self.client.get(
            path=self.get_url_with_pk("tasks:tasks_detail_api", task["id"]),
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1),
        ).data
        self.assertEquals(task_retrieve["name"], new_task_name)

    def test_delete_tag(self):
        task = self.client.post(
            path=self.TASKS_API_URL,
            data={
                "name": "Task Name",
                "tags": self.create_multiple_tags_to_user(user=self.user_1),
                "description": "Task description",
                "priority": "LOW"
            },
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        ).data

        task_delete_response = self.client.delete(
            path=self.get_url_with_pk("tasks:tasks_detail_api", task["id"]),
            HTTP_AUTHORIZATION=self.get_http_authorization(self.token_user_1)
        )
        self.assertEquals(task_delete_response.status_code, status.HTTP_200_OK)
        self.assertIn("status", task_delete_response.data)
        self.assertEquals("deleted", task_delete_response.data.get("status"))
