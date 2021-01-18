from games.blackjack.blackjack import Blackjack
#todo: extract game to its own class
#todo: add music commands

GAME = 'play '

class Commands:
    def __init__(self):
        print('initializing commands')
        self.blackjack = Blackjack()


    async def command(self, command, msg):
        if command.startswith(GAME):
            await self.play_game(command[len(GAME):], msg)
        else:
            await msg.channel.send("Unknown command")
        
        print(command)


    async def play_game(self, game, msg):
        if 'blackjack' in game:
            aux = await self.blackjack.play(game[len('blackjack')+1:], msg)
        else:
            await msg.channel.send("Unknown game")
            return