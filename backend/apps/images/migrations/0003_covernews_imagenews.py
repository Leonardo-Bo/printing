# Generated by Django 4.1.3 on 2022-11-15 07:17

import apps.images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.images.models.news_cover_upload_to)),
                ('isCover', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Cover news',
                'verbose_name_plural': 'Cover news',
            },
        ),
        migrations.CreateModel(
            name='ImageNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.images.models.news_images_upload_to)),
            ],
            options={
                'verbose_name': 'Image news',
                'verbose_name_plural': 'Image news',
            },
        ),
    ]
