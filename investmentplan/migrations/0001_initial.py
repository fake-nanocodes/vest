# Generated by Django 4.2.4 on 2023-09-02 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
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
        migrations.CreateModel(
            name='InvestmentPlanHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('maximum_amount', models.FloatField(blank=True, default=0, null=True)),
                ('minimum_amount', models.FloatField(blank=True, default=0, null=True)),
                ('number_of_days', models.FloatField(blank=True, default=0, null=True)),
                ('investment_profit_percent', models.FloatField(blank=True, default=0, null=True)),
                ('referral_profit_percent', models.FloatField(blank=True, default=0, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('profit', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('profile', models.ManyToManyField(related_name='userprofile', to='userprofile.profile')),
            ],
            options={
                'verbose_name': 'InvestmentPlanHistory',
                'verbose_name_plural': 'InvestmentPlanHistory',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('minimum_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('maximum_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('number_of_days', models.IntegerField(blank=True, default=0, null=True)),
                ('investment_profit_percent', models.FloatField(blank=True, default=0, null=True)),
                ('referral_profit_percent', models.FloatField(blank=True, default=0, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investmentplan.category')),
            ],
            options={
                'verbose_name': 'InvestmentPlan',
                'verbose_name_plural': 'InvestmentPlan',
                'ordering': ['-created'],
            },
        ),
    ]
