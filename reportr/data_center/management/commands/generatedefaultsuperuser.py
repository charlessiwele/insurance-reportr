import logging
import pathlib
import random
import string
from django.contrib.auth.models import User
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE A SUPERUSER'
    """
    This command is useful for generating a superuser with randomly generated username and email detail combo
    The details will be written to a file including the default password
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to default superuser generator')
            username = 'admin'
            password = 'admin'
            user_email = f'{username}@{username}.{username[:2]}'
            User.objects.create_superuser(username, user_email, password)
            print(f'Generated:\n username: {username} user_email: {user_email}, password: {password}')
        except Exception as exception:
            print(exception.__str__())
