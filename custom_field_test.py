import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    )
    django.setup()

from django.db import models

class CustomField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        self.model = cls

    def __eq__(self, other):
        if isinstance(other, CustomField):
            return (
                self.creation_counter == other.creation_counter and
                self.model == other.model
            )
        return NotImplemented

    def __hash__(self):
        return hash((self.creation_counter, self.model))

    def __lt__(self, other):
        if isinstance(other, CustomField):
            return (self.creation_counter, self.model) < (other.creation_counter, other.model)
        return NotImplemented

class A(models.Model):
    class Meta:
        abstract = True
    myfield = CustomField()

class B(A):
    pass

class C(A):
    pass

b_field = B._meta.get_field('myfield')
c_field = C._meta.get_field('myfield')

print(f"B.myfield == C.myfield: {b_field == c_field}")
print(f"hash(B.myfield) == hash(C.myfield): {hash(b_field) == hash(c_field)}")
print(f"B.myfield < C.myfield: {b_field < c_field}")
print(f"C.myfield < B.myfield: {c_field < b_field}")
print(f"Length of set: {len({b_field, c_field})}")

print("Script completed successfully, no errors.")
