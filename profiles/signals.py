from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
import os

# Ovaj signal se aktivira kada se kreira ili ažurira korisnik, tako da automatski kreira profil kada se kreira korisnik
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:  # Ako je korisnik nov, kreiraj profil
        Profile.objects.create(user=instance)
    else:  # Ako se korisnik već ažurira, sačuvaj njegov profil
        instance.profile.save()

# Briše sliku korisnika kada se profil obriše
@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)  # Briše sliku kada se profil obriše
