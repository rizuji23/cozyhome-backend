# Generated by Django 4.1.7 on 2023-08-26 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cozy_app', '0037_alat_total_harga'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alat',
            name='total_harga',
        ),
    ]
