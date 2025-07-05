from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Delete users who haven't verified their email within 24 hours."

    def handle(self, *args, **kwargs):
        expiry_time = now() - timedelta(hours=24)  # Menjaj na minute za testiranje
        inactive_users = User.objects.filter(is_active=False, date_joined__lt=expiry_time)
        count = inactive_users.count()
        inactive_users.delete()
        self.stdout.write(f"{count} inactive users deleted.")


