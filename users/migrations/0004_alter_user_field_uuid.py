# Generated by Django 4.2 on 2024-02-21 20:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_field_uuid_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='field_uuid',
            field=models.UUIDField(default=uuid.UUID('7ac52f8f-5fa7-474b-ab19-80b801d33f30'), unique=True, verbose_name='UUID'),
        ),
    ]
