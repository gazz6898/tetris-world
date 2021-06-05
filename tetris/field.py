from functools import reduce
import math
from typing import List, Tuple

import tetris.util as util
from tetris.constants import *
from tetris.piece import PIECES


class TetrisField:
    def __init__(self):
        self.cells = [
            [None] * TETRIS_FIELD_COLS for _ in range(TETRIS_FIELD_ROWS)]

    def test_cell_fit(self, coords: Tuple[int, int]) -> bool:
        (x, y) = coords
        return (util.has_index(self.cells, y)
                and util.has_index(self.cells[y], x)
                and self.cells[y][x] is None)

    def test_shape_fit(self, shape: List[Tuple[int, int]]) -> bool:
        return all(map(self.test_cell_fit, shape))

    def get_drop_distance(self, shape: List[Tuple[int, int]]) -> int:
        cols = {}
        for (col, row) in shape:
            cols[col] = min(row, cols[col]) if cols.__contains__(col) else row

        dy = 999
        for col in cols:
            c_dy = 0
            while self.test_cell_fit((col, cols[col] - c_dy)):
                c_dy += 1
            if c_dy < dy:
                dy = c_dy

        return dy - 1

    def project_down(self, shape: List[Tuple[int, int]]):
        dy = self.get_drop_distance(shape)
        return [(x, y - dy) for (x, y) in shape]

    def clear_rows(self):
        cleared = []
        for row in range(TETRIS_FIELD_ROWS):
            col = 0
            while col < TETRIS_FIELD_COLS:
                if self.cells[row][col] is None:
                    break
                col += 1
            if col == TETRIS_FIELD_COLS:
                cleared.append(row)

        for row in reversed(cleared):
            self.cells.pop(row)
            self.cells.append([None] * TETRIS_FIELD_COLS)

    def prepend_rows(self, rows: List[List[int]]):
        for row in reversed(rows):
            self.cells.insert(0, row[0:TETRIS_FIELD_COLS])

        self.cells = self.cells[0:TETRIS_FIELD_ROWS]
