# Generated by Django 4.2.4 on 2023-09-02 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investmentplan', '0004_delete_plan'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plan',
            field=models.ManyToManyField(related_name='userplan', to='investmentplan.investmentplanhistory'),
        ),
    ]
