# Generated by Django 5.1.3 on 2025-01-03 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userprofile_is_artist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
    ]
