from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name="order_create"),
    path('delete_order/<int:order_id>/<int:user_id>/', delete_order, name='delete_order'),
]