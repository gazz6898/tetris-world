import random

import pygame
import pygame.font
from pygame import Rect, Surface
from pygame.sprite import Sprite

from tetris.constants import *


class TetrisDebug(Sprite):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = (position[0] + (TETRIS_FIELD_COLS + 10) * TILE_SIZE,
                         position[1] + TILE_SIZE / 2)
        self.dimensions = (10 * TILE_SIZE +
                           1, TETRIS_FIELD_ROWS * TILE_SIZE)

        self.data = None
        fonts = pygame.font.get_fonts()
        sysfont_name = pygame.font.get_default_font()
        self.sysfont = pygame.font.SysFont('jetbrainsmono', 12)

        self.surface = None
        self.rect = None

        self.init_surfaces()

    def init_surfaces(self):
        (x, y) = self.position
        (w, h) = self.dimensions

        self.surface = Surface(
            (w, h), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(x + w/2, y + h/2))

        pygame.draw.rect(
            self.surface,
            MISC_COLORS["WHITE"],
            Rect((0, 0), (w - 1, h - 1)),
            1
        )

    def draw_surfaces(self):
        (x, y) = self.position
        (w, h) = self.dimensions
        self.surface.fill(MISC_COLORS["BLACK"])
        pygame.draw.rect(
            self.surface,
            MISC_COLORS["WHITE"],
            Rect((0, 0), (w - 1, h - 1)),
            1
        )
        l = 0
        data_lines = self.data.splitlines()
        num_lines = len(data_lines)
        for ln in data_lines:
            img = self.sysfont.render(
                ln, True, MISC_COLORS["WHITE"], MISC_COLORS["BLACK"])
            rect = img.get_rect(
                center=(w / 2, (h / 2) + (num_lines / 2 - l) * self.sysfont.get_height()))
            self.surface.blit(img, rect, Rect((0, 0), (w, h)))
            l += 1
