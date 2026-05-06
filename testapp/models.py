from django.db import models

class OneModel(models.Model):
    class Meta:
        ordering = ("-id",)
    id = models.BigAutoField(primary_key=True)
    root = models.ForeignKey("OneModel", on_delete=models.CASCADE, null=True)
    oneval = models.BigIntegerField(null=True)
class TwoModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    record = models.ForeignKey(OneModel, on_delete=models.CASCADE)
    twoval = models.BigIntegerField(null=True)
