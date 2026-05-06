from django.test import SimpleTestCase
from django.utils.formats import get_format
from django.utils.translation import gettext_lazy as _

class GetFormatTests(SimpleTestCase):
    def test_get_format_with_lazy_string(self):
        lazy_format = _('DATE_FORMAT')
        try:
            result = get_format(lazy_format)
        except TypeError:
            self.fail("get_format raised TypeError with lazy string")
        self.assertIsNotNone(result)

# Remove the if __name__ == '__main__': block as it's not needed for Django tests
