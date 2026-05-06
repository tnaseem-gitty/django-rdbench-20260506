import os
import django
from django.conf import settings

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
django.setup()

from django.template import Template, Context, Library
from django.test import TestCase

register = Library()

@register.simple_tag
def hello(*, greeting='hello'):
    return f'{greeting} world'

@register.inclusion_tag('dummy.html')
def hi(*, greeting):
    return {'greeting': greeting}

# Register the template library
from django.template import engines
engines['django'].engine.template_libraries['test_template_tags'] = register

class TemplateTagTests(TestCase):
    def test_simple_tag_with_keyword_only_arg(self):
        t = Template("{% load test_template_tags %}{% hello greeting='hi' %}")
        c = Context({})
        self.assertEqual(t.render(c), 'hi world')

    def test_simple_tag_with_default_keyword_only_arg(self):
        t = Template("{% load test_template_tags %}{% hello %}")
        c = Context({})
        self.assertEqual(t.render(c), 'hello world')

    def test_inclusion_tag_with_keyword_only_arg(self):
        t = Template("{% load test_template_tags %}{% hi greeting='hello' %}")
        c = Context({})
        self.assertEqual(t.render(c).strip(), 'hello')  # Assuming 'dummy.html' just outputs {{ greeting }}

    def test_multiple_keyword_args(self):
        with self.assertRaises(Exception):  # Should raise TemplateSyntaxError
            Template("{% load test_template_tags %}{% hello greeting='hi' greeting='hello' %}")

if __name__ == '__main__':
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(['tests.test_template_tags'])
    if failures:
        print("Tests failed. Please check the output above.")
    else:
        print("All tests passed successfully!")
