from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='google_maps_url',
            field=models.URLField(blank=True, verbose_name='Lien Google Maps'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_place_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='Google Place ID'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_rating',
            field=models.DecimalField(decimal_places=1, default=5.0, max_digits=2, verbose_name='Note Google'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_review_count',
            field=models.PositiveIntegerField(default=0, verbose_name="Nombre d'avis Google"),
        ),
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=120, verbose_name='Auteur')),
                ('rating', models.PositiveSmallIntegerField(default=5, verbose_name='Note')),
                ('content', models.TextField(verbose_name='Commentaire')),
                ('source', models.CharField(choices=[('google', 'Google'), ('facebook', 'Facebook'), ('manual', 'Manuel')], default='google', max_length=20, verbose_name='Source')),
                ('external_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID externe')),
                ('review_date', models.DateField(blank=True, null=True, verbose_name="Date de l'avis")),
                ('is_published', models.BooleanField(default=True, verbose_name='Publié')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Avis client',
                'verbose_name_plural': 'Avis clients',
                'ordering': ['order', '-review_date', '-created_at'],
            },
        ),
    ]
