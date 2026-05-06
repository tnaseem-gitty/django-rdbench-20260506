from django.core.files.storage import FileSystemStorage, default_storage
from django.db import models
import random

other_storage = FileSystemStorage(location='/media/other')

def get_storage():
    return random.choice([default_storage, other_storage])

class MyModel(models.Model):
    my_file = models.FileField(storage=get_storage)
