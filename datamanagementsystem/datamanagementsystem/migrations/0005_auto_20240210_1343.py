# Generated by Django 3.2.24 on 2024-02-10 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagementsystem', '0004_entity_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='entity_id',
        ),
        migrations.AddField(
            model_name='property',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datamanagementsystem.entity'),
        ),
    ]
