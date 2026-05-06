from django.forms import modelformset_factory
from django.test import TestCase
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class ModelFormsetFactoryTest(TestCase):
    def test_can_create_false(self):
        FormSet = modelformset_factory(TestModel, fields=['name'], can_create=False)
        formset = FormSet(queryset=TestModel.objects.none())
        
        # Check that no extra forms are created
        self.assertEqual(len(formset.forms), 0)
        
        # Attempt to save a new instance
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-name': 'Test',
        }
        formset = FormSet(data, queryset=TestModel.objects.none())
        
        # Check that the formset is valid
        self.assertTrue(formset.is_valid())
        
        # Attempt to save and check that no new objects are created
        instances = formset.save()
        self.assertEqual(len(instances), 0)
        self.assertEqual(TestModel.objects.count(), 0)

    def test_can_create_true(self):
        FormSet = modelformset_factory(TestModel, fields=['name'], can_create=True)
        
        # Attempt to save a new instance
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-name': 'Test',
        }
        formset = FormSet(data, queryset=TestModel.objects.none())
        
        # Check that the formset is valid
        self.assertTrue(formset.is_valid())
        
        # Attempt to save and check that a new object is created
        instances = formset.save()
        self.assertEqual(len(instances), 1)
        self.assertEqual(TestModel.objects.count(), 1)
        self.assertEqual(TestModel.objects.first().name, 'Test')
    def test_can_create_false_raises_exception(self):
        FormSet = modelformset_factory(TestModel, fields=['name'], can_create=False)
        
        # Attempt to save a new instance
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-name': 'Test',
        }
        formset = FormSet(data, queryset=TestModel.objects.none())
        
        # Check that the formset is valid
        self.assertTrue(formset.is_valid())
        
        # Attempt to save and check that an exception is raised
        with self.assertRaises(ValueError):
            formset.save()
        
        # Ensure no objects were created
        self.assertEqual(TestModel.objects.count(), 0)

