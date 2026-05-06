from django.db import models

class Outer(object):
    class Inner(models.CharField):
        pass

class A(models.Model):
    field = Outer.Inner(max_length=20)

print("Model classes defined.")
print("Now you need to run 'python manage.py makemigrations' to see the issue.")
