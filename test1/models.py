from django.db import models

class Outer(object):
    class Inner(models.CharField):
        pass

class A(models.Model):
    field = Outer.Inner(max_length=20)
import enum
from enumfields import Enum, EnumField

class Thing(models.Model):
    @enum.unique
    class State(Enum):
        on = 'on'
        off = 'off'
    state = EnumField(enum=State)
# Remove the import statement causing the circular import issue
