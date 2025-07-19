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
    path('<int:pk>/', views.get_profile, name='profile'),

    # url resetiranje loozinke 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='profiles/password_reset_form.html', html_email_template_name='profiles/password_reset_email.html'), name='password_reset'), # url za slanje e-maila za reset lozuinke
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'),name='password_reset_done'), # poruka korisniku da je poslat mail za reset lozinke
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'),name='password_reset_confirm'), # forma za postavljanje nove lozinke
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), name='password_reset_complete'), # poruka korisniku da je promjenjena lozinka


    # promjena emaila
    path('user/change_email/', views.change_email, name='change_email'), # promjena emaila
    path('confirm_old_email/<str:token>/', views.confirm_old_email, name='confirm_email_change'), # potvrda sa starog emaila
    path('cancel-email/<str:token>/', views.cancel_email_change, name='cancel_email_change'), # otkazivanje promjene emaila
    path('confirm_new_email/<str:token>/', views.confirm_new_email, name='confirm_new_email'),  # potvrda novog emaila

]