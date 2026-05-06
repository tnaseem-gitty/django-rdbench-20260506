from django.test import TestCase
from django.forms import ModelForm, RadioSelect
from django.db import models

class BatchData(models.Model):
    name = models.CharField(max_length=100)

class TestRun(models.Model):
    data_file = models.ForeignKey(BatchData, on_delete=models.SET_NULL, null=True, blank=False)

class TestRunForm(ModelForm):
    class Meta:
        model = TestRun
        fields = ['data_file']
        widgets = {'data_file': RadioSelect()}

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
