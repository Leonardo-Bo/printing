# Generated by Django 4.1.3 on 2022-11-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_alter_person_email_alter_person_link_scholar'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='position',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='person',
            name='show_in_page',
            field=models.BooleanField(default=True),
        ),
    ]
