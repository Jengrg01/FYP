# Generated by Django 5.1.3 on 2024-12-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_makeup_image_url_makeup_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makeup',
            name='rate',
            field=models.IntegerField(),
        ),
    ]
