# Generated by Django 3.2.4 on 2023-08-09 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticsapp', '0006_driver_owner_driving_licence'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
