from django.db import migrations, models
import django.db.models.deletion


def migrate_vehicle_images(apps, schema_editor):
    UsedVehicle = apps.get_model('garage', 'UsedVehicle')
    VehicleImage = apps.get_model('garage', 'VehicleImage')

    for vehicle in UsedVehicle.objects.all():
        if vehicle.image_url:
            VehicleImage.objects.create(
                vehicle=vehicle,
                image_url=vehicle.image_url,
                order=0,
            )
        elif vehicle.image:
            VehicleImage.objects.create(
                vehicle=vehicle,
                image=vehicle.image,
                order=0,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0008_image_url_charfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicles/gallery/', verbose_name='Image')),
                ('image_url', models.CharField(blank=True, max_length=500, verbose_name='URL image externe')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='garage.usedvehicle', verbose_name='Véhicule')),
            ],
            options={
                'verbose_name': 'Photo véhicule',
                'verbose_name_plural': 'Photos véhicule',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(migrate_vehicle_images, migrations.RunPython.noop),
    ]
