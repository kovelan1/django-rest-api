# Generated by Django 5.0 on 2023-12-20 18:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketballLeague', '0005_remove_playerprofile_average_score_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserStats',
            new_name='UserLogs',
        ),
    ]
