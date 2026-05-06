from django.db import models

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.product is not None:
            self.product_id = self.product.sku
        super().save(*args, **kwargs)
