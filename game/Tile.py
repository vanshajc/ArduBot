import pygame, text_to_screen


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
    def get_tile(number):
        for tile in Tile.List:
            if tile.number == number:
                return tile

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
                pygame.draw.line(SCREEN, [255, 0, 0], [tile.x, tile.y], [tile.x + tile.size, tile.y + tile.size])
                pygame.draw.line(SCREEN, [255, 0, 0], [tile.x, tile.y + tile.size], [tile.x + tile.size, tile.y])
                pygame.draw.rect(SCREEN, [40, 40, 40], tile)
                text_to_screen.draw_Text(SCREEN, "", tile.x, tile.y + 8)

