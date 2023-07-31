# Generated by Django 3.2.12 on 2023-03-02 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logisticsapp', '0002_subscriptionplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle_Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_period', models.CharField(blank=True, max_length=100, null=True)),
                ('date_subscribed', models.DateTimeField(blank=True, max_length=100, null=True)),
                ('expiry_date', models.DateTimeField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('is_amount_paid', models.BooleanField(default=False)),
                ('paid_through', models.CharField(blank=True, max_length=100, null=True)),
                ('type_of_service', models.CharField(blank=True, max_length=100, null=True)),
                ('validity_days', models.IntegerField(blank=True, null=True)),
                ('vehicle_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logisticsapp.vehicle')),
            ],
        ),
    ]
