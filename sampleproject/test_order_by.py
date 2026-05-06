import os
import django
from django.db import models
from django.db.models import F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleproject.settings')
django.setup()
class Parent(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = [F('name').asc()]

class Child(Parent):
    age = models.IntegerField()

# Create test instances
Child.objects.create(name='Alice', age=30)
Child.objects.create(name='Bob', age=25)

# Query to trigger the ordering
children = Child.objects.all()
for child in children:
    print(child.name, child.age)

print("Script completed successfully, no errors.")
