# Generated by Django 3.2.7 on 2023-09-25 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logisticsapp', '0007_customuser_user_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='insurence_expire_date',
            new_name='insurance_expire_date',
        ),
    ]
