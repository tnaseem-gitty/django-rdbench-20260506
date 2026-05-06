from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=TestModel.objects.all())

# Create a form instance with an invalid choice
form = TestForm(data={'choice': 'invalid_choice'})

try:
    form.is_valid()
except ValidationError as e:
    print(e.messages)
