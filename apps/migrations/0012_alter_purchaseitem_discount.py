# Generated by Django 4.2.10 on 2024-03-10 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_purchaseitem_delete_purchase_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='discount',
            field=models.CharField(default='0', max_length=10),
        ),
    ]