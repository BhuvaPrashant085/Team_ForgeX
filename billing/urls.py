from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('table/<int:table_id>/', views.billing_view, name='billing'),

    # Voice API
    path('api/parse-voice/', views.parse_voice, name='parse_voice'),

    # Bill APIs
    path('api/bill/<int:bill_id>/', views.get_bill, name='get_bill'),
    path('api/bill/<int:bill_id>/add-items/', views.add_items_to_bill, name='add_items'),
    path('api/bill/<int:bill_id>/remove-item/<int:item_id>/', views.remove_item_from_bill, name='remove_item'),
    path('api/bill/<int:bill_id>/generate/', views.generate_bill, name='generate_bill'),
    path('api/bill/<int:bill_id>/set-payment/', views.set_payment_method, name='set_payment'),

    # Menu
    path('api/menu/', views.menu_list, name='menu_list'),
    path('api/table/<int:table_id>/checkout/', views.checkout_table, name='checkout_table'),
]
