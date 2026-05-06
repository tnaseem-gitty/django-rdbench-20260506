from django.db import models

class Outer(object):
    class Inner(models.CharField):
        def __init__(self, *args, **kwargs):
            kwargs['max_length'] = 20
            super().__init__(*args, **kwargs)

class A(models.Model):
    field = Outer.Inner()

print('Model classes defined.')
print('Now you need to run \'python manage.py makemigrations\' to see the issue.')
