import os
import sys
import django
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.http import HttpResponseRedirect, Http404
from django.urls import path, reverse
from io import StringIO

# Set up Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
django.setup()

# Create a dummy URL configuration
def dummy_view(request):
    return HttpResponseRedirect('/')

urlpatterns = [
    path('admin/', dummy_view, name='admin:index'),
]

# Configure settings
settings.ROOT_URLCONF = __name__
settings.FORCE_SCRIPT_NAME = '/script_name'

def test_catch_all_view():
    site = AdminSite()
    factory = RequestFactory()
    
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Test with FORCE_SCRIPT_NAME
        request = factory.get('/admin/')
        request.path = '/script_name/admin/'
        
        print(f"Testing with path: {request.path}")
        
        try:
            response = site.catch_all_view(request, '')
            if isinstance(response, HttpResponseRedirect):
                print(f"Redirected to: {response.url}")
                assert response.url == '/script_name/admin/', f"Expected '/script_name/admin/', got {response.url}"
                print("Test passed successfully!")
            else:
                print(f"Unexpected response type: {type(response)}")
        except Http404:
            print("Http404 exception raised unexpectedly for valid URL.")
        except Exception as e:
            print(f"Unexpected exception: {str(e)}")

        # Test Http404 for non-existent URL
        request = factory.get('/admin/unknown')
        request.path = '/script_name/admin/unknown'
        
        print(f"\nTesting with path: {request.path}")
        
        try:
            site.catch_all_view(request, 'unknown')
            print("Unexpected: No exception raised for non-existent URL.")
        except Http404:
            print("Http404 exception raised as expected for non-existent URL.")
        except Exception as e:
            print(f"Unexpected exception: {str(e)}")

        # Test with FORCE_SCRIPT_NAME and a URL that should be appended with a slash
        request = factory.get('/admin')
        request.path = '/script_name/admin'
        
        print(f"\nTesting with path that should be appended with slash: {request.path}")
        
        try:
            response = site.catch_all_view(request, '')
            if isinstance(response, HttpResponseRedirect):
                print(f"Redirected to: {response.url}")
                assert response.url == '/script_name/admin/', f"Expected '/script_name/admin/', got {response.url}"
                print("Test passed successfully!")
            else:
                print(f"Unexpected response type: {type(response)}")
        except Http404:
            print("Http404 exception raised unexpectedly for valid URL that should be appended with slash.")
        except Exception as e:
            print(f"Unexpected exception: {str(e)}")

    finally:
        # Restore stdout and print captured output
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        print(output)

if __name__ == '__main__':
    test_catch_all_view()
