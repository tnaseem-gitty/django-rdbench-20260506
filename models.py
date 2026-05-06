from django.db import models

class Thing(models.Model):
    class Meta:
        app_label = '__main__'

class Related(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

    class Meta:
        app_label = '__main__'
