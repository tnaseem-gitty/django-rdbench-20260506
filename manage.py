import os
import django
from django.db import models
from django.db.models import Q, Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

class ManagementAgent(models.Model):
    name = models.CharField(max_length=100)

class PropertyGroup(models.Model):
    name = models.CharField(max_length=100)
    management_agent = models.ForeignKey(ManagementAgent, on_delete=models.CASCADE, related_name='property_groups')

