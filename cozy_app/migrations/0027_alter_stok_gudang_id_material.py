# Generated by Django 4.1.7 on 2023-06-11 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cozy_app', '0026_alter_project_id_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stok_gudang',
            name='id_material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cozy_app.material'),
        ),
    ]
