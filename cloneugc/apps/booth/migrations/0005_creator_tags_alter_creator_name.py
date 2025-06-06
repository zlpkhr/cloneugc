# Generated by Django 5.2.1 on 2025-05-28 06:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booth", "0004_alter_creator_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="creator",
            name="tags",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=64),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="creator",
            name="name",
            field=models.CharField(max_length=64),
        ),
    ]
