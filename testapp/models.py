from django.db import models

class Dimension(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()
