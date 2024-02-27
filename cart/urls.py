from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name="cart_detail"),
    path('add/<int:product_id>', cart_add_net_quantity, name="cart_add_net_quantity"),
    path('add_quantity/<int:product_id>', cart_add, name="cart_add"),
    path('remove/<int:product_id>', cart_remove, name="cart_remove"),
    path('update_quantity/<int:product_id>/', update_quantity, name='update_quantity'),
]