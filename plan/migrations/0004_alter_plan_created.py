# Generated by Django 4.2.4 on 2023-09-02 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_plan_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
