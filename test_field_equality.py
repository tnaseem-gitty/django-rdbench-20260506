import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'test_app',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    )
    django.setup()

from test_app.models import B, C

b_field = B._meta.get_field('myfield')
c_field = C._meta.get_field('myfield')

print(f"B.myfield == C.myfield: {b_field == c_field}")
print(f"hash(B.myfield) == hash(C.myfield): {hash(b_field) == hash(c_field)}")
print(f"B.myfield < C.myfield: {b_field < c_field}")
print(f"C.myfield < B.myfield: {c_field < b_field}")
print(f"Length of set: {len({b_field, c_field})}")

print("Script completed successfully, no errors.")
