# Generated by Django 5.1.4 on 2025-01-02 04:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "evolution_core",
            "0003_alter_game_player_table_alter_game_trait_deck",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="area",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="area",
            name="special_effects",
        ),
    ]
