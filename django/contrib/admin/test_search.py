from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin as ClientAdmin
from myapp.models import Client, ClientOffice  # Replace 'myapp' with the actual app name

class ClientAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.client_admin = ClientAdmin(Client, self.site)
        self.client1 = Client.objects.create(name="Client One", name2="Client 1", contact_person="Person A")
        self.client2 = Client.objects.create(name="Client Two", name2="Client 2", contact_person="Person B")
        self.office1 = ClientOffice.objects.create(name="Office One", name2="Office 1", client=self.client1)
        self.office2 = ClientOffice.objects.create(name="Office Two", name2="Office 2", client=self.client2)

    def test_search(self):
        request = None  # Mock request object
        queryset = Client.objects.all()
        search_term = "Client Office"
        queryset, may_have_duplicates = self.client_admin.get_search_results(request, queryset, search_term)
        self.assertEqual(queryset.count(), 2)
        print("Test completed successfully, no errors.")

if __name__ == "__main__":
    import django
    django.setup()
    TestCase.run()
