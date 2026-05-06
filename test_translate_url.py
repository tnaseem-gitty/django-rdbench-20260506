import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

from django.conf import settings
settings.configure(
    DEBUG=True,
    USE_TZ=True,
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.locale.LocaleMiddleware',
    ],
    LANGUAGE_CODE='en',
    LANGUAGES=[('en', 'English'), ('fr', 'French')],
    USE_I18N=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
)

import django
django.setup()

from django.test import TestCase
from django.urls import path
from django.urls.base import translate_url

def dummy_view(request):
    pass

urlpatterns = [
    path('optional/<str:param>/', dummy_view, name='optional'),
    path('required/<str:param>/', dummy_view, name='required'),
]

class TranslateURLTestCase(TestCase):
    def test_translate_url_with_optional_param(self):
        url = '/optional/'
        translated_url = translate_url(url, 'fr')
        self.assertEqual(translated_url, '/fr/optional/')

    def test_translate_url_with_required_param(self):
        url = '/required/value/'
        translated_url = translate_url(url, 'fr')
        self.assertEqual(translated_url, '/fr/required/value/')

if __name__ == '__main__':
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=2)
    failures = test_runner.run_tests([__name__])
    if failures:
        print("Tests failed")
    else:
        print("All tests passed")
