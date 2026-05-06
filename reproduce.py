import django
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    SECRET_KEY='dummy'
)

django.setup()

class FooBar(models.Model):
    foo_bar = models.CharField(_("foo"), choices=[(1, 'foo'), (2, 'bar')])

    class Meta:
        app_label = 'myapp'
    def __str__(self):
        return self.get_foo_bar_display()  # This returns 'foo' or 'bar' in 2.2, but 'something' in 2.1

    def get_foo_bar_display(self):
        return "something"

# Create an instance and print the display value
foobar = FooBar(foo_bar=1)
print(foobar.get_foo_bar_display())
print(str(foobar))
