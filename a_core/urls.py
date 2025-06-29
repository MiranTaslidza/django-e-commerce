
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('products.urls')),  # Redirect root URL to admin
    path('profiles/', include('profiles.urls')),    
]

if settings.DEBUG: # Django će servirati medijske fajlove SAMO u developmentu
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
