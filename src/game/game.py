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

pygame.font.init()
myfont = pygame.font.SysFont("arial", 16)
size = width, height = 640, 480

# Number of cars to train at the same time
max_players = 10


def load_players(num_players):
    cars = []
    models = []
    for i in range(num_players):
        c = Car()
        cars.append(c)
        models.append(Model())
    sprites = pygame.sprite.RenderPlain(cars)
    return cars, models, sprites, [0 for _ in range(num_players)]


def run_trial(cars, models, allsprites, scores):
    np.random.seed()
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

    # car = Car()
    # model = Model()
    # allsprites = pygame.sprite.RenderPlain((car))

    clock = pygame.time.Clock()

    score = 0

    while 1:
        clock.tick(60)

        blocked = True

        for i in range(len(cars)):
            car = cars[i]
            if Tile.collides(car.pose[0], car.pose[1]):
                continue
            blocked = False
            move = models[i].get_action(car.get_state())
            car.move(move)

        # score = score + 1
        # if Tile.collides(car.pose[0], car.pose[1]):
        #     break
        #
        # move = model.get_action(car.get_state())
        # car.move(move)

        if blocked:
            return

        for event in pygame.event.get():
            print("is something happening?")
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                car.handle_key(event.key)

        allsprites.update()

        # Draw Everything
        screen.blit(bg, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    print("Final Score: ", score)
    data = [{"score": score,
             "layer1": model.layer1.tolist(),
             "layer2": model.layer2.tolist(),
             "bias1": model.b1.tolist(),
             "bias2": model.b2.tolist()
             }]

    with open('data.json', 'w') as f:
        json.dump(data, f)


def main():
    # Init pygame
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('ArduBot: Development Stage')
    pygame.mouse.set_visible(0)


    # Run trials
    for i in range(0, 10):
        # One trial run on a set of cars and their models
        cars, models, allsprites, scores = load_players(max_players)
        run_trial(cars, models, allsprites, scores)
        time.sleep(0.5)

    # Exit
    pygame.quit()


def fill_players(num, cars, models, sprites, scores):
    nc, nm, ns, nss = load_players(num)
    cars.extend(nc)
    models.extend(nm)
    sprites.add(ns)
    scores.extend(nss)
    return cars, models, sprites, scores


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
