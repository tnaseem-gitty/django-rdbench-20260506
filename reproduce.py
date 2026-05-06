import django
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import add

# Configure Django settings
settings.configure(USE_I18N=True)
django.setup()

# Create a lazy string
lazy_string = _("lazy")

# Concatenate a normal string with the lazy string using the add filter
print("Starting concatenation test")
try:
    result = add("normal", lazy_string)
    print(f"Result: {result}")
except TypeError as e:
    print(f"Error: {e}")
