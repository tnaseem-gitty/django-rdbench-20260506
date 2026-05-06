from django.test import TestCase
from .models import BatchData, TestRun, TestRunForm

class RadioSelectTestCase(TestCase):
    def setUp(self):
        BatchData.objects.create(name="First Data File")
        BatchData.objects.create(name="Second Data File")

    def test_radio_select_no_blank_option(self):
        form = TestRunForm()
        rendered_form = form.as_p()
        self.assertNotIn('value=""', rendered_form)
        self.assertNotIn('---------', rendered_form)

    def test_radio_select_with_blank_option(self):
        TestRun._meta.get_field('data_file').blank = True
        form = TestRunForm()
        rendered_form = form.as_p()
        self.assertIn('value=""', rendered_form)
        self.assertIn('---------', rendered_form)
