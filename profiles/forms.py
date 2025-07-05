from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# forma za registraciju korisnika
class CustomUserCreationForm(UserCreationForm):
   
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    # provjera validnosti passworda
    def clean(self):
        cleaned_data = super().clean() # poziva super clean metodu
        password = cleaned_data.get("password") # uzima password iz cleaned_data
        confirm = cleaned_data.get("password2") # uzima confirm password iz cleaned_data

        if password and confirm and password != confirm: # ako password i confirm password nisu isti
            self.add_error('password_confirm', "Passwords are not remembered..") # dodaje grešku na password_confirm polje

        return cleaned_data
    
    # provjera da li je email već registrovan
    def clean_email(self):
        email = self.cleaned_data.get('email') # provjera emaila
        if User.objects.filter(email=email).exists(): # provjera da li postoji korisnik sa tim emailom
            raise forms.ValidationError("Email is already registered..") # ako postoji, vraća grešku
        return email





