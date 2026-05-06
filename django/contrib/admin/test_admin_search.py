import os
from django.test import TestCase, override_settings, TransactionTestCase
from django.contrib.admin.options import ModelAdmin
from django.db import models, connection
from django.http import HttpRequest
from django.conf import settings
from django.test.utils import isolate_apps
from django.db.transaction import atomic

# Configure the test database
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF='django.contrib.admin.sites',
        SECRET_KEY='fake-key',
    )

import django
django.setup()

@isolate_apps('django.contrib.admin')
class AdminSearchTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class MockModel(models.Model):
            name = models.CharField(max_length=100)
            description = models.TextField()

            class Meta:
                app_label = 'admin'

        class MockModelAdmin(ModelAdmin):
            search_fields = ['name', 'description']

        cls.MockModel = MockModel
        cls.MockModelAdmin = MockModelAdmin

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        connection.disable_constraint_checking()
        try:
            with atomic():
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(self.MockModel)
        finally:
            connection.enable_constraint_checking()

        self.model_admin = self.MockModelAdmin(self.MockModel, None)
        self.request = HttpRequest()
        self.MockModel.objects.create(name="Test1", description="Description1")
        self.MockModel.objects.create(name="Test2", description="Description2")
        self.MockModel.objects.create(name="Other", description="OtherDescription")

    def tearDown(self):
        super().tearDown()
        connection.disable_constraint_checking()
        try:
            with atomic():
                with connection.schema_editor() as schema_editor:
                    schema_editor.delete_model(self.MockModel)
        finally:
            connection.enable_constraint_checking()

    def test_search_results(self):
        queryset = self.MockModel.objects.all()
        search_term = "Test Description"
        filtered_qs, _ = self.model_admin.get_search_results(self.request, queryset, search_term)
        
        # Check that we get 2 results (Test1 and Test2)
        self.assertEqual(filtered_qs.count(), 2)
        
        # Check that 'Other' is not in the results
        self.assertFalse(filtered_qs.filter(name="Other").exists())

        # Check that we're not doing separate queries for each word
        self.assertNumQueries(1, lambda: list(filtered_qs))

if __name__ == '__main__':
    from django.core.management import call_command
    call_command('test', 'django.contrib.admin.test_admin_search')
