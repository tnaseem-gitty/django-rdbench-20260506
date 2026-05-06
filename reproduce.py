from django import forms
from django.contrib.postgres.forms.array import SplitArrayField

class TestForm(forms.Form):
    field = SplitArrayField(forms.BooleanField(), size=5, initial=[True, False, False, False, False])

form = TestForm()
for subfield in form['field']:
    print(subfield)

