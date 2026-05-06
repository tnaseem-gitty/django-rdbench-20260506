from django.db import models
from django.utils.translation import gettext_lazy as _

class MyChoice(models.TextChoices):
    FIRST_CHOICE = "first", _("The first choice, it is")
    SECOND_CHOICE = "second", _("The second choice, it is")

    def __str__(self):
        return self.value

class MyObject(models.Model):
    my_str_value = models.CharField(max_length=10, choices=MyChoice.choices)
