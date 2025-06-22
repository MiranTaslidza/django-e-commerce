from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Products, Category, SubCategory, ProductImage
from .forms import ProductForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

# PRIKAZ SVIH PROIZVODA
def home(request):
    products = Products.objects.filter(is_active=True)
    return render(request, 'products/index.html', {'products': products})

# dodavanje novog proizvoda
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # sačuvaj proizvod i dohvati instancu
            # ažuriraj slike koje nemaju proizvod, a postavio ih je ovaj korisnik
            ProductImage.objects.filter(user=request.user, product__isnull=True).update(product=product)
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

# prikaz detalja proizvoda
def productDetail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    return render(request, 'products/productDetail.html', {'product': product})
   


# dodavanje dropdown slika
@csrf_protect
def file_upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file') # dodajem sliku

        # uslov ukolio korisnik nije prijavljen
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Morate biti prijavljeni.'}, status=401)
        
        #postavlja priijavljenog korisnika
        user = request.user

        # dodaj sliku u bazu
        image = ProductImage.objects.create(
            image=file,
            user = user,
            product=None
        )

        return JsonResponse({
            'message': 'Uspješno!',
            'image_url': image.image.url,
            'image_id': image.id
        })

    return JsonResponse({'error': 'Dozvoljen je samo POST zahtjev.'}, status=400)


