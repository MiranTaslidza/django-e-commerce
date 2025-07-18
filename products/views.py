from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Products, Category, SubCategory, ProductImage
from .forms import ProductForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import os

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

# update proizvoda
def updateProduct(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST': 
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/updateProduct.html', {'form': form, 'product': product})

# dodavanje glavne slike
@require_POST
@csrf_exempt  # ili dodaj CSRF token u JS request
def set_main_image(request):
    image_id = request.POST.get('image_id')
    if not image_id:
        return JsonResponse({'success': False, 'error': 'No image ID provided.'})

    from products.models import ProductImage

    try:
        image = ProductImage.objects.get(id=image_id)
        product = image.product
        # Resetuj sve slike na is_main=False
        product.images.update(is_main=False)
        # Postavi odabranu sliku kao glavnu
        image.is_main = True
        image.save()
        return JsonResponse({'success': True})
    except ProductImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image not found.'})

#brisanje slika
def delete_product_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id  # da se možemo vratiti na update formu

    # Brisanje fajla sa diska
    if image.image:
        image_path = image.image.path  # puna putanja do fajla
        if os.path.isfile(image_path):
            os.remove(image_path)

    # Brisanje iz baze
    image.delete()

    return redirect('updateProduct', pk=product_id)

# dodavanje slika
@csrf_exempt
def upload_product_images(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=pk)
        images = request.FILES.getlist('images')
        image_data = []

        for img in images:
            new_image = ProductImage.objects.create(product=product, image=img)
            image_data.append({
                'id': new_image.id,
                'url': new_image.image.url
            })

        return JsonResponse({'images': image_data})

# dodavanje dropdown slika
@csrf_protect
def file_upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file') # dodajem sliku

        # uslov ukolio korisnik nije prijavljen
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You must be logged in..'}, status=401)
        
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

    return JsonResponse({'error': 'Only POST request is allowed.'}, status=400)


# brisanje proizvoda
def delete_product(request, pk):
    product = get_object_or_404(Products, pk=pk)

    # Obriši slike sa diska
    for image in product.images.all():
        if image.image:
            image_path = image.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)

    # Obriši proizvod (ovo će obrisati i povezane slike u bazi ako imaš ForeignKey sa on_delete=CASCADE)
    product.delete()

    return redirect('home')