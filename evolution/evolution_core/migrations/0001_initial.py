# Generated by Django 5.1.4 on 2025-01-02 03:57

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100),
                ),
                (
                    "current_tokens_food",
                    models.IntegerField(default=0),
                ),
                (
                    "current_tokens_shelter",
                    models.IntegerField(default=0),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True),
                ),
                (
                    "special_effects",
                    models.JSONField(default=dict),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Epoch",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "previous_epoch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.epoch",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "epoch",
                    models.IntegerField(default=1),
                ),
                (
                    "max_epochs",
                    models.IntegerField(default=6),
                ),
                (
                    "player_table",
                    models.JSONField(default=list),
                ),
                (
                    "trait_deck",
                    models.JSONField(default=list),
                ),
                (
                    "started",
                    models.BooleanField(default=False),
                ),
                (
                    "active_areas",
                    models.ManyToManyField(
                        related_name="active_games",
                        to="evolution_core.area",
                    ),
                ),
                (
                    "current_epoch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.epoch",
                    ),
                ),
                (
                    "waiting_areas",
                    models.ManyToManyField(
                        related_name="waiting_games",
                        to="evolution_core.area",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="area",
            name="game",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="areas",
                to="evolution_core.game",
            ),
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "score",
                    models.IntegerField(default=0),
                ),
                (
                    "hand",
                    models.JSONField(default=list),
                ),
                (
                    "in_game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.game",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="game",
            name="players",
            field=models.ManyToManyField(to="evolution_core.player"),
        ),
        migrations.AddField(
            model_name="epoch",
            name="first_player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="evolution_core.player",
            ),
        ),
        migrations.CreateModel(
            name="Animal",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "food_requirement",
                    models.IntegerField(default=1),
                ),
                (
                    "food_tokens",
                    models.IntegerField(default=0),
                ),
                (
                    "fat_tokens",
                    models.IntegerField(default=0),
                ),
                (
                    "shelter",
                    models.BooleanField(default=False),
                ),
                (
                    "traits",
                    models.JSONField(default=list),
                ),
                (
                    "is_alive",
                    models.BooleanField(default=True),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.game",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "animal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="evolution_core.animal",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.game",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evolution_core.player",
                    ),
                ),
            ],
        ),
    ]
