from django.test import TestCase
from tests.models import OneModel, TwoModel

class SelfReferentialFKTestCase(TestCase):
    def setUp(self):
        root = OneModel.objects.create(oneval=1)
        child1 = OneModel.objects.create(root=root, oneval=2)
        child2 = OneModel.objects.create(root=root, oneval=3)
        TwoModel.objects.create(record=root, twoval=10)
        TwoModel.objects.create(record=child1, twoval=20)
        TwoModel.objects.create(record=child2, twoval=30)

    def test_order_by_root_id(self):
        qs = TwoModel.objects.filter(record__oneval__in=[1, 2, 3])
        qs = qs.order_by("record__root_id")
        
        # Check the SQL query
        sql = str(qs.query)
        self.assertNotIn("LEFT OUTER JOIN", sql)
        self.assertIn("INNER JOIN", sql)
        self.assertIn("ORDER BY", sql)
        self.assertIn("record__root_id", sql)
        
        # Check the results
        results = list(qs.values_list('twoval', flat=True))
        self.assertEqual(results, [10, 20, 30])

    def test_order_by_root(self):
        qs = TwoModel.objects.filter(record__oneval__in=[1, 2, 3])
        qs = qs.order_by("record__root")
        
        # Check the SQL query
        sql = str(qs.query)
        self.assertNotIn("LEFT OUTER JOIN", sql)
        self.assertIn("INNER JOIN", sql)
        self.assertIn("ORDER BY", sql)
        self.assertIn("record__root", sql)
        
        # Check the results
        results = list(qs.values_list('twoval', flat=True))
        self.assertEqual(results, [10, 20, 30])
