from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # home page prikazuje sve proizvode
    path('add/', views.add_product_view, name='add_product'), # dodoavanje novog proizvoda
    path('file-upload/', views.file_upload, name='file_upload'), # uploadovanje slike
    path('product/<int:pk>/' , views.productDetail, name='product_detail'), # detalji proizvoda

]