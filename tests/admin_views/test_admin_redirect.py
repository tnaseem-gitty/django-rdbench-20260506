from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from django.http import HttpResponsePermanentRedirect
from unittest.mock import patch
from django.urls import ResolverMatch

class AdminRedirectTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()

    @patch('django.contrib.admin.sites.resolve')
    def test_catch_all_view_preserves_query_string(self, mock_resolve):
        mock_resolve.return_value = ResolverMatch(lambda: None, (), {})
        request = self.factory.get('/admin/auth/user?q=test')
        response = self.site.catch_all_view(request, 'auth/user')
        self.assertIsInstance(response, HttpResponsePermanentRedirect)
        self.assertEqual(response.url, '/admin/auth/user/?q=test')
