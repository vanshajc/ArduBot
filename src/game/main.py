#!/usr/local/bin/python3
import pygame, sys, text_to_screen
from tile import Tile
from interaction import interaction

pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((640, 480)) # 40 x 30
Tile.pre_init(SCREEN)
CLOCK = pygame.time.Clock()
FPS = 20
TOTAL_FRAMES = 0
background = pygame.Surface(SCREEN.get_size())
background = background.convert()
background.fill((250, 250, 250))

while True:

    SCREEN.blit(background, (0,0))
    interaction(SCREEN)
    Tile.draw_tiles(SCREEN)
    pygame.display.flip()
    CLOCK.tick(FPS)
    TOTAL_FRAMES += 1
