from types import FunctionType
from typing import Any, Callable, Dict

import sys

import pygame
import pygame.display
import pygame.event
import pygame.time
import pygame.sprite
from pygame.locals import *

from tetris.actions import TetrisAction
from tetris.constants import *
from tetris.game import TetrisGame

from global_constants import *

pygame.init()

tetris_game_1 = TetrisGame(position=(TILE_SIZE, 0), FPS=FPS)
keymap_1 = {
    TetrisAction.SHIFT_L: K_LEFT,
    TetrisAction.SHIFT_R: K_RIGHT,
    TetrisAction.ROT_L: K_z,
    TetrisAction.ROT_R: K_UP,
    TetrisAction.DROP_SOFT: K_DOWN,
    TetrisAction.DROP_HARD: K_SPACE,
    TetrisAction.HOLD: K_c
}

keymap_2 = {
    TetrisAction.SHIFT_L: K_a,
    TetrisAction.SHIFT_R: K_d,
    TetrisAction.ROT_L: K_q,
    TetrisAction.ROT_R: K_w,
    TetrisAction.DROP_SOFT: K_s,
    TetrisAction.DROP_HARD: K_f,
    TetrisAction.HOLD: K_c
}
tetris_game_2 = TetrisGame(position=(32 * TILE_SIZE, 0), FPS=FPS)


def main() -> None:
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Tetris World")

    all_sprites = pygame.sprite.Group()
    all_sprites.add(tetris_game_1.view,
                    tetris_game_1.debug)
    all_sprites.add(tetris_game_2.view,
                    tetris_game_2.debug)

    while True:
        displaysurface.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                for (tetris_game, garbage_key) in [(tetris_game_1, K_1), (tetris_game_2, K_2)]:
                    if event.type == KEYDOWN and not tetris_game.game_over:
                        tetris_game.input.handle_keydown_event(event.key)
                        if event.key == garbage_key:
                            tetris_game.garbage(3)
                    elif event.type == KEYUP and not tetris_game.game_over:
                        tetris_game.input.handle_keyup_event(event.key)

        for (tetris_game, keymap) in [(tetris_game_1, keymap_1), (tetris_game_2, keymap_2)]:
            if not tetris_game.game_over:
                pressed_keys = pygame.key.get_pressed()

                actions = {}

                for action in TetrisAction:
                    actions[action] = bool(pressed_keys[keymap[action]])

                tetris_game.execute_actions(actions)
                tetris_game.update()

            displaysurface.blit(tetris_game.view.cell_surface,
                                tetris_game.view.cell_rect)
            displaysurface.blit(tetris_game.view.grid_surface,
                                tetris_game.view.grid_rect)

            for i in range(PIECE_PREVIEWS):
                displaysurface.blit(tetris_game.view.queue_surfaces[i],
                                    tetris_game.view.queue_rects[i])

            displaysurface.blit(tetris_game.view.held_surface,
                                tetris_game.view.held_rect)

            tetris_game.debug.data = ""
            for row in tetris_game.field.cells:
                tetris_game.debug.data += "  ".join(
                    list(map(lambda x: "_" if x is None else str(x if x > 0 else "X"), row)))
                tetris_game.debug.data += "\n"
            tetris_game.debug.data += tetris_game._debug_str()

            tetris_game.debug.draw_surfaces()
            displaysurface.blit(tetris_game.debug.surface,
                                tetris_game.debug.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main()
