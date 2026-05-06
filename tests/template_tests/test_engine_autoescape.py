from django.template import Engine, Template, Context
from django.test import SimpleTestCase

class EngineAutoescapeTest(SimpleTestCase):
    def test_render_to_string_honors_autoescape_with_dict(self):
        template_string = "{{ text }}"
        context_dict = {"text": "<script>alert('XSS');</script>"}
        
        engine = Engine(autoescape=False)
        template = engine.from_string(template_string)
        result = template.render(Context(context_dict))
        self.assertEqual(result, "<script>alert('XSS');</script>")
        
        engine_with_autoescape = Engine(autoescape=True)
        template_with_autoescape = engine_with_autoescape.from_string(template_string)
        result_with_autoescape = template_with_autoescape.render(Context(context_dict))
        self.assertEqual(result_with_autoescape, "&lt;script&gt;alert('XSS');&lt;/script&gt;")

    def test_render_to_string_honors_autoescape_with_context(self):
        template_string = "{{ text }}"
        context_dict = {"text": "<script>alert('XSS');</script>"}
        
        engine = Engine(autoescape=False)
        template = engine.from_string(template_string)
        context = Context(context_dict, autoescape=False)
        result = template.render(context)
        self.assertEqual(result, "<script>alert('XSS');</script>")
        
        engine_with_autoescape = Engine(autoescape=True)
        template_with_autoescape = engine_with_autoescape.from_string(template_string)
        context_with_autoescape = Context(context_dict, autoescape=True)
        result_with_autoescape = template_with_autoescape.render(context_with_autoescape)
        self.assertEqual(result_with_autoescape, "&lt;script&gt;alert('XSS');&lt;/script&gt;")

    def test_engine_autoescape_overrides_context_autoescape(self):
        template_string = "{{ text }}"
        context_dict = {"text": "<script>alert('XSS');</script>"}
        
        engine = Engine(autoescape=True)
        template = engine.from_string(template_string)
        context = Context(context_dict, autoescape=False)
        result = template.render(context)
        self.assertEqual(result, "&lt;script&gt;alert('XSS');&lt;/script&gt;")
