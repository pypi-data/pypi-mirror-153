# Generated by Django 3.0.13 on 2022-04-21 15:32

from django.db import migrations
import django.db.models.deletion
import suppliers.models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
        ('invoices', '0004_auto_20220115_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='supplier',
            field=suppliers.models.SupplierField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='arrivals', to='suppliers.Supplier', verbose_name='Supplier'),
        ),
    ]
