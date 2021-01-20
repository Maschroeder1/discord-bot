from .player import Player


class Dealer(Player):
    async def play_turn(self, msg, misc):
        points = self.get_points()

        while max(points) < 17:
            self.draw_card()
            await msg.channel.send(f"@{self._name}'s dealer drew a {self._cards[-1]}")
            points = self.get_points()

        await msg.channel.send(f"@{self._name}'s dealer stood")
        self._is_finished = True

    def build_message(self):
        return f"@{self._name}'s dealer has {self._cards}, with a sum of {max(self.get_points())}"
