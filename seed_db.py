from django.core.management.base import BaseCommand
from crm.models import Customer, Product

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        customers = [
            {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
            {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
        ]
        for c in customers:
            Customer.objects.get_or_create(**c)

        products = [
            {"name": "Laptop", "price": 999.99, "stock": 10},
            {"name": "Phone", "price": 499.99, "stock": 20},
        ]
        for p in products:
            Product.objects.get_or_create(**p)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
