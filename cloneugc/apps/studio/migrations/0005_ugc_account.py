# Generated by Django 5.2.1 on 2025-05-30 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_alter_account_user"),
        ("studio", "0004_ugc_audio"),
    ]

    operations = [
        migrations.AddField(
            model_name="ugc",
            name="account",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="account.account",
            ),
        ),
    ]
