from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]
ROOT_URLCONF = 'test_urls'
