# Generated by Django 4.1.7 on 2023-06-04 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cozy_app', '0020_activity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress_project',
            name='foto',
            field=models.ImageField(default='', upload_to='progress/'),
        ),
    ]
