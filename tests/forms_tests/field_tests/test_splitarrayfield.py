from django.test import TestCase
from django.forms import SplitArrayField, BooleanField

class SplitArrayFieldTest(TestCase):
    def test_boolean_split_array_field(self):
        class TestForm(forms.Form):
            bool_array = SplitArrayField(BooleanField(), size=3, remove_trailing_nulls=False)

        form = TestForm(initial={'bool_array': [True, False, True]})
        self.assertHTMLEqual(
            str(form['bool_array']),
            '<input type=checkbox name=bool_array_0 checked id=id_bool_array_0>'
            '<input type=checkbox name=bool_array_1 id=id_bool_array_1>'
            '<input type=checkbox name=bool_array_2 checked id=id_bool_array_2>'
        )

