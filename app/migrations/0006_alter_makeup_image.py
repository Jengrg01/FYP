# Generated by Django 5.1.3 on 2024-12-16 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_makeup_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makeup',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
