# TextChoices Serialization Fix

## Issue
When using a CharField with choices from a TextChoices enum, the string representation of the field returns the enum name (e.g., 'MyChoice.FIRST_CHOICE') instead of the actual value (e.g., 'first').

## Reproduction
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class MyChoice(models.TextChoices):
    FIRST_CHOICE = "first", _("The first choice, it is")
    SECOND_CHOICE = "second", _("The second choice, it is")

class MyObject(models.Model):
    my_str_value = models.CharField(max_length=10, choices=MyChoice.choices)

obj = MyObject.objects.create(my_str_value=MyChoice.FIRST_CHOICE)
print(str(obj.my_str_value))  # Outputs: 'MyChoice.FIRST_CHOICE' instead of 'first'
```

## Fix
The proposed fix adds a `__str__` method to the TextChoices class to return the value instead of the enum name:

```python
class TextChoices(models.TextChoices):
    def __str__(self):
        return self.value
```

This change ensures that when the field value is converted to a string, it returns the actual value rather than the enum name.

## Patch
A patch file `django_text_choices_fix.patch` is provided with this fix. Apply it to the appropriate Django source file (likely `django/db/models/enums.py`).
