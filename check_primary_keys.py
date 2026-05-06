import django
from django.apps import apps
from django.conf import settings

# Initialize Django
settings.configure()
django.setup()

# List of models to check
model_names = [
    'accounts.ReservedUsername',
    'accounts.User',
    'blocks.Block',
    'contact_by_form.Feedback',
    'core_messages.ReadMark',
    'friendship.Block',
    'friendship.Follow',
    'friendship.Friend',
    'friendship.FriendshipRequest',
    'likes.UserLike',
    'uploads.Image',
]

# Check primary key type for each model
for model_name in model_names:
    try:
        model = apps.get_model(model_name)
        pk_field = model._meta.pk
        print(f'{model_name}: {type(pk_field).__name__}')
    except LookupError:
        print(f'{model_name}: Model not found')
