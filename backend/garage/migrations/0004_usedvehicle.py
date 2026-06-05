from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0003_service_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fr', models.CharField(max_length=255, verbose_name='Titre (FR)')),
                ('title_de', models.CharField(blank=True, max_length=255, verbose_name='Titre (DE)')),
                ('title_nl', models.CharField(blank=True, max_length=255, verbose_name='Titre (NL)')),
                ('description_fr', models.TextField(blank=True, verbose_name='Description (FR)')),
                ('description_de', models.TextField(blank=True, verbose_name='Description (DE)')),
                ('description_nl', models.TextField(blank=True, verbose_name='Description (NL)')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug')),
                ('brand', models.CharField(max_length=80, verbose_name='Marque')),
                ('model_name', models.CharField(max_length=80, verbose_name='Modèle')),
                ('year', models.PositiveIntegerField(verbose_name='Année')),
                ('mileage', models.PositiveIntegerField(verbose_name='Kilométrage (km)')),
                ('fuel_type', models.CharField(
                    choices=[
                        ('petrol', 'Essence'),
                        ('diesel', 'Diesel'),
                        ('electric', 'Électrique'),
                        ('hybrid', 'Hybride'),
                        ('lpg', 'LPG'),
                    ],
                    default='diesel',
                    max_length=20,
                    verbose_name='Carburant',
                )),
                ('transmission', models.CharField(
                    choices=[('manual', 'Manuelle'), ('automatic', 'Automatique')],
                    default='manual',
                    max_length=20,
                    verbose_name='Boîte',
                )),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix (€)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicles/', verbose_name='Image')),
                ('image_url', models.URLField(blank=True, verbose_name='URL image externe')),
                ('is_active', models.BooleanField(default=True, verbose_name='Visible sur le site')),
                ('is_sold', models.BooleanField(default=False, verbose_name='Vendu')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': "Véhicule d'occasion",
                'verbose_name_plural': "Véhicules d'occasion",
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
