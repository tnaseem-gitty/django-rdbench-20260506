from django.db import models

class SelfRef(models.Model):
    name = models.CharField(max_length=100)
    c8 = models.CharField(max_length=100)
