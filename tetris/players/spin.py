import random
from tetris.actions import TetrisAction
from tetris.player import TetrisPlayer

#AI Player that favors rotating over other moves
class SpinPlayer(TetrisPlayer):
    def __init__(self, game):
        super().__init__(game)

    def decide(self):
        actions = {}

        actionList = [TetrisAction.SHIFT_L, TetrisAction.SHIFT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.DROP_SOFT, TetrisAction.HOLD]
        for action in TetrisAction:
            actions[action] = False
        actions[random.choice(actionList)] = True


        return actions
