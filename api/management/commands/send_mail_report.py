from api.serializers import DishSerializer
from django.core.management import call_command
from django.core.management.base import BaseCommand

from api.models import Dish
from django.core.mail import send_mail
from django.contrib.auth.models import User

import datetime
from django.utils.timezone import get_current_timezone


class Command(BaseCommand):

    def handle(self, *args, **options):
        date_from = datetime.datetime.now(tz=get_current_timezone()) - datetime.timedelta(days=1)
        new_dishes = Dish.objects.filter(created_at__gte=date_from)
        modified_dishes = Dish.objects.filter(modified_at__gte=date_from)
        if new_dishes.exists() | modified_dishes.exists():
            # not the fastest way, but get the job done.
            new_dishes_message = 'New Dishes:\n' if new_dishes.exists() else ''
            for dish in new_dishes:
                new_dishes_message += DishSerializer(
                    dish).get_mail_description()

            modified_dishes_message = 'New Dishes:\n' if modified_dishes.exists() else ''
            for dish in modified_dishes:
                modified_dishes_message += DishSerializer(
                    dish).get_mail_description()

            send_mail('New and modifies dishes', new_dishes_message + modified_dishes, 'django@test.mailtrap.pl',
                      User.objects.filter(is_superuser=True).values_list('email'), fail_silently=False)
