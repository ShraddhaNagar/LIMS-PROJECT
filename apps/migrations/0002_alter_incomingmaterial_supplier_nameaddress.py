# Generated by Django 4.2.10 on 2024-03-03 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingmaterial',
            name='supplier_nameaddress',
            field=models.CharField(choices=[('vendor1', 'Vendor 1'), ('vendor2', 'Vendor 2'), ('vendor3', 'Vendor 3'), ('vendor4', 'Vendor 4')], max_length=200, verbose_name='Supplier Name and Address'),
        ),
    ]