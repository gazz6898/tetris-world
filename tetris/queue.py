import random

import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite

from tetris.constants import *
from tetris.piece import PIECES, TetrisPiece


class TetrisQueue(Sprite):
    def __init__(self):
        super().__init__()
        self.position = (TILE_SIZE, 3 * TILE_SIZE)
        self.dimensions = ((TETRIS_FIELD_COLS + 6) * TILE_SIZE,
                           4 * PIECE_PREVIEWS * TILE_SIZE + 1)

        self.piece_queue = []
        self.held_piece = None
        self.add_bag_to_queue()
        self.add_bag_to_queue()

        self.can_hold_piece = True

    def add_bag_to_queue(self):
        bag = [i for i in range(7)]
        random.shuffle(bag)
        self.piece_queue.extend(bag)

    def next_piece(self):
        if len(self.piece_queue) <= PIECE_PREVIEWS:
            self.add_bag_to_queue()
        piece = self.piece_queue.pop(0)
        self.can_hold_piece = True
        return piece
