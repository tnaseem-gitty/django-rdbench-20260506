from django.template import Library

register = Library()

# Import and register the template tags
from .test_template_tags import hello, hi

register.simple_tag(hello)
register.inclusion_tag('dummy.html')(hi)
