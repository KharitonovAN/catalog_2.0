# Generated by Django 4.2 on 2024-03-05 19:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_field_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='field_uuid',
            field=models.UUIDField(default=uuid.UUID('dad80adb-7fd3-4e59-9c02-9149da9ab98f'), unique=True, verbose_name='UUID'),
        ),
    ]
