# Generated by Django 3.2.23 on 2024-02-06 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagementsystem', '0002_userdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='organizationId',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datamanagementsystem.organization'),
        ),
    ]
