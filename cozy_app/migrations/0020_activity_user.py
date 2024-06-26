# Generated by Django 4.1.7 on 2023-06-04 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cozy_app', '0019_progress_project_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity_User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_activity_user', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
