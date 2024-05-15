from django.db import models
from django.contrib.auth.models import User
import random

class Player(models.Model):
    first_name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

class Card(models.Model):
    ranks = (("two", 2), ("three", 3), ("four", 4), ("five", 5), ("six", 6),
             ("seven", 7), ("eight", 8), ("nine", 9), ("ten", 10), ("J", 10),
             ("Q", 10), ("K", 10), ("A", 10))
    suits = (("spades", "spades"), ("clubs", "clubs"), ("hearts", "hearts"), ("diamonds", "diamonds"))
    cards_suits = models.CharField(choices=suits, max_length=15)
    cards_ranks = models.CharField(choices=ranks, max_length=15)
    handed_out = models.BooleanField(default=False)


class Deck(models.Model):
    cards = models.ManyToManyField(Card)


class CardGame(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    def hit(self):
        cards = self.deck.cards.filter(handed_out=False)
        player_card_1 = random.choice(cards)
        player_card_1.handed_out = True
        player_card_1.save()
        player_card_2 = random.choice(cards)
        player_card_2.handed_out = True
        player_card_2.save()
        dealer_card_1 = random.choice(cards)
        dealer_card_1.handed_out = True
        dealer_card_1.save()
        dealer_card_2 = random.choice(cards)
        dealer_card_2.handed_out = True
        dealer_card_2.save()
        return player_card_1.cards_suits, player_card_1.cards_ranks, player_card_2.cards_suits, player_card_2.cards_ranks, dealer_card_1.cards_suits, dealer_card_1.cards_ranks, dealer_card_2.cards_suits, dealer_card_2.cards_ranks

    def add_hit(self):
        cards = self.deck.cards.filter(handed_out=False)
        player_card_1 = random.choice(cards)
        player_card_1.handed_out = True
        player_card_1.save()
        return player_card_1.cards_suits, player_card_1.cards_ranks



