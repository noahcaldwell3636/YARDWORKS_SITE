# Generated by Django 3.0.4 on 2020-05-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reports', '0002_auto_20200518_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysalestotal',
            name='month',
            field=models.IntegerField(max_length=72),
        ),
        migrations.AlterField(
            model_name='monthlysalestotal',
            name='year',
            field=models.IntegerField(max_length=72),
        ),
    ]