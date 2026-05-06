from django.db import models
from django.db.models import Prefetch
from django.test import TestCase

class User(models.Model):
    email = models.EmailField()
    kind = models.CharField(
        max_length=10, choices=[("ADMIN", "Admin"), ("REGULAR", "Regular")]
    )

class Profile(models.Model):
    full_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class DeferredFieldsTestCase(TestCase):
    def test_only_related_queryset(self):
        user = User.objects.create(
            email="test@example.com",
            kind="ADMIN",
        )
        Profile.objects.create(user=user, full_name="Test Tester")
        queryset = User.objects.only("email").prefetch_related(
            Prefetch(
                "profile",
                queryset=Profile.objects.prefetch_related(
                    Prefetch("user", queryset=User.objects.only("kind"))
                ),
            )
        )
        with self.assertNumQueries(3):
            user = queryset.first()
        with self.assertNumQueries(0):
            self.assertEqual(user.profile.user.kind, "ADMIN")

if __name__ == "__main__":
    import django
    django.setup()
    TestCase.run()
