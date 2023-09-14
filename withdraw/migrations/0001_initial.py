# Generated by Django 4.2.4 on 2023-08-25 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('wallet_type', models.CharField(blank=True, max_length=50, null=True)),
                ('wallet_address', models.CharField(blank=True, max_length=100, null=True)),
                ('usdt_amount', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal', to='userprofile.profile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
