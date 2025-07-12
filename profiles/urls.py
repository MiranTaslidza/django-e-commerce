from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_user, name='verify'),  # url za verifikaciju
    path("update/", views.update_profile, name="update_profile"),
]