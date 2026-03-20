from django.core.management.base import BaseCommand
from billing.models import MenuItem, Table


class Command(BaseCommand):
    help = 'Seed initial menu items and tables'

    def handle(self, *args, **kwargs):
        # Create 10 tables
        for i in range(1, 11):
            Table.objects.get_or_create(name=f'Table {i}')
        self.stdout.write(self.style.SUCCESS('Created 10 tables'))

        # Seed menu
        menu_data = [
            # Starters
            ('Samosa', 'starter', 20),
            ('Spring Roll', 'starter', 60),
            ('Paneer Tikka', 'starter', 180),
            # Main Course
            ('Cheese Pizza', 'main', 300),
            ('Veg Burger', 'main', 120),
            ('Paneer Butter Masala', 'main', 200),
            ('Dal Tadka', 'main', 150),
            ('Veg Fried Rice', 'main', 160),
            ('French Fries', 'main', 80),
            # Drinks
            ('Coke', 'drink', 60),
            ('Lassi', 'drink', 70),
            ('Chai', 'drink', 30),
            ('Cold Coffee', 'drink', 90),
            ('Fresh Lime Soda', 'drink', 50),
            # Desserts
            ('Gulab Jamun', 'dessert', 80),
            ('Ice Cream', 'dessert', 100),
        ]
        for name, cat, price in menu_data:
            MenuItem.objects.get_or_create(
                item_name=name,
                defaults={'item_category': cat, 'price': price}
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(menu_data)} menu items'))
