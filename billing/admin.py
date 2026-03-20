from django.contrib import admin
from .models import MenuItem, Table, Customer, Bill


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'item_category', 'price', 'is_available']
    list_filter = ['item_category', 'is_available']
    search_fields = ['item_name']
    list_editable = ['price', 'is_available']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    list_editable = ['status']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'points', 'visit_count', 'created_at']
    search_fields = ['name', 'mobile']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'customer_name', 'total', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    readonly_fields = ['subtotal', 'gst_amount', 'total', 'created_at']
