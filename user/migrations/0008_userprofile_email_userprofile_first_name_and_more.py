# Generated by Django 5.1.3 on 2025-02-23 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
