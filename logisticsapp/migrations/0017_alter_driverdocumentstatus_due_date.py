# Generated by Django 3.2.4 on 2023-07-13 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticsapp', '0016_auto_20230712_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocumentstatus',
            name='due_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
