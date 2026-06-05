from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0004_usedvehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedvehicle',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Prix (€)'),
        ),
    ]
