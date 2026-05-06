import os
import django
from django.db import models
from django.db.models import Q, Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

class ManagementAgent(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'main'

class PropertyGroup(models.Model):
    name = models.CharField(max_length=100)
    management_agent = models.ForeignKey(ManagementAgent, on_delete=models.CASCADE, related_name='property_groups')

    class Meta:
        app_label = 'main'

# Define a dummy management_agent for testing
management_agent = ManagementAgent.objects.create(name="Test Agent")

property_groups = PropertyGroup.objects.filter(management_agent=management_agent)
queryset = PropertyGroup.objects.annotate(Count("management_agent__property_groups"))

# This should work
queryset.filter(
    Q(management_agent__property_groups__id__in=property_groups.values_list("id", flat=True))
    | Q(management_agent__property_groups__count=0)
).distinct()

# This causes the error
queryset.filter(
    Q(management_agent__property_groups__in=property_groups)
    | Q(management_agent__property_groups__count=0)
).distinct()

print("Script completed successfully, no errors.")
