import random


class Card:
    def __init__(self):
        self.value = -1

    def draw(self):
        if self.value == -1:
            self.value = random.randint(1, 12)

    def __str__(self):
        if self.value != -1:
            names = ['ACE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'JACK', 'QUEEN', 'KING']

            return names[self.value-1]
        
        raise Exception('temp exeption')

    def __repr__(self):
        return self.__str__()


def draw():
    card = Card()

    card.draw()

    return card
