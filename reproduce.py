import django
from django.conf import settings
from django.db import models, transaction
print("Script started")
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'myapp',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

django.setup()

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

    class Meta:
        app_label = 'myapp'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        app_label = 'myapp'

# Create tables
from django.core.management import call_command
call_command('makemigrations', 'myapp')
call_command('migrate', run_syncdb=True)

# Reproduce the issue
with transaction.atomic():
    order = Order()
    order.product = Product()
    order.product.sku = "foo"
    order.product.save()
    print(f"Product saved with SKU: {order.product.sku}")
    assert Order.objects.filter(product_id="").exists()  # Succeeds, but shouldn't
    assert Order.objects.filter(product=order.product).exists()  # Fails

print("Script completed successfully, no errors.")
