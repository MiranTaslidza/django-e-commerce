from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.contrib import messages

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        if not user.pk:
            user.set_unusable_password()
            user.is_active = False
            user.email = sociallogin.account.extra_data.get('email')
            user.username = user.email.split('@')[0]
            user.save()

            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f'http://{domain}/profiles/verify/{uid}/{token}/'

            subject = "Potvrdi svoj email"
            html = render_to_string('profiles/activation_email.html', {
                'user': user, 'link': link
            })
            email = EmailMultiAlternatives(subject, 'Potvrdi email.', to=[user.email])
            email.attach_alternative(html, 'text/html')
            email.send()
        return user
    
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                # Poveži socijalni nalog sa postojećim korisnikom
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                # Nema takvog korisnika, nastavi sa regularnom registracijom
                pass

class CustomAccountAdapter(DefaultAccountAdapter):
    def respond_user_inactive(self, request, user):
        messages.error(request, "Morate potvrditi e‑mail prije prijave.")
        return redirect('/profiles/login/')
