# Generated by Django 3.0.4 on 2020-04-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_library', '0004_remove_usage_first_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='units',
            field=models.CharField(default='None', max_length=32),
        ),
        migrations.AddField(
            model_name='usage',
            name='use_date',
            field=models.CharField(default='None', max_length=32),
        ),
        migrations.AlterField(
            model_name='usage',
            name='key',
            field=models.CharField(default='None', max_length=32),
        ),
    ]