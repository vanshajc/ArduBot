import pygame
from pygame.locals import *
from util import *
from tile import Tile
import numpy as np
import math


class Car(pygame.sprite.Sprite):
    """init car position, velocity, and image"""
    def __init__(self, auto=False):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('car.png', -1)
        self.original = self.image

        self.orientation = 0
        self.forward_velocity = 2
        self.angular_velocity = 0.001
        self.auto = auto

        self.pose = (50 + 100*np.random.random(), 250)
        self.rect.center = self.pose

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def get_state(self):
        return np.expand_dims(np.asarray(Tile.get_neighbors(Tile.to_tile_number(self.pose[0], self.pose[1]))), axis=1)

    def update(self):

        if Tile.collides(self.pose[0], self.pose[1]):
            return

        move = (-1 * self.forward_velocity * math.sin(self.orientation),
                self.forward_velocity * math.cos(self.orientation))

        # print(to_degrees(self.orientation), move[0], move[1], round(move[0]), round(move[1]))

        new_pose = self.rect.move(round(move[0]), round(-1*move[1]))

        if (new_pose[0] <= self.area.left or new_pose[0] >= self.area.right - 50) or \
            (new_pose[1] <= self.area.top or new_pose[1] >= self.area.bottom - 50):
            return

        self.pose = new_pose.center
        self.rect = new_pose

    def rotate(self, angle):
        center = self.rect.center
        self.orientation += angle
        self.image = pygame.transform.rotate(self.original, to_degrees(self.orientation))
        self.rect = self.image.get_rect(center=center)

    def handle_key(self, key):
        # if key == K_DOWN:
        #     self.forward_velocity -= 1
        # if key == K_UP:
        #     self.forward_velocity += 1
        if key == K_LEFT:
            self.rotate(math.pi/120)
        if key == K_RIGHT:
            self.rotate(-1*math.pi/120)

    def move(self, m):
        self.rotate(m * math.pi/90)


