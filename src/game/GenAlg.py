import numpy as np
from settings import *
import random
from model import Model
import pygame
from pygame.locals import *
from tile import Tile
from car import Car
from model import Model
from obstacle_map import *


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
            if Tile.collides(car.pose[0], car.pose[1]) or scores[i] > 1500:
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

