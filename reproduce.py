from django.db import models
from django.db.models import F
from django.db.models.functions import Lag
from django.db.models import Window
from django.core.management import execute_from_command_line

class LagTest(models.Model):
    modified = models.DateField()
    data = models.FloatField()
    amount = models.DecimalField(decimal_places=4, max_digits=7)

def run():
    w = Window(expression=Lag('amount', 7), partition_by=[F('modified')], order_by=F('modified').asc())
    q = LagTest.objects.all().annotate(w=w)
    print(q)

if __name__ == "__main__":
    execute_from_command_line(['manage.py', 'migrate'])
    run()
