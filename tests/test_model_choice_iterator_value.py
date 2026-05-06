import unittest
from django.forms.models import ModelChoiceIteratorValue

class TestModelChoiceIteratorValue(unittest.TestCase):
    def test_hashable(self):
        value = ModelChoiceIteratorValue(1, "test_instance")
        try:
            hash(value)
            # If we can hash it, we can add it to a set
            test_set = {value}
            self.assertEqual(len(test_set), 1)
            print("ModelChoiceIteratorValue is hashable")
        except TypeError:
            self.fail("ModelChoiceIteratorValue is not hashable")

if __name__ == '__main__':
    unittest.main()
