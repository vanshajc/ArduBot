#!/usr/local/bin/python3
import os, sys
import pygame
from pygame.locals import *
from car import *

pygame.font.init()
myfont = pygame.font.SysFont("arial", 16)
size = width, height = 800,500
score = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('ArduBot: Development Stage')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    car = Car()
    allsprites = pygame.sprite.RenderPlain((car))
    clock = pygame.time.Clock()

    while 1:
        clock.tick(30)
        scoretext = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
        screen.blit(scoretext, (5, 10))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                car.handle_key(event.key)

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
