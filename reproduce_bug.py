import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

from django.db import connection, transaction
from django.test import TestCase
from test_app.models import Product, Order

def setup_test_database():
    connection.close()
    connection.connect()
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Product)
        schema_editor.create_model(Order)

class BugReproductionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setup_test_database()

    def test_bug_reproduction(self):
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            
            print("Bug reproduction test:")
            print(f"Order with empty product_id exists: {Order.objects.filter(product_id='').exists()}")
            print(f"Order product_id: {order.product_id}")
            print(f"Order product sku: {order.product.sku}")
            print(f"Product exists: {Product.objects.filter(sku='foo').exists()}")
            print(f"Order with correct product exists: {Order.objects.filter(product__sku='foo').exists()}")

    def test_working_scenario(self):
        with transaction.atomic():
            order = Order()
            order.product = Product(sku="foo")
            order.product.save()
            order.save()
            
            print("\nWorking scenario test:")
            print(f"Order with correct product exists: {Order.objects.filter(product=order.product).exists()}")

if __name__ == "__main__":
    test_case = BugReproductionTest()
    test_case.setUpClass()
    test_case.test_bug_reproduction()
    test_case.test_working_scenario()
    print("\nScript completed successfully.")
