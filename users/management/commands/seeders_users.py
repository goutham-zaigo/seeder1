from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username='admin', email='admin@example.com')
        if created:
            user.set_password('adminpass')
            user.role = 'admin'
            user.save()
        self.stdout.write('User seeded!')
