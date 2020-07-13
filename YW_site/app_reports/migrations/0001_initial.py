# Generated by Django 3.0.4 on 2020-05-16 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=72)),
                ('account', models.CharField(max_length=72)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlySalesTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=72)),
                ('year', models.CharField(max_length=72)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=24)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_reports.Company')),
            ],
        ),
    ]