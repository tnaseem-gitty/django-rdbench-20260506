from django.db import models

# Mock Account model
class Account(models.Model):
    slug = models.SlugField()

    class Meta:
        app_label = 'mock_app'

# Mock get_object_or_404 function
def get_object_or_404(model, slug):
    if slug == "valid-slug":
        return model(slug=slug)
    else:
        raise ValueError("Object not found")
