from django.db import models
from django.contrib.auth.admin import User

class DeckModel(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decks")
    deck_name   = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f'Usuario:{self.user.username}, Deck:{self.deck_name}'

class CardModel(models.Model):
    deck        = models.ForeignKey(DeckModel, on_delete=models.CASCADE, related_name="cards")
    card_name   = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f'Deck:{self.deck.deck_name} Tarjeta:{self.card_name}'