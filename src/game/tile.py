import pygame
import text_to_screen
# 088!7rT8OWqd


class Tile(pygame.Rect):
    List = {}
    size = 32
    width, height = 20, 15
    total_tiles = 1

    @staticmethod
    def pre_init(SCREEN):
        for y in range(0, SCREEN.get_height(), Tile.size):
            for x in range(0, SCREEN.get_width(), Tile.size):
                Tile(x, y, 'empty')

    @staticmethod
    def load(lt):
        for t in lt:
            t = t - 1
            Tile((t % Tile.width)*Tile.size, int(t/Tile.width)*Tile.size, 'solid')
            
    def __init__(self, x, y, Type):  
        self.type = Type
        self.number = Tile.total_tiles
        Tile.total_tiles += 1

        pygame.Rect.__init__(self, (x, y) , (Tile.size, Tile.size) )
        Tile.List[Tile.to_tile_number(x, y)] = self

    @staticmethod
    def get_neighbors(tn, screen=None):
        n = []

        matrix_size = 2
        for h in range(-1*matrix_size, matrix_size + 1):
            for v in range(-1*matrix_size, matrix_size + 1):
                n.append(tn + h + v*Tile.width)

        ohe = []

        for t in n:
            ohe.append(Tile.get_type(t, screen))
        return ohe

    @staticmethod
    def get_type(num, screen=None):
        if num <= 0 or num >= Tile.width * Tile.height:
            return 1
        Tile.List[num].draw_tile(screen)
        return int(Tile.List[num].type == 'solid')

    @staticmethod
    def get_tile(number):
        if number in Tile.List:
            return Tile.List[number]

    @staticmethod
    def collides(x, y):
        tn = Tile.to_tile_number(x, y)
        return Tile.List[tn].type == "solid"

    @staticmethod
    def to_tile_number(x, y):
        return int(x / Tile.size) + 1 + (int(y / Tile.size) * Tile.width)

    @staticmethod
    def draw_tiles(SCREEN):        
        for tile in Tile.List:
            if not(tile.type == 'empty'):
                tile.draw_tile(SCREEN)

    def draw_tile(self, SCREEN):
        if SCREEN is None:
            return
        pygame.draw.line(SCREEN, [255, 0, 0], [self.x, self.y], [self.x + self.size, self.y + self.size])
        pygame.draw.line(SCREEN, [255, 0, 0], [self.x, self.y + self.size], [self.x + self.size, self.y])
        # pygame.draw.rect(SCREEN, [200, 200, 200, 255], self)
        text_to_screen.draw_Text(SCREEN, "", self.x, self.y + 8)

    def draw_Q(self, SCREEN, q):
        if SCREEN is None:
            return
        pygame.draw.line(SCREEN, [255, 0, 0], [self.x, self.y], [self.x + self.size, self.y + self.size])
        pygame.draw.line(SCREEN, [255, 0, 0], [self.x, self.y + self.size], [self.x + self.size, self.y])
        pygame.draw.rect(SCREEN, [200, 200, 200, 255], self)
        text_to_screen.draw_Text(SCREEN, q, self.x, self.y + 8)
