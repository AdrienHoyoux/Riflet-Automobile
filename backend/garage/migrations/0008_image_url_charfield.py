from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0007_site_content_and_why_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL image externe'),
        ),
        migrations.AlterField(
            model_name='service',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL image externe'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='about_image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL image page À propos'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL image hero'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='logo_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL logo'),
        ),
        migrations.AlterField(
            model_name='usedvehicle',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL image externe'),
        ),
    ]
