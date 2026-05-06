from django.test import TestCase
from django.db.models import Prefetch
from .models import User, Profile

class DeferredFieldsTest(TestCase):
    def test_only_related_queryset(self):
        user = User.objects.create(
            email="test@example.com",
            kind="ADMIN",
        )
        Profile.objects.create(user=user, full_name="Test Tester")
        queryset = User.objects.only("email", "kind").prefetch_related(
            Prefetch(
                "profile",
                queryset=Profile.objects.select_related('user').only('user__kind', 'full_name')
            )
        )
        with self.assertNumQueries(2):
            user = queryset.first()
            profile = user.profile  # Force loading of profile
            inner_user = profile.user  # Force loading of inner user
            print("Outer user deferred fields:", user.get_deferred_fields())
            print("Inner user deferred fields:", inner_user.get_deferred_fields())
            print("Outer user kind:", getattr(user, 'kind', 'Not loaded'))
            print("Inner user kind:", getattr(inner_user, 'kind', 'Not loaded'))
        
        print("Accessing user.profile.user.kind")
        with self.assertNumQueries(0):
            kind = inner_user.kind
            print("Accessed kind:", kind)
            self.assertEqual(kind, "ADMIN")
        
        print("Accessing outer user.kind")
        with self.assertNumQueries(0):
            outer_kind = user.kind
            print("Accessed outer kind:", outer_kind)
            self.assertEqual(outer_kind, "ADMIN")
        
        print("Script completed successfully, no errors.")
