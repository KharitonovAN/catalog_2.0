from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    class Country(models.TextChoices):
        RUSSIA = 'RUS', 'Россия'
        ARMENIA = 'ARM', 'Армения'
        BELARUS = 'BLR', 'Беларусь'
        GEORGIA = 'GEO', 'Грузия'
        CHINA = 'CHN', 'Китай'

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(choices=Country.choices, verbose_name='Страна', default=Country.RUSSIA)
    field_uuid = models.UUIDField(unique=True, default=uuid.uuid4(), verbose_name='UUID')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}/{self.is_active}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
