from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.core.wsgi import get_wsgi_application
from django.db import models
from django.urls import re_path

# Mock Account model
# Django settings
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY="a-random-secret-key",
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'mock_app',
    ],
)
application = get_wsgi_application()

# Mock Account model
class Account(models.Model):
    slug = models.SlugField()

# Mock get_object_or_404 function
def get_object_or_404(model, slug):
    if slug == "valid-slug":
        return model(slug=slug)
    else:
        raise ValueError("Object not found")

# OfferView class
class OfferView(TemplateView):
    template_name = "offers/offer.html"
    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

# URL configuration
urlpatterns = [
    path("offers/<slug:offer_slug>/", OfferView.as_view(), name="offer_view"),
]

# Django settings
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY="a-random-secret-key",
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
    ],
)

application = get_wsgi_application()

# Test the view
def test_view():
    from django.test import RequestFactory
    factory = RequestFactory()
    request = factory.get("/offers/valid-slug/")
    response = OfferView.as_view()(request, offer_slug="valid-slug")
    print(response.context_data)

if __name__ == "__main__":
    test_view()
