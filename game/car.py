import pygame
from pygame.locals import *
from util import *
import math


class Car(pygame.sprite.Sprite):
    """init car position, velocity, and image"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('car.png', -1)
        self.original = self.image

        self.orientation = 0
        self.forward_velocity = 1
        self.angular_velocity = 0.001

        self.pose = (100, 450)
        self.rect.center = self.pose

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):
        move = (self.forward_velocity * math.sin(self.orientation),
                self.forward_velocity * math.cos(self.orientation))

        print(self.orientation, math.cos(self.orientation), math.sin(self.orientation))

        new_pose = self.rect.move(move[0], -1*move[1])

        if (new_pose[0] <= self.area.left or new_pose[0] >= self.area.right - 50) or \
            (new_pose[1] < self.area.top or new_pose[1] > self.area.bottom):
            return

        self.pose = new_pose
        self.rect = self.pose

    def rotate(self, angle):
        center = self.rect.center
        self.orientation += angle
        self.image = pygame.transform.rotate(self.original, self.orientation)
        self.rect = self.image.get_rect(center=center)

    def handle_key(self, key):
        if key == K_DOWN:
            self.forward_velocity -= 1
        if key == K_UP:
            self.forward_velocity += 1
        if key == K_LEFT:
            self.rotate(math.pi/6)
        if key == K_RIGHT:
            self.rotate(-1*math.pi/6)

