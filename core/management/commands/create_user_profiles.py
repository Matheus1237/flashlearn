from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Create user profiles for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count = 0
        for user in users:
            UserProfile.objects.get_or_create(user=user)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {count} user profiles')) 