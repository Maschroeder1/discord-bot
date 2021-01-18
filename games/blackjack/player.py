from ..cards.cards import draw


class Player:
    def __init__(self, name):
        self._name = name
        self._cards = []

        self.draw_card()
        self.draw_card()

    def get_cards(self):
        return self._cards

    def draw_card(self):
        card = draw()

        self._cards.append(card)

    async def play_turn(self, msg, misc):
        command = misc['command']

        if command.startswith('hit'):
            self.draw_card()
        elif command.startswith('stand'):
            await msg.channel.send(f"{self._name} decided to not draw any cards")
        else:
            await msg.channel.send('You must either hit or stand')
    
    def build_message(self, points):
        return f"@{self._name} has {self._cards}, with a sum of {points}"
