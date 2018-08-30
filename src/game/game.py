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


def run_trial():
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

    car = Car()
    model = Model()
    allsprites = pygame.sprite.RenderPlain((car))
    clock = pygame.time.Clock()

    score = 0

    while 1:
        clock.tick(60)

        score = score + 1
        if Tile.collides(car.pose[0], car.pose[1]):
            break

        move = model.get_action(car.get_state())
        car.move(move)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                car.handle_key(event.key)

        allsprites.update()

        # Draw Everything
        screen.blit(bg, (0, 0))

        Tile.get_neighbors(Tile.to_tile_number(car.pose[0], car.pose[1]), screen)

        score_text = myfont.render("Score {0}".format(score), 1, (255, 255, 255))
        screen.blit(score_text, (5, 10))
        allsprites.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), car.rect, 1)
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
    pygame.init()
    for i in range(0, 10):
        run_trial()
        time.sleep(0.5)
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
