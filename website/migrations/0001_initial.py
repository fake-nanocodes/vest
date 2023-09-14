# Generated by Django 4.2.4 on 2023-09-01 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Blank Name', max_length=50, null=True)),
                ('email', models.EmailField(blank=True, default='Blank Email', max_length=254, null=True)),
                ('address', models.CharField(blank=True, default='Blank Address', max_length=300, null=True)),
                ('second_address', models.CharField(blank=True, default='Blank Address', max_length=300, null=True)),
                ('logo', models.ImageField(default='logo.png', upload_to='site_images')),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True)),
                ('minimum_withdrawal', models.FloatField(blank=True, default=0, null=True)),
                ('maximum_withdrawal', models.FloatField(blank=True, default=0, null=True)),
                ('owned_by', models.CharField(blank=True, default='Admin', max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Website',
                'verbose_name_plural': 'Website',
            },
        ),
    ]