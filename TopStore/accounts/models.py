from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from .managers import TopStoreUserManager


# Create your models here.


class TopStoreUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(4),
        ],
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = TopStoreUserManager()

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    profile_image = models.ImageField(
        upload_to='profiles',
        blank=True,
    )
    user = models.OneToOneField(
        TopStoreUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )


from .signals import *
