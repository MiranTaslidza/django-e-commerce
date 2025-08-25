from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from products.models import Products

class Cart(models.Model):
    # Opcije plaćanja
    PAYMENT_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('COD', 'Cash on Delivery'),
    ]

    # Status korpe
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ORDERED', 'Ordered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart #{self.id} ({self.user.username})"

    # Ukupan broj proizvoda u korpi
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    # Ukupna cijena korpe
    @property
    def total_price(self):
        total = sum(item.total_price for item in self.items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot cijene pri dodavanju
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    # Ukupna cijena stavke
    @property
    def total_price(self):
        return self.price * self.quantity
