from ..cards.cards import draw


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

    def busted(self):
        points = self.get_points()

        return len([x for x in points if x <= 21]) == 0

    def get_points(self):  # this smells, not sure where to put it though
        points = [0]

        for card in self._cards:
            if card.is_face():
                points = [x + 10 for x in points]
            elif card.is_ace():
                points = [x + 1 for x in points] + [x + 10 for x in points]
            else:
                points = [x + card.value for x in points]

        return points

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

    def build_message(self):
        if self.busted():
            points = [str(x) for x in self.get_points()]
            points.sort()
            points_string = " or ".join(points)
        else:
            points = [str(x) for x in self.get_points() if x <= 21]
            points.sort()
            points_string = " or ".join(points)

        return f"@{self._name} has {self._cards}, with a sum of {points_string}"
