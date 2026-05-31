# Generated manually for initial setup

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Téléphone')),
                ('subject', models.CharField(max_length=255, verbose_name='Sujet')),
                ('message', models.TextField(verbose_name='Message')),
                ('is_read', models.BooleanField(default=False, verbose_name='Lu')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Reçu le')),
            ],
            options={
                'verbose_name': 'Message de contact',
                'verbose_name_plural': 'Messages de contact',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='Riflet Automobile', max_length=255, verbose_name='Nom')),
                ('tagline_fr', models.CharField(blank=True, max_length=255, verbose_name='Slogan (FR)')),
                ('tagline_de', models.CharField(blank=True, max_length=255, verbose_name='Slogan (DE)')),
                ('tagline_nl', models.CharField(blank=True, max_length=255, verbose_name='Slogan (NL)')),
                ('about_fr', models.TextField(blank=True, verbose_name='À propos (FR)')),
                ('about_de', models.TextField(blank=True, verbose_name='À propos (DE)')),
                ('about_nl', models.TextField(blank=True, verbose_name='À propos (NL)')),
                ('address', models.CharField(max_length=255, verbose_name='Adresse')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Code postal')),
                ('country', models.CharField(default='Belgique', max_length=100, verbose_name='Pays')),
                ('phone', models.CharField(max_length=30, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('facebook_url', models.URLField(blank=True, verbose_name='Facebook')),
                ('monday_hours', models.CharField(default='08:30 - 12:00 | 13:00 - 17:30', max_length=100, verbose_name='Lundi')),
                ('tuesday_hours', models.CharField(default='08:30 - 12:00 | 13:00 - 17:30', max_length=100, verbose_name='Mardi')),
                ('wednesday_hours', models.CharField(default='08:30 - 12:00 | 13:00 - 17:30', max_length=100, verbose_name='Mercredi')),
                ('thursday_hours', models.CharField(default='08:30 - 12:00 | 13:00 - 17:30', max_length=100, verbose_name='Jeudi')),
                ('friday_hours', models.CharField(default='08:30 - 12:00 | 13:00 - 17:30', max_length=100, verbose_name='Vendredi')),
                ('saturday_hours', models.CharField(default='Fermé', max_length=100, verbose_name='Samedi')),
                ('sunday_hours', models.CharField(default='Fermé', max_length=100, verbose_name='Dimanche')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
                ('logo_url', models.URLField(blank=True, verbose_name='URL logo')),
                ('hero_image_url', models.URLField(blank=True, verbose_name='URL image hero')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Paramètres du site',
                'verbose_name_plural': 'Paramètres du site',
            },
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fr', models.CharField(max_length=255, verbose_name='Titre (FR)')),
                ('title_de', models.CharField(blank=True, max_length=255, verbose_name='Titre (DE)')),
                ('title_nl', models.CharField(blank=True, max_length=255, verbose_name='Titre (NL)')),
                ('description_fr', models.TextField(blank=True, verbose_name='Description (FR)')),
                ('description_de', models.TextField(blank=True, verbose_name='Description (DE)')),
                ('description_nl', models.TextField(blank=True, verbose_name='Description (NL)')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug')),
                ('content_fr', models.TextField(verbose_name='Contenu (FR)')),
                ('content_de', models.TextField(blank=True, verbose_name='Contenu (DE)')),
                ('content_nl', models.TextField(blank=True, verbose_name='Contenu (NL)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='news/', verbose_name='Image')),
                ('image_url', models.URLField(blank=True, verbose_name='URL image externe')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publié')),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de publication')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Actualité',
                'verbose_name_plural': 'Actualités',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fr', models.CharField(max_length=255, verbose_name='Titre (FR)')),
                ('title_de', models.CharField(blank=True, max_length=255, verbose_name='Titre (DE)')),
                ('title_nl', models.CharField(blank=True, max_length=255, verbose_name='Titre (NL)')),
                ('description_fr', models.TextField(blank=True, verbose_name='Description (FR)')),
                ('description_de', models.TextField(blank=True, verbose_name='Description (DE)')),
                ('description_nl', models.TextField(blank=True, verbose_name='Description (NL)')),
                ('icon', models.CharField(default='🔧', max_length=50, verbose_name='Icône (emoji ou nom)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Image')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['order', 'title_fr'],
            },
        ),
    ]
