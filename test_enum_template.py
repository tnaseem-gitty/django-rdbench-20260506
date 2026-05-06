import os
import django
from django.conf import settings
from django.template import Context, Template
from django.db import models

# Define a simple Django settings configuration
settings.configure(
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
    ],
)

# Initialize Django
django.setup()

# Define an enumeration type
class YearInSchool(models.TextChoices):
    FRESHMAN = 'FR', 'Freshman'
    SOPHOMORE = 'SO', 'Sophomore'
    JUNIOR = 'JR', 'Junior'
    SENIOR = 'SR', 'Senior'

# Create a template that uses the enumeration type
template_string = """
{% load static %}
{% if student.year_in_school == YearInSchool.FRESHMAN %}
    Freshman
{% elif student.year_in_school == YearInSchool.SOPHOMORE %}
    Sophomore
{% elif student.year_in_school == YearInSchool.JUNIOR %}
    Junior
{% elif student.year_in_school == YearInSchool.SENIOR %}
    Senior
{% else %}
    Unknown
{% endif %}
"""

# Create a context with a student object
context = Context({
    'student': {'year_in_school': YearInSchool.FRESHMAN},
    'YearInSchool': YearInSchool,
})

# Render the template
template = Template(template_string)
output = template.render(context)
print(output)
# class IntegerChoices(int, Choices):
#     """Class for creating enumerated integer choices."""
#     do_not_call_in_templates = True
#     pass
