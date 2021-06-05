from enum import Enum


class TetrisAction(Enum):
    SHIFT_L = 1
    SHIFT_R = 2
    ROT_L = 3
    ROT_R = 4
    DROP_SOFT = 5
    DROP_HARD = 6
    HOLD = 7
