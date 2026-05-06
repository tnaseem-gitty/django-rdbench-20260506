import os
import django
from django.conf import settings
from django.test.utils import get_runner
from django.apps import apps
from django.contrib import admin

if __name__ == "__main__":
    # Configure the test environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.conf.global_settings')
    
    # Update the existing settings
    settings.configure(
        DEBUG=True,
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
        ROOT_URLCONF='django.contrib.admin.test_urls',
        SECRET_KEY='fake-key',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
    )

    django.setup()

    # Ensure all apps are populated
    apps.populate(settings.INSTALLED_APPS)

    # Get the test runner
    TestRunner = get_runner(settings)

    # Run the test
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(["django.contrib.admin.test_admin_search"])

    # Exit with non-zero status if there were failures
    exit(bool(failures))
