from django.db import models

class Dimension(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.name
