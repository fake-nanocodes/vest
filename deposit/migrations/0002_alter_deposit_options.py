# Generated by Django 4.2.4 on 2023-08-25 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deposit',
            options={'ordering': ['-time']},
        ),
    ]
