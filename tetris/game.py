import random
from typing import List

from tetris.actions import TetrisAction
from tetris.constants import *
from tetris.debug import TetrisDebug
from tetris.field import TetrisField
from tetris.input import TetrisInput
from tetris.queue import TetrisQueue
from tetris.view import TetrisView
from tetris.piece import PIECES


class TetrisGame:
    def __init__(self, position=(0, 0), FPS=60, use_view=True):
        self.debug = TetrisDebug(position)
        self.field = TetrisField()
        self.input = TetrisInput()
        self.queue = TetrisQueue()
        self.view = TetrisView(position) if use_view else None

        self.current_piece = self.queue.next_piece()
        self.current_position = (4, 20)
        self.current_orientation = 0

        self.locking_in = True
        self.can_hard_drop = True
        self.can_rotate_l = True
        self.can_rotate_r = True

        self.score = 0

        self.attacking = False
        self.attack = 0

        self.FPS = FPS

        self.drop_frames = FPS
        self.lock_frames = LOCK_IN_FRAMES
        self.lock_resets = 0
        self.shift_frames = 0
        self.delay_auto_shift = True

        self.use_view = use_view
        self.game_over = False

        if self.use_view:
            self.view.redraw(field=self.field, queue=self.queue)
            self.draw_current_piece()

    def _debug_str(self) -> str:
        return "\n".join([
            "Game Over:" + str(self.game_over),
            "Lock Resets: " + str(self.lock_resets),
            "Lock Frames: " + str(self.lock_frames),
            "Locking In: " + str(self.locking_in),
            "Drop Frames: " + str(self.drop_frames),
            "Shift Frames: " + str(self.shift_frames),
            "Delay Auto Shift: " + str(self.delay_auto_shift),
            "Current Position:" + str(self.current_position),
            "Attack:" + str(self.attack),
            "Score:" + str(self.score)
        ])

    def redraw(self):
        if self.use_view:
            self.view.redraw(self.field, self.queue)
            self.draw_current_piece()

    def update(self):
        if self.drop_frames:
            self.drop_frames -= 1
        elif self.locking_in and self.lock_frames:
            self.lock_frames -= 1
        else:
            self.drop_piece()

    def execute_actions(self, actions: Dict[TetrisAction, bool]):
        if actions[TetrisAction.SHIFT_L] and not actions[TetrisAction.SHIFT_R]:
            self.auto_shift_piece(-1)
        elif actions[TetrisAction.SHIFT_R] and not actions[TetrisAction.SHIFT_L]:
            self.auto_shift_piece(1)
        elif not (actions[TetrisAction.SHIFT_L] or actions[TetrisAction.SHIFT_R]):
            self.reset_auto_shift()

        if actions[TetrisAction.DROP_SOFT]:
            self._manage_soft_drop()
        if actions[TetrisAction.DROP_HARD]:
            self.hard_drop()
        else:
            self.can_hard_drop = True

        if actions[TetrisAction.ROT_L]:
            self.rotate_l()
        else:
            self.can_rotate_l = True
        if actions[TetrisAction.ROT_R]:
            self.rotate_r()
        else:
            self.can_rotate_r = True

        if actions[TetrisAction.HOLD]:
            self.hold_piece()

    def spawn_piece(self):
        if self.use_view:
            self.view.redraw(field=self.field, queue=self.queue)

        self.current_position = (4, 20)
        self.current_orientation = 0
        self.current_piece = self.queue.next_piece()
        if self.use_view:
            self.view.draw_queue(self.queue)

        self.locking_in = False
        self.lock_resets = 0
        self.lock_frames = LOCK_IN_FRAMES

        if self.field.test_shape_fit(self.get_current_shape()):
            self.draw_current_piece()
        else:
            self.end_game()

    def end_game(self):
        self.game_over = True
        dead_cells = []
        for row in range(TETRIS_FIELD_ROWS):
            for col in range(TETRIS_FIELD_COLS):
                if self.field.cells[row][col] is not None:
                    dead_cells.append((col, row))

        for cell in self.get_current_shape():
            dead_cells.append(cell)

        if self.use_view:
            self.view.draw_piece(MISC_COLORS["GRAY"], dead_cells)

    def hold_piece(self):
        if self.queue.can_hold_piece:
            self.locking_in = False
            self.lock_resets = 0
            self.lock_frames = LOCK_IN_FRAMES
            next_piece = self.queue.held_piece if self.queue.held_piece is not None else self.queue.next_piece()
            self.queue.held_piece = self.current_piece
            self.queue.can_hold_piece = False
            if self.use_view:
                self.view.draw_queue(self.queue)

            self.erase_current_piece()

            self.current_piece = next_piece
            self.current_position = (4, 20)
            self.current_orientation = 0
            self.locking_in = False

            self.draw_current_piece()

    def get_current_shape(self):
        return PIECES[self.current_piece].centered_on(self.current_position, self.current_orientation)

    def get_offset_shape(self, offset, rotation=0):
        (x, y) = self.current_position
        (x_off, y_off) = offset
        return (
            PIECES[self.current_piece]
            .centered_on(
                (x + x_off, y + y_off),
                (self.current_orientation + rotation) % 4
            )
        )

    def draw_current_piece(self):
        if self.use_view:
            self.view.draw_piece(
                MISC_COLORS["GRAY"],
                self.field.project_down(self.get_current_shape())
            )

            self.view.draw_piece(
                PIECES[self.current_piece].color,
                self.get_current_shape()
            )

    def erase_current_piece(self):
        if self.use_view:
            self.view.draw_piece(
                MISC_COLORS["BLACK"],
                self.field.project_down(self.get_current_shape())
            )

            self.view.draw_piece(
                MISC_COLORS["BLACK"], self.get_current_shape())

    def _manage_soft_drop(self):
        if self.drop_frames <= self.FPS - SOFT_DROP_FRAMES:
            if not self.locking_in:
                self.drop_piece()
            else:
                self.drop_frames = 0

    def lock_in_piece(self):
        try:
            for (sx, sy) in self.get_current_shape():
                self.field.cells[sy][sx] = self.current_piece

            self.locking_in = False
            self.lock_frames = LOCK_IN_FRAMES
            self.lock_resets = 0

            cleared = self.field.clear_rows()

            self.score += [0, 40, 100, 300, 1200][cleared]

            self.attacking = bool(cleared)
            self.attack += [0, 0, 1, 2, 4][cleared]

            self.spawn_piece()
        except IndexError:
            self.end_game()

    def drop_piece(self):
        (px, py) = self.current_position
        next_position = (px, py - 1)

        if self.field.test_shape_fit(self.get_offset_shape((0, -1))):
            self.erase_current_piece()
            self.current_position = next_position
            self.draw_current_piece()

            self.drop_frames = self.FPS

            return True
        elif not self.locking_in:
            self.locking_in = True
            self.lock_frames = LOCK_IN_FRAMES if self.lock_resets < 12 or self.lock_frames == 0 else self.lock_frames
            return False
        else:
            self.lock_in_piece()
            return False

    def hard_drop(self):
        if self.can_hard_drop:
            self.can_hard_drop = False
            self.lock_frames = 0
            self.locking_in = True

            drop_distance = self.field.get_drop_distance(
                self.get_current_shape())
            (x, y) = self.current_position
            self.current_position = (x, y - drop_distance)
            self.lock_in_piece()

            self.drop_frames = self.FPS

    def shift_piece(self, direction: -1 | 1) -> bool:
        if self.field.test_shape_fit(self.get_offset_shape((direction, 0))):
            self.erase_current_piece()
            self.current_position = (
                self.current_position[0] + direction,
                self.current_position[1]
            )
            self.draw_current_piece()
            self.lock_resets += 1 if self.locking_in else 0
            self.locking_in = False

    def auto_shift_piece(self, direction: -1 | 1) -> bool:
        if self.shift_frames:
            self.shift_frames -= 1
        elif self.delay_auto_shift:
            self.delay_auto_shift = False
            self.shift_frames = DAS_FRAMES
            self.shift_piece(direction)
        else:
            self.shift_frames = ASR_FRAMES
            self.shift_piece(direction)

    def reset_auto_shift(self):
        self.shift_frames = 0
        self.delay_auto_shift = True

    def rotate_r(self):
        if self.can_rotate_r:
            self.can_rotate_r = False
            piece = PIECES[self.current_piece]
            if piece.piece_id == "O":
                return

            (x, y) = self.current_position
            kick_table = KICK_TABLE_I if piece.piece_id == "I" else KICK_TABLE_JLSTZ

            for (kx, ky) in kick_table[self.current_orientation]:
                if self.field.test_shape_fit(self.get_offset_shape((kx, ky), 1)):
                    self.lock_resets += 1 if self.locking_in else 0
                    self.locking_in = self.lock_resets >= 12
                    self.erase_current_piece()

                    self.current_position = (x + kx, y + ky)
                    self.current_orientation += 1
                    self.current_orientation %= 4
                    self.draw_current_piece()
                    return

    def rotate_l(self):
        if self.can_rotate_l:
            self.can_rotate_l = False
            piece = PIECES[self.current_piece]
            if piece.piece_id == "O":
                return

            (x, y) = self.current_position
            kick_table = KICK_TABLE_I if piece.piece_id == "I" else KICK_TABLE_JLSTZ

            for (kx, ky) in kick_table[(self.current_orientation-1) % 4]:
                if self.field.test_shape_fit(self.get_offset_shape((-kx, -ky), -1)):
                    self.lock_resets += 1 if self.locking_in else 0
                    self.locking_in = self.lock_resets >= 12
                    self.erase_current_piece()

                    self.current_position = (x - kx, y - ky)
                    self.current_orientation -= 1
                    self.current_orientation %= 4
                    self.draw_current_piece()
                    return

    def garbage(self, lines: int):
        well_col = random.randint(0, TETRIS_FIELD_COLS-1)
        garbage_rows = [[-1 for _ in range(TETRIS_FIELD_COLS)]
                        for _ in range(lines)]
        for row in garbage_rows:
            row[well_col] = None

        drop_distance = self.field.get_drop_distance(self.get_current_shape())
        if drop_distance < lines:
            (x, y) = self.current_position
            y_prime = y + (lines - drop_distance)

            if y_prime >= TETRIS_FIELD_ROWS:
                self.end_game()
                return
            else:
                self.current_position = (x, y_prime)

        self.field.prepend_rows(garbage_rows)

        if self.use_view:
            self.redraw()
