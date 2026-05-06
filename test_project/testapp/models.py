from django.db import models

class Item(models.Model):
    uid = models.AutoField(primary_key=True, editable=False)
    f = models.BooleanField(default=False)

    def reset(self):
        self.pk = None
        self.f = False

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.f = True
        super().save(*args, **kwargs)

class Derived(Item):
    pass
