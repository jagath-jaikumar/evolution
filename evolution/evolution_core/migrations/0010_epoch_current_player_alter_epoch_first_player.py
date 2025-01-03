# Generated by Django 5.1.4 on 2025-01-03 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "evolution_core",
            "0009_remove_action_animal_remove_action_timestamp_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="epoch",
            name="current_player",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="epochs_as_current_player",
                to="evolution_core.player",
            ),
        ),
        migrations.AlterField(
            model_name="epoch",
            name="first_player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="epochs_as_first_player",
                to="evolution_core.player",
            ),
        ),
    ]
