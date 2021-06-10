import random
from tetris.actions import TetrisAction
from tetris.player import TetrisPlayer

#AI Player that favors soft dropping over other moves.
class SoftPlayer(TetrisPlayer):
    def __init__(self, game):
        super().__init__(game)

    def decide(self):
        actions = {}

        actionList = [TetrisAction.ROT_L, TetrisAction.ROT_R, TetrisAction.SHIFT_L, TetrisAction.SHIFT_R, TetrisAction.DROP_SOFT, TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.DROP_SOFT,TetrisAction.HOLD]
        
        for action in TetrisAction:
            actions[action] = False
        actions[random.choice(actionList)] = True


        return actions
