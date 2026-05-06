from django.apps import AppConfig

class TestAppConfig(AppConfig):
    name = 'test_app'
    class Meta:
        app_label = 'test_app'
