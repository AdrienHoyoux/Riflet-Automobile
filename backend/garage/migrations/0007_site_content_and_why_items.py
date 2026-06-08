from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0006_adminmfadevice'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhyChooseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_fr', models.CharField(max_length=500, verbose_name='Texte (FR)')),
                ('text_de', models.CharField(blank=True, max_length=500, verbose_name='Texte (DE)')),
                ('text_nl', models.CharField(blank=True, max_length=500, verbose_name='Texte (NL)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Argument « Pourquoi nous choisir »',
                'verbose_name_plural': 'Arguments « Pourquoi nous choisir »',
                'ordering': ['order', 'pk'],
            },
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_image_url',
            field=models.URLField(blank=True, verbose_name='URL image page À propos'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_subtitle_de',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre page À propos (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_subtitle_fr',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre page À propos (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_subtitle_nl',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre page À propos (NL)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_title_de',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre page À propos (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_title_fr',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre page À propos (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_title_nl',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre page À propos (NL)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_services_subtitle_de',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre section services accueil (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_services_subtitle_fr',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre section services accueil (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_services_subtitle_nl',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre section services accueil (NL)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_services_title_de',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre section services accueil (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_services_title_fr',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre section services accueil (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_services_title_nl',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre section services accueil (NL)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_why_title_de',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre « Pourquoi nous choisir » (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_why_title_fr',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre « Pourquoi nous choisir » (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_why_title_nl',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre « Pourquoi nous choisir » (NL)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='services_subtitle_de',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre page Services (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='services_subtitle_fr',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre page Services (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='services_subtitle_nl',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sous-titre page Services (NL)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='services_title_de',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre page Services (DE)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='services_title_fr',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre page Services (FR)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='services_title_nl',
            field=models.CharField(blank=True, max_length=255, verbose_name='Titre page Services (NL)'),
        ),
    ]
