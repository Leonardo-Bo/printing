# Generated by Django 4.1.3 on 2023-01-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_alter_publication_doi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='authors',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]
