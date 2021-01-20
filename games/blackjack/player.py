from ..cards.cards import draw


def calculate_points(cards):  # this smells, not sure where to put it though
    points = 0

    for card in cards:
        if card.value < 10:
            points += card.value
        else:
            points += 10

    return points


class Player:
    def __init__(self, name):
        self._name = name
        self._cards = []
        self._is_finished = False

        self.draw_card()
        self.draw_card()

    def get_cards(self):
        return self._cards

    def is_finished(self):
        return self._is_finished

    def get_name(self):
        return self._name

    def draw_card(self):
        card = draw()

        self._cards.append(card)

    async def play_turn(self, msg, misc):
        if 'command' in misc:
            await self.do_play_turn(msg, misc['command'])
        else:
            await msg.channel.send('You must either hit or stand')

    async def do_play_turn(self, msg, command):
        if command.startswith('hit'):
            self.draw_card()
            await msg.channel.send(f"@{self._name} drew a {self._cards[-1]}")
        elif command.startswith('stand'):
            await msg.channel.send(f"{self._name} decided to not draw any more cards")
            self._is_finished = True

    def build_message(self, points):
        return f"@{self._name} has {self._cards}, with a sum of {points}"
