import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils.functional import SimpleLazyObject
from django.core.management import call_command

# Models
class A(models.Model):
    class Meta:
        app_label = 'test_app'

class B(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE)
    class Meta:
        app_label = 'test_app'

class C(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        app_label = 'test_app'

# Test Case
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

# Run migrations and test
if __name__ == "__main__":
    call_command('migrate')
    test_case = BugTestCase()
    test_case.test_bug()
    print("Test completed. If no error occurred, the bug might be fixed.")
