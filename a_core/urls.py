
from django.contrib import admin
from django.urls import path, include, re_path
from profiles.views import verify_user

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('products.urls')),  # Redirect root URL to admin
    path('profiles/', include('profiles.urls')),    
        # samo hook ovi za allauth OAuth
    #path('accounts/', include('allauth.socialaccount.urls')),
        # *** OVO MORA BITI UKLJUČENO ***
    
    # preusmjeri inactive na tvoj login
    path('accounts/inactive/', RedirectView.as_view(url='/profiles/login/?account_inactive')),

    re_path(r'^accounts/confirm-email/(?P<key>[-:\w]+)/$', verify_user, name='account_confirm_email'), path('accounts/', include('allauth.urls')), # ovo sam uključio
    
    
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG: # Django će servirati medijske fajlove SAMO u developmentu
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
