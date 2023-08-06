import uuid
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from marketplace.accounts.views import UserPermissionViewSet, UserViewSet
from marketplace.core.tests.base import APIBaseTestCase
from marketplace.accounts.models import User, ProjectAuthorization


class BaseTest(APIBaseTestCase):
    def setUp(self):
        super().setUp()

class StatisticTestCase(BaseTest):
    project_uuid = uuid.uuid4()
    url = reverse("user-list")

    view_class = UserViewSet

    @property
    def view(self):
        return self.view_class.as_view({"post": "create"})

    def test_retrieve(self):
        print(self.url)