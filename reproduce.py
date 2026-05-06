import django
from django.conf import settings

settings.configure(DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}, INSTALLED_APPS=[
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sites',
    'tests.delete',  # Replace with the actual app name containing models A, B, and C
], SECRET_KEY='test_secret_key', USE_TZ=True)

django.setup()

from django.contrib.auth.models import User
from django.db import models
from django.db.models import OuterRef, Subquery
from django.test import TestCase
from django.utils.functional import SimpleLazyObject

class A(models.Model):
    class Meta:
        app_label = 'tests.delete'

class B(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE)
    class Meta:
        app_label = 'tests.delete'

class C(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        app_label = 'tests.delete'

class BugTestCase(TestCase):
    def test_bug(self):
        owner_user = (
            B.objects.filter(a=OuterRef("pk"))
            .annotate(owner_user=Subquery(C.objects.values("owner")))
            .values("owner_user")
        )
        user = SimpleLazyObject(lambda: User.objects.create_user("testuser"))
        A.objects.annotate(owner_user=Subquery(owner_user)).filter(
            owner_user=user
        )
print("Script completed successfully, no errors.")
