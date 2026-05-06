from django.test import TestCase
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class TestModelChoiceFieldValidation(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_modelchoicefield_invalid_choice(self):
        field = ModelChoiceField(queryset=User.objects.all())
        
        # Test with an invalid choice
        with self.assertRaises(ValidationError) as cm:
            field.clean('invalid_id')
        
        self.assertEqual(cm.exception.code, 'invalid_choice')
        self.assertIn('invalid_id', str(cm.exception))

    def test_modelmultiplechoicefield_invalid_choice(self):
        field = ModelMultipleChoiceField(queryset=User.objects.all())
        
        # Test with an invalid choice
        with self.assertRaises(ValidationError) as cm:
            field.clean(['invalid_id'])
        
        self.assertEqual(cm.exception.code, 'invalid_pk_value')
        self.assertIn('invalid_id', str(cm.exception))
