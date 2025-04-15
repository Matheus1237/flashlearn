from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        self.stdout.write('Starting create_admin command...')
        
        try:
            # Verifica se o banco de dados está pronto
            self.stdout.write('Checking database...')
            User.objects.count()  # Isso vai falhar se o banco não estiver pronto
            
            if not User.objects.filter(username='admin').exists():
                self.stdout.write('Creating superuser...')
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser already exists'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
            raise