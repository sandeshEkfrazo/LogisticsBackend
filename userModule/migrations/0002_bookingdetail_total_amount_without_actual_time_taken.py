# Generated by Django 3.2.12 on 2023-03-01 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdetail',
            name='total_amount_without_actual_time_taken',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
