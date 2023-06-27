from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


def user_directory_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
