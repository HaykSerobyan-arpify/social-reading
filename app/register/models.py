from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_image_file_extension, FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        if kwargs.get('is_active') is not True:
            raise ValueError('Superuser must be active')
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be staff')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        primary_key=True,
        editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar = models.ImageField(default='default.png', upload_to='profile_images',
                               validators=[validate_image_file_extension,
                                           FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                               blank=True)
    avatar_google = models.SlugField(null=True, blank=True)
    avatar_facebook = models.SlugField(null=True, blank=True)
    profile_background = models.ImageField(default='profile_default_background.jpeg', upload_to='profile_backgrounds',
                                           validators=[validate_image_file_extension,
                                                       FileExtensionValidator(
                                                           allowed_extensions=['jpeg', 'png', 'jpg'])],
                                           blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'avatar', 'avatar_google',
                       'avatar_facebook', 'profile_background', 'created', 'updated', 'auth_provider']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f'{self.email} - {self.get_full_name()}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
