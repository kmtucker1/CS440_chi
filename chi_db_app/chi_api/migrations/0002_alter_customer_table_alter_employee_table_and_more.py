# Generated by Django 4.2 on 2023-04-17 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chi_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customer',
            table='customer',
        ),
        migrations.AlterModelTable(
            name='employee',
            table='employee',
        ),
        migrations.AlterModelTable(
            name='transaction',
            table='transaction',
        ),
        migrations.AlterModelTable(
            name='vehicle',
            table='vehicle',
        ),
        migrations.AlterModelTable(
            name='vehiclehistory',
            table='vehicle_history',
        ),
    ]
