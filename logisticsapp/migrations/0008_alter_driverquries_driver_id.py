# Generated by Django 3.2.12 on 2022-11-04 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logisticsapp', '0007_driverquries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverquries',
            name='driver_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logisticsapp.driver'),
        ),
    ]
