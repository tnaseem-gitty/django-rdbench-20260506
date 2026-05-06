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
    ValidationError,
)

class MF(MultiValueField):
    def __init__(self):
        fields = [
            CharField(required=False),
            CharField(required=True),
        ]
        widgets = [f.widget for f in fields]
        super().__init__(
            fields=fields,
            widget=MultiWidget(widgets=widgets),
            require_all_fields=False,
            required=False,
        )

    def compress(self, data_list):
        if data_list:
            return ' '.join(data_list)
        return None

    def clean(self, value):
        if not value or len(value) < 2 or not value[1]:
            raise ValidationError("Second field is required.")
        return super().clean(value)

class F(Form):
    mf = MF()

# Test case 1: Both fields empty (should now fail)
f1 = F({
    'mf_0': '',
    'mf_1': '',
})
print("Test case 1 (both empty):")
print(f"is_valid: {f1.is_valid()}")
print(f"errors: {f1.errors}")

# Test case 2: First field non-empty, second field empty (should fail)
f2 = F({
    'mf_0': 'xxx',
    'mf_1': '',
})
print("\nTest case 2 (first non-empty, second empty):")
print(f"is_valid: {f2.is_valid()}")
print(f"errors: {f2.errors}")

# Test case 3: Both fields non-empty (should pass)
f3 = F({
    'mf_0': 'xxx',
    'mf_1': 'yyy',
})
print("\nTest case 3 (both non-empty):")
print(f"is_valid: {f3.is_valid()}")
print(f"errors: {f3.errors}")

print("\nScript completed successfully, no errors.")
