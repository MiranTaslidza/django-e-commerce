from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError 



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



# forma za ažuriranje profila
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control text-white'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control text-white '}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control text-white'}))

    class Meta:
        model = Profile
        fields = ('profile_picture','username', 'first_name', 'last_name', 'street', 'postal_code', 'city', 'state', 'phone_number', 'birth_date')
    
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file mb-3'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-white', 'placeholder': 'YYYY-MM-DD'}),
            'street': forms.TextInput(attrs={'class': 'form-control text-white'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control text-white'}),
            'city': forms.TextInput(attrs={'class': 'form-control text-white'}),
            'state': forms.TextInput(attrs={'class': 'form-control text-white'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control text-white'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Očekujemo da nam views.py pošalje user objekat.
        super().__init__(*args, **kwargs)  # Pokrećemo osnovnu ModelForm logiku.
        #Ako user postoji, postavljamo first_name i last_name polja da već imaju vrednosti iz baze.
        if user:
            
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name  # Postavljamo početnu vrednost
            self.fields['last_name'].initial = user.last_name
            

    def save(self, commit=True):
        profile = super().save(commit=False)  # Pravimo Profile objekat, ali ga još ne snimamo u bazu.
        user = profile.user #Dohvatamo povezanog korisnika.
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']  # Uzimamo podatke iz forme i dodeljujemo ih User modelu.
        user.last_name = self.cleaned_data['last_name'] # Uzimamo podatke iz forme i dodeljujemo ih User modelu
        # Ako commit=True, prvo snimamo User, pa Profile.
        if commit:
            user.save()  # Snimamo User model
            profile.save()  # Snimamo Profile model
        return profile




# forma za promjenu email adrese
class ChangeEmailForm(forms.Form):
    # polje za unos emaila unutar forme
    new_email = forms.EmailField(
        label="New Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter new email"}),
    )

    # konstruktor init koji ser poziva kada se kreira forma
    def __init__(self, user, *args, **kwargs):
        """Prosljeđujemo korisnika da bismo mogli provjeriti emailove."""
        self.user = user
        super().__init__(*args, **kwargs)

    # validacija novog emaila
    def clean_new_email(self):
        """Provjera da li novi email već postoji u sistemu."""
        new_email = self.cleaned_data["new_email"]
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email is already in use. Please choose another.")
        return new_email

