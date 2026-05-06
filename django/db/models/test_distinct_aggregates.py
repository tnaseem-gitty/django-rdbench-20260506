from django.db import models
from django.db.models import Avg, Sum
from django.test import TestCase

class Item(models.Model):
    value = models.IntegerField()

class DistinctAggregatesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Item.objects.create(value=1)
        Item.objects.create(value=1)
        Item.objects.create(value=2)

    def test_avg_distinct(self):
        result = Item.objects.aggregate(avg_distinct=Avg('value', distinct=True))
        self.assertEqual(result['avg_distinct'], 1.5)

    def test_sum_distinct(self):
        result = Item.objects.aggregate(sum_distinct=Sum('value', distinct=True))
        self.assertEqual(result['sum_distinct'], 3)

if __name__ == "__main__":
    TestCase.main()
