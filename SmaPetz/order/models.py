from pyexpat import model
from django.db import models
from products.models import Product
from profiles.models import Store
from django_countries.fields import CountryField

# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    stores = models.ManyToManyField(Store, related_name='orders')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    store_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price * self.quantity
