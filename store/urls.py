from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),

]
