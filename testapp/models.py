from django.db import models
from positions.fields import PositionField

class Thing(models.Model):
    number = models.IntegerField(default=0)
    order = PositionField()
from testapp.models import Thing
