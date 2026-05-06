from django.forms import TextInput
from django.forms.boundfield import BoundWidget
from django.forms.renderers import DjangoTemplates
from django.test import SimpleTestCase

class TestBoundWidget(SimpleTestCase):
    def test_id_for_label(self):
        widget = TextInput()
        renderer = DjangoTemplates()
        
        # Test when id is provided in attrs
        bound_widget = BoundWidget(widget, {'name': 'test', 'value': 'value', 'attrs': {'id': 'custom_id'}, 'index': 0}, renderer)
        self.assertEqual(bound_widget.id_for_label, 'custom_id')
        
        # Test when id is not provided in attrs
        bound_widget = BoundWidget(widget, {'name': 'test', 'value': 'value', 'attrs': {}, 'index': 0}, renderer)
        self.assertEqual(bound_widget.id_for_label, 'id_test_0')
