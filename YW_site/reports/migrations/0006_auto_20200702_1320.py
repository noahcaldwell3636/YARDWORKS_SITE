# Generated by Django 3.0.8 on 2020-07-02 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20200519_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstablishedSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('customer_number', models.CharField(max_length=32)),
                ('sale_type', models.CharField(max_length=16)),
                ('bill_to_name', models.CharField(max_length=128)),
                ('bill_to_address', models.CharField(max_length=256)),
                ('bill_to_city', models.CharField(max_length=128)),
                ('bill_to_state', models.CharField(max_length=8)),
                ('bill_to_zip', models.CharField(max_length=16)),
                ('ship_to_name', models.CharField(max_length=128)),
                ('ship_to_address', models.CharField(max_length=256)),
                ('ship_to_city', models.CharField(max_length=128)),
                ('ship_to_state', models.CharField(max_length=8)),
                ('ship_to_zip', models.CharField(max_length=16)),
                ('ship_date', models.DateField(blank=True, null=True)),
                ('payment_type', models.CharField(max_length=16)),
                ('warehouse_code', models.CharField(max_length=16)),
                ('taxable_amount', models.FloatField()),
                ('nontaxable_amount', models.FloatField()),
                ('freight_amount', models.FloatField()),
                ('sales_tax_amount', models.FloatField()),
                ('cost_of_sales', models.FloatField()),
                ('batch', models.CharField(max_length=32)),
                ('amount_without_tax', models.FloatField()),
                ('amount_with_tax', models.FloatField()),
                ('profit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=16)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='groups',
        ),
        migrations.AddField(
            model_name='companygroup',
            name='companies',
            field=models.ManyToManyField(to='reports.Company'),
        ),
        migrations.DeleteModel(
            name='MonthlySalesTotal',
        ),
        migrations.AddField(
            model_name='invoice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Company'),
        ),
        migrations.AddField(
            model_name='establishedsite',
            name='invoices',
            field=models.ManyToManyField(to='reports.Invoice'),
        ),
    ]
