# Generated by Django 4.1.7 on 2023-06-06 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cozy_app', '0021_alter_progress_project_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost_project',
            name='id_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cozy_app.project'),
        ),
        migrations.AlterField(
            model_name='progress_project',
            name='id_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cozy_app.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='id_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cozy_app.customer'),
        ),
    ]
