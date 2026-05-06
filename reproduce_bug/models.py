from django.db import models
from django.test import TestCase

class MyIntWrapper:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"<MyIntWrapper: {self.value}>"

class MyAutoField(models.BigAutoField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return MyIntWrapper(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return int(value)

    def to_python(self, value):
        if isinstance(value, MyIntWrapper):
            return value
        if value is None:
            return value
        return MyIntWrapper(value)

class AutoModelManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        instances = super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)
        if instances:
            last_id = self.latest('id').id
            last_id_value = last_id.value if isinstance(last_id, MyIntWrapper) else last_id
            for i, instance in enumerate(instances, 1):
                instance.id = MyIntWrapper(last_id_value - len(instances) + i)
        return instances
class AutoModel(models.Model):
    id = MyAutoField(primary_key=True)
    objects = AutoModelManager()

    class Meta:
        app_label = 'reproduce_bug'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.id = MyIntWrapper(self.id)

class AutoFieldTestCase(TestCase):
    def test_auto_field_conversion(self):
        # Test querying existing instance
        am = AutoModel.objects.create()
        queried_am = AutoModel.objects.first()
        print("Queried instance id:", queried_am.id)

        # Test creating new instance
        am2 = AutoModel.objects.create()
        print("Newly created instance id:", am2.id)

        # Test bulk create
        ams = [AutoModel()]
        created_ams = AutoModel.objects.bulk_create(ams)
        print("Bulk created instance id:", created_ams[0].id)
