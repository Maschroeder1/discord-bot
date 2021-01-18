from .player import Player


class Dealer(Player):
    async def play_turn(self, msg, misc):
        points = misc['points']

        while points < 17:
            self.draw_card()
            await msg.channel.send(f"@{self._name}'s dealer drew a @{self._cards[-1]}")
        
        await msg.channel.send(f"@{self._name}'s dealer stood")

    def build_message(self, points):
        return f"@{self._name}'s dealer has {self._cards}, with a sum of {points}"
