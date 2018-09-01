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
max_players = 25
mutation_rate = 0.8
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


def run_trial(cars, models, allsprites, scores, display=True):
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

    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)

        blocked = True

        for i in range(len(cars)):
            car = cars[i]
            if Tile.collides(car.pose[0], car.pose[1]):
                continue
            blocked = False
            move = models[i].get_action(car.get_relative_state())
            car.move(move)
            scores[i] += 1

        if blocked:
            return scores

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                car.handle_key(event.key)

        allsprites.update()
        # Draw Everything
        if display:
            screen.blit(bg, (0, 0))
            allsprites.draw(screen)
            pygame.display.flip()

    return scores


def main():
    # Init pygame
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('ArduBot: Development Stage')
    # pygame.mouse.set_visible(0)

    cars, models, allsprites, scores = load_players(max_players)

    # Run trials
    for i in range(0, max_trials):
        cars, _, allsprites, _ = load_players(max_players)
        models = get_next_gen(models, scores)
        # One trial run on a set of cars and their models
        scores = np.zeros(max_players)
        scores = run_trial(cars, models, allsprites, scores, display=True)
        time.sleep(0.2)
        print("Generation:", i, "Score:", np.max(scores), "Average:", np.average(scores))
        print(scores)
        print("="*100)

    print("Best score:", np.max(scores))

    with open("data.json", "w") as f:
        json.dump(models[np.argmax(scores)].getJSON(), f)

    # Exit
    pygame.quit()


def get_next_gen(models, scores):
    ind = np.argsort(scores)

    # Take the 20% best players and add them in automatically.
    best = int(max_players*0.2)
    pM = []
    pS = []
    for i in ind[::-1][:best]:
        pM.append(models[i])
        pS.append(scores[i])

    pM = np.asarray(pM)
    pS = np.asarray(pS)
    offsprings = crossover(pM, max_players - best, pS)

    for off in offsprings:
        if random.random() > mutation_rate:
            off.mutate()

    new_models = np.hstack((pM, offsprings))
    return new_models


def crossover(parents, offspring_size, scores):
    offspring = []

    for k in range(offspring_size):
        parent1_idx = select_parent(scores)
        parent2_idx = select_parent(scores)
        # parent2_idx = (k + 1) % parents.shape[0]
        m = Model.combine_random(parents[parent1_idx], parents[parent2_idx])

        # m.layer1 = random.choice((parents[parent1_idx].layer1, parents[parent2_idx].layer1))
        # m.layer2 = random.choice((parents[parent1_idx].layer2, parents[parent2_idx].layer2))

        offspring.append(m)
    return np.asarray(offspring)


def select_parent(scores):
    p_sum = np.random.randint(int(np.sum(scores)))

    i = 0
    while p_sum > 0:
        p_sum -= scores[i]
        i += 1
    return i - 1


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
