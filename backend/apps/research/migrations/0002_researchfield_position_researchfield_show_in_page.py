# Generated by Django 4.1.3 on 2022-11-21 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchfield',
            name='position',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='researchfield',
            name='show_in_page',
            field=models.BooleanField(default=True),
        ),
    ]
