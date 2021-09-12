from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class TopStoreUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The user must have an email')
        if not username:
            raise ValueError('The user must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields)

        user.password = make_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)
