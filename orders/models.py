from django.db import models
from app.models import Course

# Create your models here.
class Order(models.Model):
    choices = (
        ('unfullfilled', 'Unfullfilled'),
        ('ready to pickup', 'READY TO PICKUP'),
        ('canceled', 'CANCELED'),
        ('shipped', 'SHIPPED'),
        ('partially fulfilled', 'PARTIALLY FULFILLED'),
        ('fullfilled', 'Fullfilled'),
    )
    
    deliver = (
        ('standart shipping', 'Standard shipping'),
        ('local pickup', 'Local pickup'),
        ('local delivery', 'Local delivery'),
        ('free shipping', 'Free shipping'),
        ('cash on delivery', 'Cash on delivery'),
        ('express', 'Express'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=22)
    status = models.CharField(choices=choices, default="unfullfilled", max_length=20)
    city = models.CharField(max_length=101)
    delivery = models.CharField(choices=deliver, max_length=20, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self) -> str:
        return f'Order {self.id}'
    
    @classmethod
    def get_total_all_orders(cls):
        # Barcha buyurtmalarni qaytaradi
        all_orders = cls.objects.all()

        # Barcha buyurtmalarning umumiy to'lamini hisoblash
        total_cost_all_orders = sum(order.get_total_cost() for order in all_orders)

        return total_cost_all_orders
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity