#!/usr/local/bin/python3.6
import pygame
from pygame.locals import *
from obstacle_map import *
from tile import Tile
from car import Car
from model import Model
import time
import numpy as np
import json
from settings import *

from RL import run_trial, get_next_gen

pygame.font.init()


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
    # pygame.mouse.set_visible(0)

    cars, models, allsprites, scores = load_players(max_players)
    print("Beginning --")
    # Run trials
    for i in range(0, max_trials):
        cars, _, allsprites, _ = load_players(max_players)
        models = get_next_gen(models, scores)
        # One trial run on a set of cars and their models
        scores = np.zeros(max_players)
        scores = run_trial(cars, models, allsprites, scores, display=True)
        time.sleep(0.2)
        print("Generation:", i, "Score:", np.max(scores[0]), "Average:", np.average(scores[0]))
        print("Initialized: ", scores[1], scores[2])
        print("="*100)

    print("Best score:", np.max(scores))

    with open("../../data/data.json", "w") as f:
        json.dump(models[np.argmax(scores)].getJSON(), f)

    # Exit
    pygame.quit()


def manual_mode(car):
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


if __name__ == '__main__':
    main()
