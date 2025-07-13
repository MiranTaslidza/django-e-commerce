from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_user, name='verify'),  # url za verifikaciju
    path("update/", views.update_profile, name="update_profile"),
    path("delete/", views.delete_account, name="delete_account"),
    path('user/change_password/', views.change_password, name='change_password'),

     # url resetiranje loozinke
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='profiles/password_reset_form.html'), name='password_reset'), #url za reset lozinke
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'),name='password_reset_done'), # url za potvrdu slanja linka za reset lozinke
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'),name='password_reset_confirm'), # potvrda reset lozinke
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), name='password_reset_complete'), # potvrda reset lozinke


]