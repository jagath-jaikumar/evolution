import uuid

from django.contrib.auth.models import User
from django.db import models

from evolution.evolution_core.mechanics.phases import Phase


class Player(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    score = models.IntegerField(default=0, db_index=True)
    hand = models.JSONField(default=list)
    in_game = models.ForeignKey("Game", on_delete=models.CASCADE, db_index=True)
    animals = models.ManyToManyField("Animal", related_name="players", db_index=True)
    animal_order = models.JSONField(default=list)

    def __str__(self):
        return self.user.username


class Game(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    players = models.ManyToManyField(Player, db_index=True)
    player_table = models.JSONField(default=list, null=True)
    active_areas = models.ManyToManyField("Area", related_name="active_games", db_index=True)
    waiting_areas = models.ManyToManyField("Area", related_name="waiting_games", db_index=True)
    trait_deck = models.JSONField(default=list, null=True)
    started = models.BooleanField(default=False, db_index=True)
    ended = models.BooleanField(default=False, db_index=True)
    current_epoch = models.ForeignKey(
        "Epoch",
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['created_by', 'started', 'ended']),
            models.Index(fields=['started', 'ended']),
            models.Index(fields=['created_at', 'started']),
        ]

    def __str__(self):
        epoch_num = self.current_epoch.epoch_number if self.current_epoch else None
        return f"Game {self.id} - Epoch {epoch_num} - Started: {self.started} - Players: {self.players.count()}"


class Area(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="areas",
        db_index=True,
    )
    current_tokens_food = models.IntegerField(default=0, db_index=True)
    current_tokens_shelter = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return f"Area {self.name} - Food: {self.current_tokens_food}, Shelter: {self.current_tokens_shelter}"


class Animal(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE, db_index=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_index=True)
    food_requirement = models.IntegerField(default=1, db_index=True)
    food_tokens = models.IntegerField(default=0, db_index=True)
    fat_tokens = models.IntegerField(default=0, db_index=True)
    shelter = models.BooleanField(default=False, db_index=True)
    traits = models.JSONField(default=list)
    is_alive = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['player', 'game', 'is_alive']),
        ]

    def __str__(self):
        return (
            f"Animal {self.id} - Player: {self.player.user.username}, Food: {self.food_tokens}/{self.food_requirement}"
        )


class Action(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_index=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, db_index=True)
    action_set = models.JSONField(default=list)


class Epoch(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    epoch_number = models.IntegerField(default=1, db_index=True)
    previous_epoch = models.ForeignKey("Epoch", on_delete=models.CASCADE, null=True, db_index=True)
    first_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="epochs_as_first_player", db_index=True)
    current_phase = models.CharField(max_length=100, default=Phase.DEVELOPMENT, db_index=True)
    current_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, related_name="epochs_as_current_player", db_index=True
    )
