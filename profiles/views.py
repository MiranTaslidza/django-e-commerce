from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,  ProfileUpdateForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from .models import Profile
from django.contrib.auth.decorators import login_required

#login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # koristi Django login
            return redirect('home')
        else:
            # možeš dodati poruku da su loši podaci
            pass
    return render(request, 'profiles/login.html')


#logout
def logout_view(request):
    logout(request)
    return redirect('login')


# registracija korisnika
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

           # Čuvanje podataka u sesiji pre nego što se korisnik registruje
            request.session['registration_data'] = form.cleaned_data
            email = form.cleaned_data.get('email')  

            # Generišemo token i UID za verifikaciju
            user = User(username=form.cleaned_data.get('username'), email=email)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  # Korisnik je neaktivan dok ne potvrdi e-mail
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Kreiraj verifikacioni link
            current_site = get_current_site(request)
            domain = current_site.domain
            link = f"http://{domain}/profiles/verify/{uid}/{token}/" # ukoliko koristim unutar glavnog url profiles url link = f"http://{domain}/profiles/verify/{uid}/{token}/"

            # Pošalji e-mail s verifikacionim linkom
            subject = "Verify your email"
            html_message = render_to_string('profiles/activation_email.html', {
                'user': user,
                'link': link,
            })
            send_email_notification(subject, html_message, [email])  # Koristimo funkciju za slanje e-maila

            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "profiles/register.html", {"form": form})




# kontroiler koji šalje mail korisniku
from django.core.mail import EmailMultiAlternatives

def send_email_notification(subject, message, recipient_list):
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body="This is a verification email.",
            from_email='dr.restful.code@gmail.com',  # Zameni svojom adresom
            to=recipient_list,
        )
        email.attach_alternative(message, "text/html")  # Dodaje HTML verziju e-maila
        email.send()

    except Exception as e:
        print(f"Failed to send email: {e}")

# kontrioler za verifikaciju korisnika
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

def verify_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # Dekodira uidb64
        user = get_user_model().objects.get(pk=uid) # Dobija korisnika na osnovu ID-a
        if default_token_generator.check_token(user, token): # Proverava token

            user.is_active = True # Aktivira korisnika

            user.save() # Čuva promene u bazi podataka
            messages.success(request, 'Your account has been verified!') # Prikazuje poruku uspeha
            return redirect('login') # Preusmerava na stranicu za prijavu
        
        #‚‚ Ako token nije validan, prikazuje poruku greške
        else:
            messages.error(request, 'The verification link is invalid or has expired.')
            return redirect('home')  # Ili bilo koja druga stranica

    # Ako dođe do greške prilikom dekodiranja ili pronalaženja korisnika, prikazuje poruku greške
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        messages.error(request, 'Invalid verification link.')
        return redirect('home')  # Ili bilo koja druga stranica


# Kontroler za ažuriranje profila
@login_required
def update_profile(request):
    if request.method == "POST": # Proveravamo da li korisnik šalje podatke putem POST zahteva.
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            #return redirect("profile", pk=request.user.profile.pk)
            return redirect("home")
    else:
        form = ProfileUpdateForm(instance=request.user.profile, user=request.user)

    return render(request, "profiles/update_profile.html", {"form": form})




