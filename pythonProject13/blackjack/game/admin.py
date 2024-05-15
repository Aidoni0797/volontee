from django.contrib import admin
from .models import Player, Card, Deck, CardGame


@admin.register(Player)
class Player(admin.ModelAdmin):
    player = ['player']

@admin.register(Card)
class Card(admin.ModelAdmin):
    list_display = ['ranks', 'handed_out']
    list_editable = ['handed_out']

@admin.register(Deck)
class Deck(admin.ModelAdmin):
    deck = ['card_id']

@admin.register(CardGame)
class CardGame(admin.ModelAdmin):
    CardGame = ['user', 'deck']


