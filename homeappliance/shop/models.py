from django.db import models

from accounts.models import Customer

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    picture = models.ImageField(upload_to='upload/product/', blank=True)  

    on_sale = models.BooleanField(default=False)
    on_sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)


    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    address = models.CharField(max_length=200, default='', blank=False)
    province = models.CharField(max_length=35, default='', blank=False)
    city = models.CharField(max_length=30, default='', blank=False)
    postal_code = models.CharField(max_length=11, default='', blank=False)
    phone = models.CharField(max_length=15, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"سفارش #{self.id} - {self.customer}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    def get_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    score = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'customer')

    def __str__(self):
        return f"{self.customer} - {self.product} - {self.score}"