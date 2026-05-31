from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0002_customerreview_sitesettings_google_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image_url',
            field=models.URLField(blank=True, verbose_name='URL image externe'),
        ),
    ]
