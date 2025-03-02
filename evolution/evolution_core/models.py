import uuid

from django.contrib.auth.models import User
from django.db import models

from evolution.evolution_core.mechanics.phases import Phase


def short_uuid():
    return str(uuid.uuid4())[:8]


class Player(models.Model):
    id = models.CharField(
        primary_key=True,
        default=short_uuid,
        editable=False,
        db_index=True,
        max_length=8,
    )
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="players")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    score = models.IntegerField(default=0, db_index=True)
    hand = models.JSONField(default=list)
    animals = models.JSONField(default=list)
    seat_position = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["seat_position"]  # Default ordering by seat
        unique_together = (("game", "seat_position"),)


class Game(models.Model):
    id = models.CharField(
        primary_key=True,
        default=short_uuid,
        editable=False,
        db_index=True,
        max_length=8,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    active_areas = models.JSONField(default=list)
    waiting_areas = models.JSONField(default=list)
    trait_deck = models.JSONField(default=list)
    game_started = models.BooleanField(default=False, db_index=True)
    game_ended = models.BooleanField(default=False, db_index=True)
    current_epoch = models.ForeignKey(
        "Epoch",
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
    )
    actions = models.ManyToManyField("GameAction")

    def __str__(self):
        epoch_num = self.current_epoch.epoch_number if self.current_epoch else None
        return f"Game {self.id} - Epoch {epoch_num} - Started: {self.game_started} - Players: {self.players.count()}"


class GameAction(models.Model):
    id = models.CharField(
        primary_key=True,
        default=short_uuid,
        editable=False,
        db_index=True,
        max_length=8,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    epoch = models.ForeignKey("Epoch", on_delete=models.CASCADE, related_name="actions", db_index=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, db_index=True)
    actions = models.JSONField(default=list)
    action_number = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["-action_number"]


class Epoch(models.Model):
    id = models.CharField(
        primary_key=True,
        default=short_uuid,
        editable=False,
        db_index=True,
        max_length=8,
    )
    epoch_number = models.IntegerField(default=1, db_index=True)
    previous_epoch = models.ForeignKey("Epoch", on_delete=models.CASCADE, null=True, db_index=True)
    first_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="epochs_as_first_player", db_index=True
    )
    current_phase = models.CharField(max_length=100, default=Phase.DEVELOPMENT.value, db_index=True)
    current_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, related_name="epochs_as_current_player", db_index=True
    )
