from django.db import models

class Dimension(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        app_label = 'testapp'
