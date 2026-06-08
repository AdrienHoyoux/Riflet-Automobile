from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0009_vehicleimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='vehicle',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='contact_messages',
                to='garage.usedvehicle',
                verbose_name='Véhicule concerné',
            ),
        ),
    ]
