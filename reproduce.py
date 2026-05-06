from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from .models import Photo, Report

class ReportPhotoInlineModelAdmin(admin.TabularInline):
    model = Report.photos.through
    show_change_link = True

class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportPhotoInlineModelAdmin]

admin.site.register(Report, ReportAdmin)

class TestViewPermissions(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.view_permission = Permission.objects.get(codename='view_report')
        self.user.user_permissions.add(self.view_permission)
        self.client.login(username='testuser', password='password')

    def test_view_permissions(self):
        response = self.client.get(reverse('admin:app_report_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Add another Report')
        self.assertNotContains(response, 'Delete')

print("Script completed successfully, no errors.")
