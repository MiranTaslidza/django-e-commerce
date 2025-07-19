from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm,  ProfileUpdateForm, ChangeEmailForm
from django.contrib.auth import authenticate, logout, authenticate, login as auth_login, get_user_model, update_session_auth_hash
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.core.signing import Signer, BadSignature, TimestampSigner
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes 
from django.template.loader import render_to_string




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


# detalji profila
@login_required
def get_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    context ={
        'profile':profile
    }

    return render(request, 'profiles/profile.html', context)



# registracija korisnika
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


# brisanje profila
@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return JsonResponse({"message": "Account deleted"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)



# promjena passworda
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # Promeni lozinku korisnika
            update_session_auth_hash(request, user)  # Održava aktivnu sesiju nakon promene lozinke
            
            # Slanje email obaveštenja
            subject = "Password Changed Successfully"
            message = render_to_string('profiles/password_change_email.html', {
                'user': user,
                'login_url': request.build_absolute_uri(reverse('login')),  # Link za prijavu
            })
            send_email_notification(subject, message, [user.email])
            
            messages.success(request, "Your password has been successfully updated!")
            return redirect('home')
        else:
            messages.error(request, "There was an error changing your password. Please try again.")
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'profiles/change_password.html', {'form': form})



# Kontroler za promenu emaila
@login_required
def change_email(request):
    """View za prikazivanje i obradu promene emaila."""
    if request.method == 'POST':
        form = ChangeEmailForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            profile = request.user.profile

            # Sačuvaj novi email privremeno i označi ga kao nepotvrđen
            profile.new_email = new_email
            profile.email_confirmed = False
            profile.save()

            # Generisanje sigurnosnog tokena za potvrdu
            signer = TimestampSigner()
            token = signer.sign(request.user.username)

            # Kreiraj link za potvrdu
            confirm_url = request.build_absolute_uri(
                reverse('confirm_email_change', kwargs={'token': token})
            )

            # Kreiraj link za otkazivanje promjene emaila
            cancel_url = request.build_absolute_uri(
                reverse('cancel_email_change', kwargs={'token': token})
            )

            # Slanje emaila na stari email
            mail_subject = 'Confirm Your Email Change'

            message = render_to_string('profiles/confirm_old_email.html', {
                'user': request.user,
                'confirm_url': confirm_url,
                'cancel_url': cancel_url,
            })

            send_mail(
                mail_subject,
                '',  # Ostavlja se prazno plain text, ili možeš dodati kratku poruku
                'noreply@mywebsite.com',
                [profile.user.email],
                html_message=message
            )

            messages.success(request, "We have sent a verification link to your old email address.")
            return redirect('profile', pk=request.user.pk)  # Možete redirektovati na neki drugi URL po potrebi

        else:
            messages.error(request, "There was an error with the email change. Please try again.")
    else:
        form = ChangeEmailForm(user=request.user)

    return render(request, 'profiles/change_email.html', {'form': form})



# potvrda na starom emailu
@login_required
def confirm_old_email(request, token):
    signer = TimestampSigner()
    try:
        # Dešifruj token da dobijemo korisničko ime
        username = signer.unsign(token, max_age=3600)
        user = get_object_or_404(User, username=username)
        
        if user.profile.email_confirmed:
            messages.info(request, "Ova promjena e-pošte je već potvrđena.")
            return redirect('profile', pk=request.user.pk)

        # Generiši novi token za potvrdu novog emaila
        new_token = signer.sign(user.profile.new_email)
        new_confirm_url = request.build_absolute_uri(
            reverse('confirm_new_email', kwargs={'token': new_token})
        )

        # Generiši cancel URL koristeći originalni token
        cancel_url = request.build_absolute_uri(
            reverse('cancel_email_change', kwargs={'token': token})
        )

        # Ovdje kreiraš dictionary s podacima – to je tvoj "context" za otkazivanje emaila 
        context = {
            'user': user,
            'new_confirm_url': new_confirm_url,
            'cancel_url': cancel_url,
        }

        # Ovdje se koristi render_to_string s context-om
        message = render_to_string('profiles/confirm_new_email.html', context)

        # Pošalji email
        mail_subject = 'Potvrdi promjenu e-pošte'
        send_mail(
            mail_subject,
            '',  # Ostavlja se prazno plain text, ili možeš dodati kratku poruku
            'noreply@mywebsite.com',
            [user.profile.new_email],
            html_message=message
        )
        
        messages.success(request, "Verifikacijski link je poslan na tvoj novi email.")
        return redirect('profile', pk=request.user.pk)

    except BadSignature:
        messages.error(request, "Nevažeći ili istekli token.")
        return redirect('profile', pk=request.user.pk)




# kontroler za poništavanje promjene emaila
@login_required
def cancel_email_change(request, token):
    """
    View koja poništava zahtev za promenu emaila. Proverava token (npr. da li pripada
    trenutnom korisniku) i briše vrednost new_email u profilu.
    """
    signer = TimestampSigner()
    try:
        # Pretpostavljamo da je token generisan na način da sadrži username.
        token_username = signer.unsign(token, max_age=3600)  # token važi 1 sat
        if token_username != request.user.username:
            messages.error(request, "Invalid cancellation token.")
            return redirect('profile', pk=request.user.pk)
    except BadSignature:
        messages.error(request, "Invalid or expired cancellation link.")
        return redirect('profile', pk=request.user.pk)
    
    # Ako je token validan, poništavamo zahtev
    profile = request.user.profile
    profile.new_email = None  # Brišemo privremeno čuvani novi email
    profile.email_confirmed = False
    profile.save()
    
    messages.success(request, "Your email change request has been cancelled.")
    return redirect('profile', pk=request.user.pk)

# Kontroler za potvrdu novog emaila
@login_required
def confirm_new_email(request, token):
    """
    View koji finalizira promjenu emaila. Korisnik klikne na verifikacioni link iz emaila
    poslanog na novu adresu, a ovdje se token provjerava, stari email se sprema, a email se ažurira.
    """
    signer = TimestampSigner()
    try:
        # Dešifruj token da dobijemo novu email adresu
        new_email = signer.unsign(token, max_age=3600)  # Token vrijedi 1 sat
        user = request.user
        profile = user.profile

        # Provjeri da li se tokenirani novi email podudara s onim koji je privremeno spremljen
        if profile.new_email != new_email:
            messages.error(request, "Token se ne podudara s novom email adresom.")
            return redirect('profile', pk=user.pk)

        # Sačuvaj trenutnu email adresu u polje old_email, prije ažuriranja
        profile.old_email = user.email
        profile.save()

        # Ažuriraj email korisnika
        user.email = new_email
        user.save()

        # Označi da je nova email adresa potvrđena i očisti privremeni podatak
        profile.email_confirmed = True
        profile.new_email = None
        profile.save()

        messages.success(request, "Vaša email adresa je uspješno promijenjena!")
        return redirect('profile', pk=user.pk)

    except BadSignature:
        messages.error(request, "Nevažeći ili istekli token.")
        return redirect('profile', pk=request.user.pk)

