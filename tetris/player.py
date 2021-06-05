from typing import Dict

from tetris.actions import TetrisAction
from tetris.game import TetrisGame


class TetrisPlayer:
    def __init__(self, game: TetrisGame):
        self.game = game

    def decide(self) -> Dict[TetrisAction, bool]:
        actions = {}

        for action in TetrisAction:
            actions[action] = False

        return actions
