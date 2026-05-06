from django.db import models

class Publication(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'test_app'

class Article(models.Model):
    title = models.CharField(max_length=100)
    publications = models.ManyToManyField(to=Publication, blank=True)

    class Meta:
        app_label = 'test_app'
