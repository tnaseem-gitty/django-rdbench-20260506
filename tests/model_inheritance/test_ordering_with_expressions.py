from django.db import models
from django.test import TestCase
from django.db.models import F

class OrderingParent(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()

    class Meta:
        ordering = [F('value').desc()]
        app_label = 'model_inheritance'

class OrderingChild(OrderingParent):
    extra = models.CharField(max_length=50)

    class Meta:
        app_label = 'model_inheritance'

class OrderingWithExpressionsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        OrderingParent.objects.create(name='Parent 1', value=10)
        OrderingParent.objects.create(name='Parent 2', value=20)
        OrderingChild.objects.create(name='Child 1', value=15, extra='Extra 1')
        OrderingChild.objects.create(name='Child 2', value=25, extra='Extra 2')

    def test_ordering_with_expressions(self):
        # Test ordering of OrderingParent objects (including child objects due to multi-table inheritance)
        parents = OrderingParent.objects.all()
        self.assertEqual(list(parents.values_list('name', flat=True)), ['Child 2', 'Parent 2', 'Child 1', 'Parent 1'])

        # Test ordering of OrderingChild objects
        children = OrderingChild.objects.all()
        self.assertEqual(list(children.values_list('name', flat=True)), ['Child 2', 'Child 1'])

        # Test ordering of only OrderingParent objects (excluding child objects)
        parent_only = OrderingParent.objects.filter(orderingchild__isnull=True)
        self.assertEqual(list(parent_only.values_list('name', flat=True)), ['Parent 2', 'Parent 1'])
