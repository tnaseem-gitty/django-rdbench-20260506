from django.db import models

class A(models.Model):
    class Meta:
        abstract = True
    myfield = models.IntegerField()

class B(A):
    pass

class C(A):
    pass

# This line is added to avoid unused model warnings
__all__ = ['B', 'C']
