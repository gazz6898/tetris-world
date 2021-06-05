from typing import Dict, Tuple

TETRIS_FIELD_ROWS: int = 22
TETRIS_FIELD_COLS: int = 10

TILE_SIZE: int = 24

ASR_FRAMES: int = 4
DAS_FRAMES: int = 12

SOFT_DROP_FRAMES: int = 6
LOCK_IN_FRAMES: int = 16

MISC_COLORS: Dict[str, Tuple[int, int, int]] = {
    "BLACK": (0, 0, 0),
    "GRAY": (180, 180, 180),
    "WHITE": (255, 255, 255)
}

PIECE_COLORS: Dict[str, Tuple[int, int, int]] = {
    "RED": (215, 15, 55),
    "ORANGE": (225, 90, 5),
    "YELLOW": (225, 160, 5),
    "GREEN": (90, 180, 0),
    "CYAN": (15, 155, 215),
    "BLUE": (30, 70, 200),
    "VIOLET": (175, 40, 140)
}
PIECE_PREVIEWS = 5

KICK_TABLE_JLSTZ = [
    [(0, 0), (-1, 0), (-1,  1), (0, -2), (-1, -2)],
    [(0, 0), (1, 0), (1, -1), (0,  2), (1,  2)],
    [(0, 0), (1, 0), (1,  1), (0, -2), (1, -2)],
    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
]

KICK_TABLE_I = [
    [(0, 0), (-2, 0), (1,  0), (-2, -1), (1, 2)],
    [(0, 0),	(-1, 0)	, (2, 0),	(-1, 2),	(2, -1)],
    [(0, 0),	(2, 0),	(-1, 0),	(2, 1),	(-1, -2)],
    [(0, 0),	(1, 0),	(-2, 0),	(1, -2),	(-2, 1)]
]
