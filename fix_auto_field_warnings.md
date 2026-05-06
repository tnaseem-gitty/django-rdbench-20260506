# Fixing Auto-created Primary Key Warnings in Django 3.2+

To resolve the warnings about auto-created primary keys in Django 3.2 and later versions, follow these steps for each of your custom apps:

1. Locate the `apps.py` file in your app directory. If it doesn't exist, create one.

2. In the `apps.py` file, define or update the `AppConfig` class for your app. Add the `default_auto_field` attribute set to `'django.db.models.BigAutoField'`.

Here's an example of how your `apps.py` file should look:

```python
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'
```

3. Repeat this process for all of your custom apps mentioned in the warning messages (blocks, contact_by_form, core_messages, friendship, likes, uploads, etc.).

4. If you prefer to set this globally for all apps in your project, you can add the following to your project's `settings.py` file:

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

5. After making these changes, run your migrations again:

```
python manage.py makemigrations
python manage.py migrate
```

This should resolve the warnings about auto-created primary keys.

Note: If you're working with an existing database, changing the primary key field type might require careful migration planning. Always backup your database before applying such changes to a production system.
