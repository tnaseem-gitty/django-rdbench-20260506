from django.template.defaultfilters import escapeseq
from django.test import SimpleTestCase
from django.utils.safestring import mark_safe

class EscapeseqTests(SimpleTestCase):
    def test_escapeseq(self):
        items = ['<p>Hello</p>', 'World & "Django"', mark_safe('<b>Safe</b>')]
        self.assertEqual(
            escapeseq(items),
            ['&lt;p&gt;Hello&lt;/p&gt;', 'World &amp; &quot;Django&quot;', '<b>Safe</b>']
        )

    def test_escapeseq_with_join(self):
        items = ['<p>Hello</p>', 'World & "Django"', mark_safe('<b>Safe</b>')]
        escaped_items = escapeseq(items)
        self.assertEqual(
            ','.join(escaped_items),
            '&lt;p&gt;Hello&lt;/p&gt;,World &amp; &quot;Django&quot;,<b>Safe</b>'
        )

    def test_escapeseq_non_string(self):
        items = [1, 2, '<p>3</p>']
        self.assertEqual(
            escapeseq(items),
            ['1', '2', '&lt;p&gt;3&lt;/p&gt;']
        )
