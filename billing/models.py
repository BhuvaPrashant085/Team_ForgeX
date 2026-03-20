from django.db import models
import json


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('drink', 'Drink'),
        ('dessert', 'Dessert'),
    ]
    item_name = models.CharField(max_length=100)
    item_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name} - ₹{self.price}"

    class Meta:
        ordering = ['item_category', 'item_name']


class Table(models.Model):
    STATUS_CHOICES = [
        ('free', 'Free'),
        ('occupied', 'Occupied'),
    ]
    name = models.CharField(max_length=20)  # e.g. "Table 1"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free')

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    points = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.mobile})"


class Bill(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('online', 'Online'),
        ('card', 'Card'),
    ]
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100, default='Guest')
    items = models.JSONField(default=list)   # list of {item_id, name, qty, price, subtotal}
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    GST_RATE = 0.05

    def calculate_totals(self):
        self.subtotal = sum(i['subtotal'] for i in self.items)
        self.gst_amount = round(float(self.subtotal) * self.GST_RATE, 2)
        self.total = round(float(self.subtotal) + self.gst_amount, 2)

    def __str__(self):
        return f"Bill #{self.id} - {self.table} - ₹{self.total}"


class Staff(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('captain', 'Captain'),
        ('cashier', 'Cashier'),
    ]
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    mail = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    password = models.CharField(max_length=4, unique=True)  # 4-digit auto-generated
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
