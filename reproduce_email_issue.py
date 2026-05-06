import os
from django.conf import settings
from django.core.mail import EmailMessage
from unittest.mock import patch

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
settings.configure()

def test_unicode_dns():
    with patch("django.core.mail.message.DNS_NAME", "漢字"):
        email = EmailMessage('subject', '', 'from@example.com', ['to@example.com'])
        email.encoding = 'iso-8859-1'
        try:
            message = email.message()
            print("Message-ID:", message['Message-ID'])
            print("Test passed unexpectedly")
        except UnicodeEncodeError as e:
            print(f"UnicodeEncodeError occurred as expected: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    test_unicode_dns()
    print("Script completed successfully.")
