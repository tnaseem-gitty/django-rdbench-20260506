from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _

class Status(Enum):
    GOOD = _('Good')
    BAD = _('Bad')

    def __str__(self):
        return self.name

class Item(models.Model):
    status = models.CharField(max_length=128, default=Status.GOOD)

class AnotherItem(models.Model):
    status = models.CharField(max_length=128, default=Status.BAD)
