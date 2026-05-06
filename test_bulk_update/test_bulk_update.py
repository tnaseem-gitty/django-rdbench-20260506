from django.db import models, connection
from django.test import TestCase

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

class BulkUpdateTest(TestCase):
    def setUp(self):
        MyModel.objects.create(name='obj1', value=1)
        MyModel.objects.create(name='obj2', value=2)
        MyModel.objects.create(name='obj3', value=3)

    def test_bulk_update(self):
        objs = list(MyModel.objects.all())
        for obj in objs:
            obj.value += 10
        rows_updated = MyModel.objects.bulk_update(objs, ['value'])
        self.assertEqual(rows_updated, 3)
        for obj in objs:
            obj.refresh_from_db()
            self.assertTrue(obj.value > 3)

if __name__ == "__main__":
    import django
    django.setup()
    TestCase.main()
