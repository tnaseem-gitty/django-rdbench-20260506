import os
import django
from django.conf import settings

# Set up Django configuration
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )
    django.setup()

from django.forms import (
    Form,
    CharField,
    MultiValueField,
    MultiWidget,
)

class MF(MultiValueField):
    widget = MultiWidget
    def __init__(self):
        fields = [
            CharField(required=False),
            CharField(required=True),
        ]
        widget = self.widget(widgets=[
            f.widget
            for f in fields
        ], attrs={})
        super(MF, self).__init__(
            fields=fields,
            widget=widget,
            require_all_fields=False,
            required=False,
        )
    def compress(self, value):
        return []

class F(Form):
    mf = MF()

# Test case 1: Both fields empty
f1 = F({
    'mf_0': '',
    'mf_1': '',
})
print("Test case 1 (both empty):")
print(f"is_valid: {f1.is_valid()}")
print(f"errors: {f1.errors}")

# Test case 2: First field non-empty, second field empty
f2 = F({
    'mf_0': 'xxx',
    'mf_1': '',
})
print("\nTest case 2 (first non-empty, second empty):")
print(f"is_valid: {f2.is_valid()}")
print(f"errors: {f2.errors}")

print("\nScript completed successfully, no errors.")
