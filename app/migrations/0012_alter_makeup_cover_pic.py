# Generated by Django 5.1.3 on 2025-03-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_makeup_cover_pic_makeup_created_at_makeup_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makeup',
            name='cover_pic',
            field=models.ImageField(blank=True, default='default-cover.jpg', null=True, upload_to='static/uploads/'),
        ),
    ]
