from django.db import models
from products.models import Products
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    PAYMENT_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('cod', 'Cash on delivery payment / courier'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='CartItem')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f"{self.user.username} - Cart #{self.id}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # cijena po proizvodu
