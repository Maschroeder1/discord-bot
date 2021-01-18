import time
from .player import Player
from .dealer import Dealer

# todo: finish games
# todo: deal with up to N aces
# todo: deck system

TIMEOUT = 300


def calculate_points(cards):  # this smells, not sure where to put it though
    points = 0

    for card in cards:
        if card.value < 10:
            points += card.value
        else:
            points += 10

    return points


class Blackjack:
    def __init__(self):
        self.users_timeout = dict()
        self.players = dict()
        self.dealers = dict()

    async def play(self, msg, args):
        player = msg.author
        misc = {'command': args[0]}

        if self.has_playable_game(player):
            await self.continue_game(player, msg, misc)
        else:
            await self.new_game(player, msg)

    def has_playable_game(self, player):
        return player in self.users_timeout and self.users_timeout[player] - time.time() < TIMEOUT

    async def continue_game(self, player_name, msg, misc):
        player = self.players[player_name]
        dealer = self.dealers[player_name]

        await player.play_turn(msg, misc)
        await self.post_player_gamestate(player_name, msg)

        if self.has_playable_game(player_name):
            await dealer.play_turn(msg, {'points': calculate_points(dealer.get_cards())})
            await self.post_dealer_gamestate(player_name, msg)

    async def new_game(self, player, msg):
        await msg.channel.send(f'Starting new game for player {player}')

        self.users_timeout[player] = time.time()
        self.players[player] = Player(player)
        self.dealers[player] = Dealer(player)

        await self.post_player_gamestate(player, msg)
        await self.post_dealer_gamestate(player, msg)

    async def post_player_gamestate(self, player_name, msg):
        player = self.players[player_name]
        player_points = calculate_points(player.get_cards())
        player_state = player.build_message(player_points)

        await msg.channel.send(player_state)

        if player_points > 21:
            await msg.channel.send(f'@{player_name} busted! Dealer wins!')
            self.end_game(player_name)

    async def post_dealer_gamestate(self, player, msg):
        dealer = self.dealers[player]
        dealer_points = calculate_points(dealer.get_cards())
        dealer_state = dealer.build_message(dealer_points)

        await msg.channel.send(dealer_state)

        if dealer_points > 21:
            await msg.channel.send(f"Dealer busted! @{player} wins!")
            self.end_game(player)

    def end_game(self, player):
        del self.users_timeout[player]
        del self.players[player]
        del self.dealers[player]
