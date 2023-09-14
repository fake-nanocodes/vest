# Generated by Django 4.2.4 on 2023-08-26 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('usdt_amount', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer'), ('bonus', 'Bonus'), ('penalty', 'Penalty')], max_length=20)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
            ],
        ),
    ]
