from django.core.management import call_command
from django.core.management.base import BaseCommand

from api.models import Menu

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Menu.objects.exists():
            self.stdout.write('Seeding initial data')
            call_command('loaddata', 'data.json')
        else:
            self.stdout.write('Initial data exists, skipping...')