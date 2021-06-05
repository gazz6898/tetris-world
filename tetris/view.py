from functools import reduce
from tetris.queue import TetrisQueue
from typing import List, Tuple

import pygame
from pygame import Color, Rect, Surface
from pygame import math
from pygame.sprite import Sprite

from tetris.constants import *
from tetris.piece import PIECES, TetrisPiece


class TetrisView(Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.dimensions = (TETRIS_FIELD_COLS * TILE_SIZE + 1,
                           TETRIS_FIELD_ROWS * TILE_SIZE + 1)

        self.cell_surface = None
        self.cell_rect = None

        self.grid_surface = None
        self.grid_rect = None

        self.held_surface = None
        self.held_rect = None

        self.queue_surfaces = [None for _ in range(PIECE_PREVIEWS)]
        self.queue_rects = [None for _ in range(PIECE_PREVIEWS)]

        self.init_surfaces()

    def init_surfaces(self):
        (x, y) = self.position
        (w, h) = self.dimensions

        self.cell_surface = Surface((TETRIS_FIELD_COLS * TILE_SIZE + 1,
                                     TETRIS_FIELD_ROWS * TILE_SIZE + 1), pygame.SRCALPHA)
        self.cell_rect = self.cell_surface.get_rect(
            center=(x + w / 2 + 5 * TILE_SIZE,
                    y + h / 2 + TILE_SIZE)
        )

        self.cell_surface.fill(MISC_COLORS["BLACK"])

        self.grid_surface = Surface((TETRIS_FIELD_COLS * TILE_SIZE + 1,
                                     TETRIS_FIELD_ROWS * TILE_SIZE + 1), pygame.SRCALPHA)
        self.grid_rect = self.grid_surface.get_rect(
            center=(x + w / 2 + 5 * TILE_SIZE,
                    y + h / 2 + TILE_SIZE)
        )

        HELD_SURFACE_SIZE = (3 * TILE_SIZE + 1, 3 * TILE_SIZE + 1)
        HELD_RECT_SIZE = (3 * TILE_SIZE, 3 * TILE_SIZE)
        RECT_X = (5 * TILE_SIZE / 2)
        RECT_Y = (9 * TILE_SIZE / 2)

        self.held_surface = Surface(HELD_SURFACE_SIZE, pygame.SRCALPHA)
        self.held_rect = self.held_surface.get_rect(
            center=(x + RECT_X, y + RECT_Y))

        pygame.draw.rect(
            self.held_surface,
            MISC_COLORS["WHITE"],
            Rect((0, 0), HELD_RECT_SIZE),
            1
        )

        for i in range(PIECE_PREVIEWS):
            surface_i = Surface(HELD_SURFACE_SIZE, pygame.SRCALPHA)
            self.queue_surfaces[i] = surface_i
            self.queue_rects[i] = surface_i.get_rect(
                center=(x + RECT_X + (5 + TETRIS_FIELD_COLS) * TILE_SIZE,
                        y + RECT_Y + i * 4 * TILE_SIZE)
            )
            surface_i.fill(MISC_COLORS["BLACK"])
            pygame.draw.rect(
                surface_i,
                MISC_COLORS["WHITE"],
                Rect((0, 0), HELD_RECT_SIZE),
                1
            )

    def redraw(self, field, queue):
        self.draw_field(field)
        self.draw_grid()
        self.draw_queue(queue)

    def draw_grid(self):
        x_offsets = [i * TILE_SIZE for i in range(TETRIS_FIELD_COLS + 1)]
        y_offsets = [j * TILE_SIZE for j in range(2, TETRIS_FIELD_ROWS + 1)]

        for x_offset in x_offsets:
            pygame.draw.aaline(
                self.grid_surface, MISC_COLORS["WHITE"], (x_offset, y_offsets[0]), (x_offset, y_offsets[-1]))

        for y_offset in y_offsets:
            pygame.draw.aaline(
                self.grid_surface, MISC_COLORS["WHITE"], (0, y_offset), (x_offsets[-1], y_offset))

    def draw_field(self, field):
        self.cell_surface.fill(MISC_COLORS["BLACK"])

        for i in range(TETRIS_FIELD_ROWS):
            for j in range(TETRIS_FIELD_COLS):
                if field.cells[i][j] is not None:
                    pygame.draw.rect(
                        self.cell_surface,
                        PIECES[field.cells[i][j]].color if (field.cells[i][j] != -1)
                        else MISC_COLORS["GRAY"],
                        Rect(
                            (j * TILE_SIZE,
                             (TETRIS_FIELD_ROWS - 1 - i) * TILE_SIZE),
                            (TILE_SIZE, TILE_SIZE)
                        )
                    )

    def draw_piece(self, color: Tuple[int, int, int], shape: List[Tuple[int, int]]) -> None:
        for (x, y) in shape:
            pygame.draw.rect(
                self.cell_surface,
                color,
                Rect(
                    (x * TILE_SIZE,
                     (TETRIS_FIELD_ROWS - y - 1) * TILE_SIZE
                     ),
                    (TILE_SIZE, TILE_SIZE)
                )
            )

    def draw_queue(self, queue: TetrisQueue):
        def draw_piece(surface, piece: TetrisPiece, color_override=None):
            shape = piece.orientations[0]
            for (x, y) in shape:
                pygame.draw.rect(
                    surface,
                    color_override if color_override is not None else piece.color,
                    Rect(
                        (x * (TILE_SIZE / 2) + 1.25 * TILE_SIZE,
                         -y * (TILE_SIZE / 2) + 1.25 * TILE_SIZE
                         ),
                        (TILE_SIZE / 2, TILE_SIZE / 2)
                    )
                )

        if queue.held_piece is not None:
            self.held_surface.fill(MISC_COLORS["BLACK"])
            pygame.draw.rect(
                self.held_surface,
                MISC_COLORS["WHITE"],
                Rect((0, 0), (3 * TILE_SIZE, 3 * TILE_SIZE)),
                1
            )
            draw_piece(
                self.held_surface, PIECES[queue.held_piece], None if queue.can_hold_piece else MISC_COLORS["GRAY"])

        for i in range(PIECE_PREVIEWS):
            surface_i = self.queue_surfaces[i]
            surface_i.fill(MISC_COLORS["BLACK"])
            pygame.draw.rect(
                surface_i,
                MISC_COLORS["WHITE"],
                Rect((0, 0), (3 * TILE_SIZE, 3 * TILE_SIZE)),
                1
            )

            p = queue.piece_queue[i]
            draw_piece(surface_i, PIECES[p])
