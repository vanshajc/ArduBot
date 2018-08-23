import pygame
from pygame.locals import *
import os
import math


def load_image(name, color_key=None):
    fullname = os.path.join('../images', name)

    image = pygame.image.load(fullname)

    image = image.convert()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0,0))
        image.set_colorkey(color_key, RLEACCEL)
    return image, image.get_rect()


def to_degrees(rad):
    return rad*180/math.pi

