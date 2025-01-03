import uuid

from django.contrib.auth.models import User
from django.db import models
from evolution.evolution_core.mechanics.states import Phase


class Player(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    hand = models.JSONField(default=list)
    in_game = models.ForeignKey("Game", on_delete=models.CASCADE)
    animals = models.ManyToManyField("Animal", related_name="players")
    animal_order = models.JSONField(default=list)

    def __str__(self):
        return self.user.username


class Game(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    epoch = models.IntegerField(default=1)  # Current Epoch (1-6)
    players = models.ManyToManyField(Player)
    player_table = models.JSONField(default=list, null=True)
    active_areas = models.ManyToManyField("Area", related_name="active_games")
    waiting_areas = models.ManyToManyField("Area", related_name="waiting_games")
    trait_deck = models.JSONField(default=list, null=True)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    current_epoch = models.ForeignKey(
        "Epoch",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"Game {self.id} - Epoch {self.epoch} - Started: {self.started} - Players: {self.players.count()}"


class Area(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="areas",
    )
    current_tokens_food = models.IntegerField(default=0)
    current_tokens_shelter = models.IntegerField(default=0)

    def __str__(self):
        return f"Area {self.id} - Food: {self.current_tokens_food}, Shelter: {self.current_tokens_shelter}"


class Animal(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    food_requirement = models.IntegerField(default=1)
    food_tokens = models.IntegerField(default=0)
    fat_tokens = models.IntegerField(default=0)
    shelter = models.BooleanField(default=False)
    traits = models.JSONField(default=list)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"Animal {self.id} - Player: {self.player.user.username}, Food: {self.food_tokens}/{self.food_requirement}"
        )


class Action(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    action_set = models.JSONField(default=list)


class Epoch(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    previous_epoch = models.ForeignKey("Epoch", on_delete=models.CASCADE, null=True)
    first_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="epochs_as_first_player")
    current_phase = models.CharField(max_length=100, default=Phase.DEVELOPMENT)
    current_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, related_name="epochs_as_current_player"
    )
