from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.templatetags.admin_modify import submit_row

class MockSuperUser:
    def has_perm(self, perm):
        return True

class MockRequest:
    def __init__(self, user):
        self.user = user

class SaveAsNewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.site = AdminSite()

    def test_show_save_as_new(self):
        request = self.factory.get(reverse("admin:index"))
        request.user = self.user
        context = submit_row(request)
        self.assertTrue(context["show_save_as_new"])
