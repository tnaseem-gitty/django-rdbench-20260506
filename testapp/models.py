from django.db import models

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

    class Meta:
        app_label = 'testapp'
