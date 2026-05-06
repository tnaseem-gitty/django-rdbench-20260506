from django.db import migrations
from django.db.migrations.operations.models import AddIndex, RemoveIndex
from django.db.models import Index
from django.test import TestCase

class IndexOptimizationTests(TestCase):
    def test_add_remove_index_reduction(self):
        index = Index(fields=['name'], name='test_index')
        add_index = AddIndex('TestModel', index)
        remove_index = RemoveIndex('TestModel', 'test_index')

        # Test AddIndex followed by RemoveIndex
        reduced = add_index.reduce(remove_index, 'testapp')
        self.assertEqual(reduced, [])

        # Test RemoveIndex followed by AddIndex
        reduced = remove_index.reduce(add_index, 'testapp')
        self.assertEqual(reduced, [])

    def test_no_reduction_for_different_indexes(self):
        index1 = Index(fields=['name'], name='test_index_1')
        index2 = Index(fields=['age'], name='test_index_2')
        add_index1 = AddIndex('TestModel', index1)
        add_index2 = AddIndex('TestModel', index2)
        remove_index1 = RemoveIndex('TestModel', 'test_index_1')
        remove_index2 = RemoveIndex('TestModel', 'test_index_2')

        # Test no reduction for different indexes
        reduced = add_index1.reduce(remove_index2, 'testapp')
        self.assertEqual(reduced, [add_index1])

        reduced = remove_index1.reduce(add_index2, 'testapp')
        self.assertEqual(reduced, [remove_index1])

if __name__ == '__main__':
    import unittest
    unittest.main()
