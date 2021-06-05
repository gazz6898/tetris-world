from __future__ import annotations
from typing import Tuple, List

from tetris.constants import PIECE_COLORS
import tetris.util as util


class TetrisPiece:
    def __init__(self,
                 piece_id: str,
                 color: Tuple[int, int, int],
                 shape: List[Tuple[float, float]],
                 center: Tuple[float, float] = (0, 0),
                 ):
        self.piece_id = piece_id
        self.color = color
        self.center = center
        self.orientations = [
            list(map(rotation, shape))
            for rotation in [util.rot0, util.rot90, util.rot180, util.rot270]
        ]

    def centered_on(self, new_center: Tuple[float, float], orientation: 0 | 1 | 2 | 3 = 0) -> List[Tuple[int, int]]:
        (x, y) = new_center
        (x_off, y_off) = self.center
        return [(int(sx + x + x_off), int(sy + y + y_off))
                for (sx, sy) in self.orientations[orientation]
                ]


PIECES = [
    # Z-piece
    TetrisPiece("Z",
                PIECE_COLORS["RED"],
                [(-1, 1), (0, 1), (0, 0), (1, 0)]
                ),
    # L-piece
    TetrisPiece("L",
                PIECE_COLORS["ORANGE"],
                [(-1, 0), (0, 0), (1, 0), (1, 1)]
                ),
    # O-piece
    TetrisPiece("O",
                PIECE_COLORS["YELLOW"],
                [(0.5, 0.5), (0.5, -0.5), (-0.5, -0.5), (-0.5, 0.5)],
                (0.5, -0.5)
                ),
    # S-piece
    TetrisPiece("S",
                PIECE_COLORS["GREEN"],
                [(-1, 0), (0, 0), (0, 1), (1, 1)]
                ),
    # I-piece
    TetrisPiece("I",
                PIECE_COLORS["CYAN"],
                [(-1.5, 0.5), (-0.5, 0.5), (0.5, 0.5), (1.5, 0.5)],
                (0.5, -0.5)
                ),
    # J-piece
    TetrisPiece("J",
                PIECE_COLORS["BLUE"],
                [(-1, 1), (-1, 0), (0, 0), (1, 0)]
                ),
    # T-piece
    TetrisPiece("T",
                PIECE_COLORS["VIOLET"],
                [(-1, 0), (0, 0), (0, 1), (1, 0)]
                ),
]
