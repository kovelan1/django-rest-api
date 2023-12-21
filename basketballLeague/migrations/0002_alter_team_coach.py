# Generated by Django 5.0 on 2023-12-20 17:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketballLeague', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='coach',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team', to=settings.AUTH_USER_MODEL),
        ),
    ]
