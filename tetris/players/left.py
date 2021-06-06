from tetris.actions import TetrisAction
from tetris.player import TetrisPlayer

class LeftPlayer(TetrisPlayer):
    def __init__(self, game):
        super().__init__(game)

    def decide(self):
        actions = {}

        for action in TetrisAction:
            actions[action] = False

        actions[TetrisAction.SHIFT_L] = True

        return actions