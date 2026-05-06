from django.conf import settings
from django.http import HttpRequest
from django.contrib.admin.sites import AdminSite

# Configure settings
settings.configure(
    APPEND_SLASH=True,
    ROOT_URLCONF=__name__,
)

from django.urls import path, re_path
from django.http import HttpResponse

# Minimal URL configuration
urlpatterns = [
    re_path(r'^admin/auth/foo/$', lambda request: HttpResponse("OK")),
]

# Create a mock request with a query string
request = HttpRequest()
request.path = "/admin/auth/foo"
request.path_info = request.path

print(f"Request path: {request.path}")
print(f"Request path info: {request.path_info}")
admin_site = AdminSite()
response = admin_site.catch_all_view(request, "auth/foo")

# Print the location header to verify the redirect
print(response['Location'])
