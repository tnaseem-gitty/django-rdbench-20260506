
from django.db import models

class OurModel(models.Model):
    our_field = models.JSONField()
