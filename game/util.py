import pygame
from pygame.locals import *
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('../images', name)

    image = pygame.image.load(fullname)

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()