import django
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

# Minimal Django settings configuration
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ],
)

django.setup()

# Create an instance of the AuthenticationForm
form = AuthenticationForm()

# Check if the maxlength attribute is present in the widget attrs
maxlength = form.fields['username'].widget.attrs.get('maxlength')
if maxlength == '254':
    print("Test passed: maxlength attribute is present.")
else:
    print("Test failed: maxlength attribute is not present.")
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

# Minimal Django settings configuration
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ],
)

django.setup()

# Create an instance of the AuthenticationForm
form = AuthenticationForm()

# Check if the maxlength attribute is present in the widget attrs
maxlength = form.fields['username'].widget.attrs.get('maxlength')
if maxlength == '254':
    print("Test passed: maxlength attribute is present.")
else:
    print("Test failed: maxlength attribute is not present.")
