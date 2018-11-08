from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core import models


class Command(BaseCommand):
    help = "Run to create_admin to create a default superuser account."

    def handle(self, *args, **options):

        if not User.objects.filter(username=settings.ADMIN_USERNAME):
            user = User.objects.create(
                username=settings.ADMIN_USERNAME,
                first_name=settings.ADMIN_USERNAME.title(),
                last_name=settings.ADMIN_USERNAME.title(),
                email=settings.ADMIN_EMAIL,
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )
            user.set_password(settings.ADMIN_PASSWORD)
            user.save()

            profile = models.Profile.objects.create(
                user=user,
                salutation='Mx',
                country='GB',
                institution='The Cloud',
                department='Tech',
            )
            for role in models.Role.objects.all():
                profile.roles.add(role)
            profile.save()

            print(f'Default admin user \'{user.username}\' created.')

        else:
            print(
                'Default admin user not created. '
                f'User \'{settings.ADMIN_USERNAME}\' already exists.'
            )
