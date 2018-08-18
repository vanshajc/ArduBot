import pygame
from pygame.locals import *
from util import *
import math

class Car(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('car.png', -1)
        self.orientation = 0
        self.forward_velocity = 0.1
        self.angular_velocity = 0
        self.pose = (50,50)
        self.rect.center = self.pose

    def update(self):
        "move the fist based on the mouse position"

        self.dist = (self.forward_velocity * math.cos(self.orientation),
                     self.forward_velocity * math.sin(self.orientation))
        self.orientation += self.angular_velocity

        self.pose = self.rect.move(self.dist[0], self.dist[1])