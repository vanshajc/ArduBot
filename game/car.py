import pygame
from pygame.locals import *
from util import *
import math

class Car(pygame.sprite.Sprite):
    """init car position, velocity, and image"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('car.png', -1)
        self.original = self.image

        self.orientation = 0
        self.forward_velocity = 5
        self.angular_velocity = 0.001

        self.pose = (100, 50)
        self.rect.center = self.pose

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()



    def update(self):

        center = self.rect.center
        self.move = (self.forward_velocity * math.cos(self.orientation),
                     self.forward_velocity * math.sin(self.orientation))

        self.new_pose = self.rect.move(self.move[0], self.move[1])

        if  (self.new_pose[0] <= self.area.left or self.new_pose[0] >= self.area.right - 50) or \
            (self.new_pose[1] < self.area.top or self.new_pose[1] > self.area.bottom):
            return

        self.orientation += self.angular_velocity
        self.image = pygame.transform.rotate(self.original, self.angular_velocity)
        self.pose = self.new_pose
        self.rect = self.pose
        self.rect = self.image.get_rect(center=center)

    def handleKey(self, key):
        if key == K_DOWN:
            print("reducing speed")
            self.forward_velocity -= 5
        if key == K_UP:
            self.forward_velocity += 5
        # if key == K_LEFT:
        #     self.angular_velocity -= 0.01
        # if key == K_RIGHT:
        #     self.angular_velocity += 0.01

