from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # ime i prezima uzima iz ovog modela 
    street = models.CharField(max_length=100, blank=True) # ulica 
    postal_code = models.CharField(max_length=10, blank=True) #poštarski kod
    city = models.CharField(max_length=100, blank=True) # grad
    state = models.CharField(max_length=100, blank=True) # država
    phone_number = models.CharField(max_length=20, blank=True) # broj telefona
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True) # slika
    #POLJE ZA ISTORIJU KUPLJENI PROIZVODA PREKO KORPE
    birth_date = models.DateField(null=True, blank=True) # datum rođenja

    USER_ROLES = [
        ('buyer', 'Kupac'),
        ('seller', 'Prodavac'),
    ]

    #Polje za tip korisnika
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='buyer'
    )

    def __str__(self):
        return self.user.username
    
    # polje 7 istorija narudzbi se dodaje unutar korpe i uzima se preko serijalizera da prikaže korisniku istoriju narudzbi

    def save(self, *args, **kwargs):
        """Ako korisnik menja sliku, brišemo staru pre nego šaljemo novu."""
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.profile_picture and old_profile.profile_picture != self.profile_picture:
                if old_profile.profile_picture.name != "avatar.png":
                    default_storage.delete(old_profile.profile_picture.path)
        except Profile.DoesNotExist:
            pass

        # **OBAVEZNO** zovi parentski save da se upišu polja u bazu:
        super().save(*args, **kwargs)