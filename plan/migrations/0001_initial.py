# Generated by Django 4.2.4 on 2023-09-02 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0003_rename_plan_profile_user_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_days', models.IntegerField(blank=True, default=0, null=True)),
                ('investment_profit_percent', models.FloatField(blank=True, default=0, null=True)),
                ('referral_profit_percent', models.FloatField(blank=True, default=0, null=True)),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('profit', models.FloatField(blank=True, default=0, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
            ],
        ),
    ]
