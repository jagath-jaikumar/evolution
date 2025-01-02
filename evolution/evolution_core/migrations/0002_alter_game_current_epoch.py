# Generated by Django 5.1.4 on 2025-01-02 03:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("evolution_core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="current_epoch",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="evolution_core.epoch",
            ),
        ),
    ]