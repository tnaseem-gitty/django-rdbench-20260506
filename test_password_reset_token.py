import os
import django
from django.conf import settings
from django.core.management import call_command

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
        SECRET_KEY='dummy-secret-key',
    )

django.setup()

# Now we can safely import Django components
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def run_test():
    # Run migrations
    call_command('migrate')

    # Create a test user
    User = get_user_model()
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    # Generate a token
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)

    # Verify the token
    print("Initial token verification:", token_generator.check_token(user, token))

    # Change the user's email
    user.email = 'newemail@example.com'
    user.save()

    # Verify the token again
    print("Token verification after email change:", token_generator.check_token(user, token))

    print("Test completed.")

if __name__ == "__main__":
    run_test()
