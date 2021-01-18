import discord
import time
import random
from ..cards.cards import Card

#todo: finish games
#todo: deal with up to N aces
#todo: deck system
#todo: extract player and dealer classes

TIMEOUT = 300

class Blackjack:
    def __init__(self):
        self.users_timeout = dict()
        self.users_hands = dict()
        self.dealer_hands = dict()


    async def play(self, args, msg):
        player = msg.author

        if self.has_playable_game(player):
            await self.continue_game(player, args, msg)
        else:
            await self.new_game(player, msg)


    def has_playable_game(self, player):
        return player in self.users_timeout and self.users_timeout[player] - time.time() < TIMEOUT


    async def continue_game(self, player, args, msg):
        await self.play_player_turn(player, args, msg)
        await self.update_player_gamestate(player, msg)

        if self.has_playable_game(player):
            await self.play_dealer_turn(player, msg)
            await self.update_dealer_gamestate(player, msg)
            

    async def play_player_turn(self, player, args, msg):
        if args.startswith('hit'):
            self.player_draw_card(player)
        elif args.startswith('stand'):
            await msg.channel.send("{player} decided to not draw any cards".format(player=player))
        else:
            await msg.channel.send('You must either hit or stand')


    async def play_dealer_turn(self, player, msg):
        if self.dealer_points(player) < 17:
            self.dealer_draw_card(player)
            await msg.channel.send("@{player}'s dealer hit".format(player=player))
        else:
            await msg.channel.send("@{player}'s dealer stood".format(player=player))


    async def new_game(self, player, msg):
        await msg.channel.send('Starting new game for player {player}'.format(player=player))

        self.users_timeout[player] = time.time()
        self.users_hands[player] = []
        self.dealer_hands[player] = []

        self.draw_initial_cards(player)
        await self.update_player_gamestate(player, msg)
        await self.update_dealer_gamestate(player, msg)


    def draw_initial_cards(self, player):
        self.player_draw_card(player)
        self.player_draw_card(player)

        self.dealer_draw_card(player)
        self.dealer_draw_card(player)


    async def update_player_gamestate(self, player, msg):
        player_points = self.player_points(player)
        player_state = self.build_player_message(player, player_points)

        await msg.channel.send(player_state)

        if player_points > 21:
            await msg.channel.send('@{player} busted! Dealer wins!'.format(player=player))
            self.end_game(player)


    async def update_dealer_gamestate(self, player, msg):
        dealer_points = self.dealer_points(player)
        dealer_state = self.build_dealer_message(player, dealer_points)

        await msg.channel.send(dealer_state)

        if dealer_points > 21:
            await msg.channel.send("Dealer busted! @{player} wins!".format(player=player))
            self.end_game(player)


    def end_game(self, player):
        del self.users_timeout[player]
        del self.users_hands[player]
        del self.dealer_hands[player]


    def build_player_message(self, player, points):
        return "@{player_name} has {player_cards}, with a sum of {player_points}".format(player_name=player, player_cards=self.users_hands[player], player_points=points)
    

    def player_points(self, player):
        return self.calculate_points(self.users_hands[player])


    def build_dealer_message(self, player, points):
        return "@{player_name}'s dealer has {dealer_cards}, with a sum of {dealer_points}".format(player_name=player, dealer_cards=self.dealer_hands[player], dealer_points=points)


    def dealer_points(self, player):
        return self.calculate_points(self.dealer_hands[player])
    

    def calculate_points(self, hand):
        points = 0

        for card in hand:
            if card.value < 10:
                points += card.value
            else:
                points += 10

        return points


    def player_draw_card(self, player):
        self.users_hands[player].append(self.draw_card())
    

    def dealer_draw_card(self, player):
        self.dealer_hands[player].append(self.draw_card())


    def draw_card(self):
        card = Card()

        card.draw()

        return card