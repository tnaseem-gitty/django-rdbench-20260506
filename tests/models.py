from django.db import models

class OneModel(models.Model):
    class Meta:
        ordering = ("-id",)
    root = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    oneval = models.BigIntegerField(null=True)

class TwoModel(models.Model):
    record = models.ForeignKey(OneModel, on_delete=models.CASCADE)
    twoval = models.BigIntegerField(null=True)
