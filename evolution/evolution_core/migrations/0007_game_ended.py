# Generated by Django 5.1.4 on 2025-01-02 22:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("evolution_core", "0006_alter_epoch_previous_epoch"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="ended",
            field=models.BooleanField(default=False),
        ),
    ]