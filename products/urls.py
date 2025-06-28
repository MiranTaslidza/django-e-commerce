from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # home page prikazuje sve proizvode
    path('product/<int:pk>/' , views.productDetail, name='product_detail'), # detalji proizvoda
    path('add/', views.add_product_view, name='add_product'), # dodoavanje novog proizvoda
    path('file-upload/', views.file_upload, name='file_upload'), # uploadovanje slike
    path('updateProduct/<int:pk>/', views.updateProduct, name='updateProduct'), # update proizvoda
    path('delete-image/<int:image_id>/', views.delete_product_image, name='delete_product_image'), # brisanje slike
    path('set-main-image/', views.set_main_image, name='set_main_image'), # postavljanje glavne slike
    path('products/<int:pk>/upload-images/', views.upload_product_images, name='upload_product_images'), # dodavanje novi slika



]