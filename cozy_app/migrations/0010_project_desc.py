# Generated by Django 4.1.7 on 2023-03-23 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cozy_app", "0009_cost_project_cost_lain"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="desc",
            field=models.TextField(null=True),
        ),
    ]