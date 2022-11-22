# Generated by Django 4.1.3 on 2022-11-16 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0001_initial'),
        ('crossuser', '0001_initial'),
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('show_in_home', models.BooleanField(default=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_carousel', to='crossuser.userid')),
                ('author_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_carousel_update', to='crossuser.userid')),
                ('field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carousel_field', to='research.researchfield')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carousel_news', to='news.news')),
            ],
            options={
                'verbose_name': 'Carousel',
                'verbose_name_plural': 'Carousel',
            },
        ),
    ]
