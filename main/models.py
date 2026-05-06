from django.db import models

class Person(models.Model):
    friends = models.ManyToManyField('self')

    class Meta:
        app_label = 'main'

class User(models.Model):
    pass

    class Meta:
        app_label = 'main'

class Entry(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_entries')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_entries')

    class Meta:
        app_label = 'main'
