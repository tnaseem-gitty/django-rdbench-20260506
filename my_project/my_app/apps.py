from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app'
# myapp global initial_demo ...
with open("manage.py", mode="r") as stream:
    print("=== %s" % stream.encoding)
