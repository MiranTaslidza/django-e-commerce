from django.shortcuts import render
from .models import Products, Category, SubCategory, ProductImage


def home(request):
    products = Products.objects.filter(is_active=True)
    return render(request, 'products/index.html', {'products': products})

