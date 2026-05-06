from django.db import models

class MyModel(models.Model):
    myfield = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
