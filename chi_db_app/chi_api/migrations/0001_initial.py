# Generated by Django 4.2 on 2023-04-16 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('license_number', models.CharField(blank=True, max_length=10, null=True)),
                ('license_state', models.CharField(blank=True, max_length=20, null=True)),
                ('insurance_provider', models.CharField(blank=True, max_length=20, null=True)),
                ('policy_number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('job_title', models.CharField(blank=True, max_length=20, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('benefits', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('vehicle_id', models.AutoField(primary_key=True, serialize=False)),
                ('vin', models.CharField(blank=True, max_length=50, null=True)),
                ('make', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('trim', models.CharField(blank=True, max_length=50, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('mpg', models.IntegerField(blank=True, null=True)),
                ('milage', models.IntegerField(blank=True, null=True)),
                ('country_of_assembly', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_type', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('history_date', models.DateTimeField(blank=True, null=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chi_api.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(blank=True, max_length=20, null=True)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chi_api.customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chi_api.employee')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chi_api.vehicle')),
            ],
        ),
    ]
