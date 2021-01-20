import discord
from commands import Commands

# todo: add moderation

COMMAND = 'hey bot '


class Events:
    def __init__(self, token):
        print('initializing events')

        self.client = discord.Client()
        self.declare_events()
        self.commands = Commands()
        self.client.run(token)

    def declare_events(self):
        @self.client.event
        async def on_ready():
            print(f'{self.client.user} is ready')

        @self.client.event
        async def on_message(msg):
            if msg.content.startswith(COMMAND):
                await self.commands.command(msg.content[len(COMMAND):], msg)
