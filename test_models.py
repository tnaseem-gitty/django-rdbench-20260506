from django.db import models

class TestImageFieldModel(models.Model):
    class Meta:
        app_label = 'test_app'

class TestModelNoDimensions(TestImageFieldModel):
    image = models.ImageField(upload_to='test_images/')

class TestModelWithDimensions(TestImageFieldModel):
    image = models.ImageField(upload_to='test_images/', width_field='width', height_field='height')
    width = models.IntegerField()
    height = models.IntegerField()
