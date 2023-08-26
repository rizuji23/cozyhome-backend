# Generated by Django 4.1.7 on 2023-03-15 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cozy_app", "0002_customer_kategori_material_material_project_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Modified_Stok",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("id_modified_stok", models.CharField(max_length=100)),
                ("stok", models.BigIntegerField()),
                ("keterangan", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id_material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cozy_app.material",
                    ),
                ),
                (
                    "id_stok_gudang",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cozy_app.stok_gudang",
                    ),
                ),
            ],
        ),
    ]
