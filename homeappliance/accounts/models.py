from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    province = models.CharField(max_length=35, blank=True)
    city = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.user.username