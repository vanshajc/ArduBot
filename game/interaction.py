import pygame, sys
from tile_Class import Tile

WALLS =[]

def interaction(SCREEN):

    Mpos = pygame.mouse.get_pos() # [x, y] 
    Mx = int(Mpos[0] / Tile.width)
    My = int(Mpos[1] / Tile.height)
    tileNumber = (My * 40) + (Mx + 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:
            print(pygame.mouse.get_pressed())

            if pygame.mouse.get_pressed()[0] or event.button == 1:
                for tile in Tile.List:
                    if abs(tile.x - Mpos[0]) < 32 and abs(tile.y - Mpos[1]) < 32:
                        tile.type = 'solid'
                        if tileNumber not in WALLS:
                            WALLS.append(tileNumber)
                        break
            elif pygame.mouse.get_pressed()[2] or event.button == 3: # 1 = LEFT
                tile = Tile.get_tile(tileNumber)
                if tileNumber in WALLS:
                    tile.type = 'empty'
                    WALLS.remove(tileNumber)
                else:
                    break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_l]:
        print(WALLS)
        with open("obstacle_map.py", "w") as text_file:
            text_file.write('{}\n\t{}\n\t{}'.format("def obstacles():", "obstacle_map = " + str(WALLS), "return obstacle_map"))

