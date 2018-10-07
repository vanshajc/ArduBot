import pygame
from pygame.locals import *
from util import *
from tile import Tile
import numpy as np
import math
from settings import SENSOR_RANGE


class Car(pygame.sprite.Sprite):

    matrix_size = SENSOR_RANGE

    """init car position, velocity, and image"""
    def __init__(self, auto=False):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('car.png', -1)
        self.original = self.image

        self.orientation = 0
        self.forward_velocity = 2
        self.angular_velocity = 0.001
        self.auto = auto

        self.pose = (50 + np.random.rand()*100, 250)
        self.rect.center = self.pose

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def get_state(self):
        return np.expand_dims(np.asarray(Tile.get_neighbors(Tile.to_tile_number(self.pose[0], self.pose[1]))), axis=1)

    def update(self):
        move = (-1 * self.forward_velocity * math.sin(self.orientation),
                self.forward_velocity * math.cos(self.orientation))

        # print(to_degrees(self.orientation), move[0], move[1], round(move[0]), round(move[1]))

        new_pose = self.rect.move(round(move[0]), round(-1*move[1]))

        if (new_pose[0] <= self.area.left or new_pose[0] >= self.area.right - 50) or \
            (new_pose[1] <= self.area.top or new_pose[1] >= self.area.bottom - 50):
            return

        if Tile.collides(self.pose[0], self.pose[1]):
            return -1

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

    def get_relative_state(self):
        size = 2*Car.matrix_size + 1
        grid = np.zeros((size, size))
        c, s = float(np.cos(self.orientation)), float(np.sin(self.orientation))
        R = np.array([[c, -s],
                      [s, -c]])
        for i in range(-1*Car.matrix_size, Car.matrix_size + 1):
            for j in range(-1 * Car.matrix_size, Car.matrix_size + 1):
                vec = (R.dot(np.asarray([i, j])))*Tile.size + np.asarray(self.pose)
                grid[i, j] = Tile.get_type(Tile.to_tile_number(vec[0], vec[1]))
        return np.expand_dims(grid.flatten(), axis=1)

    def get_list(self):
        return np.array2string(self.get_relative_state().flatten())

    def get_list_debug(self, screen):
        size = 2 * Car.matrix_size + 1
        grid = np.zeros((size, size))
        g2 = np.zeros((size, size))
        c, s = float(np.cos(self.orientation)), float(np.sin(self.orientation))
        R = np.array([[c, -s],
                      [s, c]])
        count = 0
        print("-"*50)
        for i in range(0, Car.matrix_size*2 + 1):
            for j in range(0, Car.matrix_size*2 + 1):
                ip = i - Car.matrix_size
                jp = j - Car.matrix_size
                print(R.dot(np.asarray([ip, jp])) * Tile.size)
                vec = (R.dot(np.asarray([jp, ip]))) * Tile.size + np.asarray(self.pose)
                grid[j, i] = Tile.get_type(Tile.to_tile_number(vec[0], vec[1]))
                g2[j, i] = Tile.get_type(Tile.to_tile_number(self.pose[0] + ip*Tile.size, self.pose[1] + jp*Tile.size))
                # Tile.get_tile(Tile.to_tile_number(self.pose[0] + ip*Tile.size, self.pose[1] + jp*Tile.size))\
                #     .draw_Q(screen, count)
                count += 1

        print(np.array2string(np.expand_dims(g2.flatten(), axis=1).flatten()),
              np.array2string(np.expand_dims(grid.flatten(), axis=1).flatten()))

    def move(self, m):
        self.rotate(m * math.pi/120)


