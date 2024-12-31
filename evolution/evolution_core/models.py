from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    is_first_player = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    epoch = models.IntegerField(default=1)  # Current Epoch (1-6)
    max_epochs = models.IntegerField(default=6)
    players = models.ManyToManyField(Player, through="PlayerGame")

    def __str__(self):
        return f"Game {self.id} - Epoch {self.epoch}"


class PlayerGame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hand = models.JSONField(default=list)  # Stores cards in hand as a list of card IDs
    order = models.IntegerField()  # Turn order for this player


class Area(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tokens_food = models.IntegerField(default=0)
    tokens_shelter = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    special_effects = models.JSONField(
        default=dict
    )  # e.g., {'swamp': True, 'bonus_food': 2}

    def __str__(self):
        return (
            f"Area {self.id} - Food: {self.tokens_food}, Shelter: {self.tokens_shelter}"
        )


class Trait(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    increases_food_requirement = models.IntegerField(default=0)  # +1, +2, etc.
    is_paired = models.BooleanField(default=False)  # For paired traits
    victory_points = models.IntegerField(default=0)  # Points awarded for this trait
    triggered_effects = models.JSONField(
        default=dict
    )  # Key-value pairs for effects and conditions
    priority = models.IntegerField(default=0)  # Higher priority overrides basic rules

    def __str__(self):
        return self.name


class Animal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    food_requirement = models.IntegerField(default=1)
    food_tokens = models.IntegerField(default=0)
    fat_tokens = models.IntegerField(default=0)
    shelter = models.BooleanField(default=False)
    traits = models.ManyToManyField(
        Trait,
        through="AnimalTrait",
        through_fields=("animal", "trait"),  # Explicitly specify the fields
    )
    is_alive = models.BooleanField(default=True)
    victory_points = models.IntegerField(default=0)

    def __str__(self):
        return f"Animal {self.id} - Player: {self.player.user.username}, Food: {self.food_tokens}/{self.food_requirement}"


class AnimalTrait(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    paired_animal = models.ForeignKey(
        Animal,
        null=True,
        blank=True,
        related_name="paired_trait",
        on_delete=models.SET_NULL,
    )
    is_rotated = models.BooleanField(
        default=False
    )  # Rotated after attacking or additional action

    def __str__(self):
        return f"{self.trait.name} on {self.animal.id}"


class Card(models.Model):
    name = models.CharField(max_length=100)
    main_trait = models.ForeignKey(
        Trait, on_delete=models.CASCADE, related_name="main_trait"
    )
    short_trait = models.ForeignKey(
        Trait, on_delete=models.CASCADE, related_name="short_trait"
    )
    STATE_CHOICES = [
        ("deck", "In Deck"),
        ("hand", "In Hand"),
        ("played", "Played"),
        ("discarded", "Discarded"),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="deck")

    def __str__(self):
        return self.name


class Deck(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    cards = models.JSONField(default=list)  # List of card IDs

    def __str__(self):
        return f"Deck for Game {self.game.id}"


class TokenSupply(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    food_tokens = models.IntegerField(default=100)
    fat_tokens = models.IntegerField(default=100)
    shelter_tokens = models.IntegerField(default=100)

    def __str__(self):
        return f"Token Supply - Game {self.game.id}"


class GamePhase(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    phase_name = models.CharField(
        max_length=50
    )  # Development, Areas, Feeding, Extinction
    current_player = models.ForeignKey(
        Player, null=True, blank=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Phase: {self.phase_name} - Game {self.game.id}"


class ActionLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, null=True, blank=True, on_delete=models.SET_NULL)
    action_type = models.CharField(max_length=50)  # e.g., Feed, Attack, Search Shelter
    target_animal = models.ForeignKey(
        Animal,
        null=True,
        blank=True,
        related_name="targeted_actions",
        on_delete=models.SET_NULL,
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class EpochLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    epoch = models.IntegerField()
    log = models.TextField()

    def __str__(self):
        return f"Epoch {self.epoch} Log - Game {self.game.id}"


class FinalScore(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.player.user.username} - {self.score} points"
