# Generated by Django 3.2.4 on 2023-07-21 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0003_bookingdistance_last_km_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queries',
            name='isfor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roleRef', to='masters.userroleref'),
        ),
    ]
