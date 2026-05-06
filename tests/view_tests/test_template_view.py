from django.test import TestCase
from django.urls import path
from django.views.generic import TemplateView

class TestOfferView(TemplateView):
    template_name = "dummy.html"
    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        return {"offer_slug": offer_slug}

class TemplateViewTests(TestCase):
    def setUp(self):
        self.factory = self.client_class()

    def test_template_view_with_slug(self):
        urlpatterns = [
            path('offers/<slug:offer_slug>/', TestOfferView.as_view(), name='offer_view'),
        ]
        with self.settings(ROOT_URLCONF=type('URLConf', (), {'urlpatterns': urlpatterns})):
            response = self.client.get('/offers/test-slug/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['offer_slug'], 'test-slug')

    def test_template_view_without_slug(self):
        urlpatterns = [
            path('offers/', TestOfferView.as_view(), name='offer_view'),
        ]
        with self.settings(ROOT_URLCONF=type('URLConf', (), {'urlpatterns': urlpatterns})):
            response = self.client.get('/offers/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['offer_slug'], '')
