from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, null=True, blank=True)  # Changed to EmailField

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField( null=True, blank=True)  # Added image field
    discount = models.FloatField(default=0.0)
    discount_price = models.FloatField(null=True, blank=True)
    sales = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)  # Changed to snake_case
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=128, null=True, blank=True)  # Added blank=True

    def __str__(self):
        return str(self.id)
    
 
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items (self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)  # Changed to snake_case

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    # def __str__(self):
    #     return f'{self.product} - {self.quantity}'

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=128)  # Corrected typo
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zipcode = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)  # Changed to snake_case
    
    def __str__(self):
        return self.address
    from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

