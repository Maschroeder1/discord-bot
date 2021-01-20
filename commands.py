from games.blackjack.blackjack import Blackjack
# todo: extract game to its own class
# todo: add music commands

GAME = 'play'


class Commands:
    def __init__(self):
        print('initializing commands')
        self.blackjack = Blackjack()

    async def command(self, command, msg):
        command_as_array = command.split()

        if command_as_array[0].lower() == GAME:
            await self.play_game(command_as_array[1:], msg)
        else:
            await msg.channel.send("Unknown command")

    async def play_game(self, game, msg):
        if game[0].lower() == 'blackjack':
            await self.blackjack.play(msg, game[1:])
        else:
            await msg.channel.send("Unknown game")
