from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/<str:filterterm>/', views.product_list, name='product_list'),
    path('product_details/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('contact/', views.contact_view, name='contact'),
    path('complaint/', views.complaint_view, name='complaint'),
    path('banners/<str:banner>', views.banners, name='banners'),

    path('api/zoeken/', views.zoek_producten, name='zoek_producten'),
]
