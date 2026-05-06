import django
from django.conf import settings
from django import template
from django.template import Context, Template

# Minimal settings configuration
settings.configure(
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
    ]
)

django.setup()

register = template.Library()

@register.simple_tag
def hello(*, greeting='hello'):
    return f'{greeting} world'

@register.simple_tag
def hi(*, greeting):
    return f'{greeting} world'

# Register the custom tags
template.engines['django'].engine.template_libraries['custom_tags'] = register

# Simulate template rendering
template_string = """
{% load custom_tags %}
{% hello greeting='hi' %}
{% hi greeting='hi' greeting='hello' %}
"""

t = Template(template_string)
c = Context({})

try:
    print(t.render(c))
except template.TemplateSyntaxError as e:
    print(f"Error: {e}")
