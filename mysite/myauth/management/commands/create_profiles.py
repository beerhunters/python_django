from django.contrib.auth.models import User
from django.core.management import BaseCommand

from myauth.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)