#!/usr/local/bin/python3
import pygame
from pygame.locals import *
from obstacle_map import *
from Tile import Tile
from car import Car

pygame.font.init()
myfont = pygame.font.SysFont("arial", 16)
size = width, height = 640, 480
score = 0


def main():
    pygame.init()
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
    allsprites = pygame.sprite.RenderPlain((car))
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)

        score_text = myfont.render("Score {0}".format(score), 1, (255, 255, 255))

        if Tile.collides(car.rect.center[0], car.rect.center[1]):
            print(car.pose[0], car.pose[1], Tile.to_tile_number(car.pose[0], car.pose[1]), car.rect.center)
            print(car.image.get_width(), car.image.get_height())
            print("!!!! Collision !!!!")
            break

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

        allsprites.update()

        # Draw Everything
        screen.blit(bg, (0,0))
        screen.blit(score_text, (5, 10))
        allsprites.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), car.rect, 1)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
