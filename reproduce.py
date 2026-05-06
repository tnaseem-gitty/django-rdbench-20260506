from collections import namedtuple
from django.db import models

# Define a named tuple
Range = namedtuple('Range', ['start', 'end'])

# Create a sample model
class SampleModel(models.Model):
    value = models.IntegerField()

# Create a named tuple instance
range_instance = Range(start=1, end=10)

# Attempt to use the named tuple in a queryset filter with __range
try:
    SampleModel.objects.filter(value__range=range_instance)
except TypeError as e:
    print(f"Error: {e}")
