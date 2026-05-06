from django import forms
from django.test import TestCase

class MultipleCheckboxTest(TestCase):
    def test_multiple_checkboxes(self):
        class TestForm(forms.Form):
            checkbox1 = forms.BooleanField(required=False)
            checkbox2 = forms.BooleanField(required=False)
            checkbox3 = forms.BooleanField(required=False)

        form = TestForm(initial={'checkbox1': True, 'checkbox2': False, 'checkbox3': True})
        self.assertInHTML('<input type=checkbox name=checkbox1 checked id=id_checkbox1>', str(form['checkbox1']))
        self.assertInHTML('<input type=checkbox name=checkbox2 id=id_checkbox2>', str(form['checkbox2']))
        self.assertInHTML('<input type=checkbox name=checkbox3 checked id=id_checkbox3>', str(form['checkbox3']))

