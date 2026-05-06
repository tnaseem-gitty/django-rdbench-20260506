from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.test import TestCase

UserModel = get_user_model()

class AuthenticateTestCase(TestCase):
    def test_authenticate_with_none_username_and_password(self):
        backend = ModelBackend()
        with self.assertNumQueries(0):
            user = backend.authenticate(None, username=None, password=None)
            self.assertIsNone(user)

if __name__ == "__main__":
    TestCase.main()
