from django.db import models
import re

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.phone:
            pattern = r'^\+?\d{10,15}$|^\d{3}-\d{3}-\d{4}$'
            if not re.match(pattern, self.phone):
                raise ValueError("Invalid phone format. Use +1234567890 or 123-456-7890.")

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.price <= 0:
            raise ValueError("Price must be positive.")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new orders
            super().save(*args, **kwargs)
            self.total_amount = sum(product.price for product in self.products.all())
            super().save(update_fields=['total_amount'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"
