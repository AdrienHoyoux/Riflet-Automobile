from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('garage', '0005_alter_usedvehicle_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMfaDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(max_length=64, verbose_name='Secret TOTP')),
                ('is_enabled', models.BooleanField(default=False, verbose_name='Activée')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True, verbose_name='Confirmée le')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mfa_device', to='auth.user', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'MFA administrateur',
                'verbose_name_plural': 'MFA administrateurs',
            },
        ),
    ]
