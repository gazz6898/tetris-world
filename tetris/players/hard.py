import random
from tetris.actions import TetrisAction
from tetris.player import TetrisPlayer

#AI Player that favors Hard dropping over other moves. Will probably lose instantly.
class HardPlayer(TetrisPlayer):
    def __init__(self, game):
        super().__init__(game)

    def decide(self):
        actions = {}

        actionList = [TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.SHIFT_L, TetrisAction.SHIFT_R, TetrisAction.DROP_HARD, TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.DROP_HARD,TetrisAction.HOLD]
        
        for action in TetrisAction:
            actions[action] = False
        actions[random.choice(actionList)] = True


        return actions
