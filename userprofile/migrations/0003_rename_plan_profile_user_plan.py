# Generated by Django 4.2.4 on 2023-09-02 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_profile_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='plan',
            new_name='user_plan',
        ),
    ]
