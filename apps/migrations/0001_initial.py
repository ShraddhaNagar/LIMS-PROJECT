# Generated by Django 4.2.10 on 2024-03-03 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_indent', models.DateField()),
                ('material', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('grade', models.CharField(choices=[('AR', 'AR'), ('ACS', 'ACS'), ('HPLC', 'HPLC'), ('GC', 'GC'), ('LR', 'LR')], max_length=20)),
                ('supplier_nameaddress', models.CharField(choices=[('vendor1', 'Vendor 1'), ('vendor2', 'Vendor 2'), ('vendor3', 'Vendor 3'), ('vendor4', 'Vendor 4')], max_length=200)),
                ('incoming_material_inspection', models.CharField(choices=[('Ok', 'Ok'), ('Fine', 'Fine'), ('Not Ok', 'Not Ok')], max_length=20)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=8)),
                ('material_received_date', models.DateField(blank=True, null=True)),
                ('hsn_sac', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_no', models.CharField(blank=True, max_length=30, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]