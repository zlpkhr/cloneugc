# Generated by Django 5.2.1 on 2025-05-28 07:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booth", "0006_creator_language_alter_creator_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="creator",
            name="cartesia_voice_id",
            field=models.TextField(blank=True, editable=False, null=True),
        ),
    ]
