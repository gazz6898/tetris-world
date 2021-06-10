import random

from tetris.actions import TetrisAction
from tetris.player import TetrisPlayer

#AI player that equally does everything except hard drop
class RandomPlayer(TetrisPlayer):
    def __init__(self, game):
        super().__init__(game)

    def decide(self):
        actions = {}

        for action in TetrisAction:
            actions[action] = False
        actions[
            random.choice(
                [action for action in TetrisAction if action != TetrisAction.DROP_HARD]
            )
        ] = True

        return actions
