from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    
    def __str__(self):
        return self.Item_name
    
    Item_name = models.CharField(max_length=200)
    Item_desc = models.TextField(max_length=500)
    Item_price = models.IntegerField()
    Item_img = models.CharField(max_length=1100, default="https://cdn-icons-png.flaticon.com/512/1377/1377194.png")

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.Item_name}"
    
    @property
    def total_price(self):
        return self.quantity * self.item.Item_price

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.Item_name} in Order {self.order.id}"
