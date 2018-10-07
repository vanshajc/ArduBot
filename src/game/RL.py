import numpy as np
from settings import *
import pygame
from pygame.locals import *
from tile import Tile
from obstacle_map import *
import time

Q = {}

count = 0
learning_rate = 1
discount_rate = 0.9
possible_actions = [-1.5, 0, 1.5]


def epsilon():
    return 1 - count


def get_best_action(state):
    best_action = 0
    best_value = 0

    for i in possible_actions:
        key = (state, i)
        if key in Q:
            if Q[key] > best_value:
                best_action = i
                best_value = Q[key]
        else:
            Q[key] = 0

    return best_action, best_value


def update_table(state, action, next_state, car):
    key = (state, action)
    reward = -9999 if Tile.collides(car.pose[0], car.pose[1]) else 1
    print("Update Q Table: ", key, Q[key], get_best_action(next_state))
    Q[key] = Q[key] + learning_rate * (reward + discount_rate * get_best_action(next_state)[1] - Q[key])
    print("New Q Value:", key, Q[key])



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
    random_moves = 0
    while 1:
        clock.tick(60)

        blocked = True

        states = []
        actions = []

        for i in range(len(cars)):
            car = cars[i]

            state = car.get_list()
            action = get_best_action(state)[0]
            val = np.random.rand()
            if val < epsilon():
                random_moves += 1
                action = possible_actions[np.random.randint(0, high=len(possible_actions))]
            else:
                print("Choosing: ", car.pose, get_best_action(state), (-1.5, Q[(state, -1.5)]), (0, Q[(state, 0)]),
                      (1.5, Q[(state, 1.5)]))

            global count
            count += 0.0001/max_players

            states.append(state)
            actions.append(action)

            if Tile.collides(car.pose[0], car.pose[1]) or scores[i] > 1500:
                continue
            blocked = False

            car.move(action)

            scores[i] += 1

        if blocked:
            return scores, len(Q), random_moves

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                for k in Q:
                    print(k, Q[k])
                return
            elif event.type == KEYDOWN:
                car.handle_key(event.key)

        allsprites.update()

        # Update q values
        for i in range(len(cars)):
            update_table(states[i], actions[i], cars[i].get_list(), cars[i])

        # Draw Everything
        if display:
            screen.blit(bg, (0, 0))
            allsprites.draw(screen)
            pygame.display.flip()

    return scores, len(Q), random_moves


def get_next_gen(models, scores):
    return models

