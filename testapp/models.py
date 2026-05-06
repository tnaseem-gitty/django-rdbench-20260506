from django.db import models

class Thing(models.Model):
    pass

class Related(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
