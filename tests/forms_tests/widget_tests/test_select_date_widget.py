from django.forms import SelectDateWidget
from django.test import TestCase

class TestSelectDateWidget(TestCase):
    def test_select_date_widget_with_large_values(self):
        widget = SelectDateWidget()
        data = {
            'field_year': '1234567821345678',
            'field_month': '1',
            'field_day': '1'
        }
        result = widget.value_from_datadict(data, {}, 'field')
        self.assertEqual(result, '1234567821345678-1-1')

    def test_select_date_widget_with_valid_values(self):
        widget = SelectDateWidget()
        data = {
            'field_year': '2023',
            'field_month': '6',
            'field_day': '15'
        }
        result = widget.value_from_datadict(data, {}, 'field')
        self.assertEqual(result, '2023-06-15')
