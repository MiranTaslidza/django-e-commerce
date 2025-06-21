from django.shortcuts import render
from .models import Products, Category, SubCategory, ProductImage

from .forms import ProductForm
from django.shortcuts import redirect



def home(request):
    products = Products.objects.filter(is_active=True)
    return render(request, 'products/index.html', {'products': products})

# dodavanje novog proizvoda
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # ili neka druga stranica
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})
