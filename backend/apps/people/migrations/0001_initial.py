# Generated by Django 4.1.3 on 2022-11-16 05:14

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crossuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('role', models.CharField(max_length=255)),
                ('github', models.CharField(blank=True, max_length=255, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('link_scholar', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_person', to='crossuser.userid')),
                ('author_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_person_update', to='crossuser.userid')),
            ],
        ),
    ]
