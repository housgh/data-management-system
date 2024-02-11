# Generated by Django 3.2.24 on 2024-02-11 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagementsystem', '0006_alter_property_entity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='property_type',
        ),
        migrations.AddField(
            model_name='property',
            name='property_type_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
