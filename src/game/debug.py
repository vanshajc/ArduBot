#!/usr/local/bin/python3.6
import pygame
from pygame.locals import *
from obstacle_map import *
from tile import Tile
from car import Car
from model import Model
import time
import numpy as np
import random
import json

pygame.font.init()
myfont = pygame.font.SysFont("arial", 16)
size = width, height = 640, 480

# Number of cars to train at the same time
max_players = 50
mutation_rate = 0.3
max_trials = 100


def load_players(num_players):
    cars = []
    models = []
    for i in range(num_players):
        c = Car()
        cars.append(c)
        models.append(Model())
    sprites = pygame.sprite.RenderPlain(cars)
    return cars, models, sprites, np.ones(num_players)


def main():
    # Init pygame
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('ArduBot: Development Stage')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    bg = pygame.image.load("../../images/map1.png")

    screen.blit(bg, (0, 0))
    pygame.display.flip()

    Tile.pre_init(screen)
    Tile.load(obstacles())

    clock = pygame.time.Clock()

    cars, models, allsprites, scores = load_players(1)

    car = cars[0]

    while(1):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                car.handle_key(event.key)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            car.handle_key(pygame.K_RIGHT)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            car.handle_key(pygame.K_LEFT)

        # allsprites.update()
        print(car.get_relative_state())
        print("-"*100)
        # Draw Everything
        screen.blit(bg, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
