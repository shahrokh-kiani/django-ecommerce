# cart/models.py
from django.db import models
from shop.models import Product
from accounts.models import Customer

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_subtotal(self):
        price = self.product.on_sale_price if self.product.on_sale else self.product.price
        return price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"