from django.db import models

class TestModelNoDimensions(models.Model):
    image = models.ImageField(upload_to='test_images/')

class TestModelWithDimensions(models.Model):
    image = models.ImageField(upload_to='test_images/', width_field='width', height_field='height')
    width = models.IntegerField()
    height = models.IntegerField()
