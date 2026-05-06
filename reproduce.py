import django
from django.conf import settings

# Setup Django
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

from django.db.models import Case, When, Value, BooleanField, Q
from django.contrib.auth.models import User

# Reproducing the issue
users = User.objects.annotate(
    _a=Case(
        When(~Q(pk__in=[]), then=Value(True)),
        default=Value(False),
        output_field=BooleanField(),
    )
).order_by("-_a").values("pk")

print(list(users))
