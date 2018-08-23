import pygame, text_to_screen

class Tile(pygame.Rect):
    List = []
    width, height = 32, 32
    total_tiles = 1
    H, V = 1, 40 

    @staticmethod
    def pre_init(SCREEN):
        for y in range(0, SCREEN.get_height(), Tile.height):
            for x in range(0, SCREEN.get_width(), Tile.width):
                Tile(x, y, 'empty')

    @staticmethod
    def load(lt):
        for t in lt:
            t = t - 1
            print("Tile at: ", t, t%40, int(t/40))
            Tile((t % 40)*32, int(t/40)*32, 'solid')
            
    def __init__(self, x, y, Type):  
        self.type = Type
        self.number = Tile.total_tiles
        Tile.total_tiles += 1

        pygame.Rect.__init__(self, (x, y) , (Tile.width, Tile.height) )
        Tile.List.append(self)

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
        return (x / Tile.width) + 1 + (y / Tile.height * 40)

    @staticmethod
    def draw_tiles(SCREEN):        
        for tile in Tile.List:
            if not(tile.type == 'empty'):
                print(SCREEN.get_height(), SCREEN.get_width(), tile)
                pygame.draw.line(SCREEN, [255, 0, 0], [tile.x, tile.y], [tile.x + tile.width, tile.y + tile.width])
                pygame.draw.line(SCREEN, [255, 0, 0], [tile.x, tile.y + tile.width], [tile.x + tile.width, tile.y])
                pygame.draw.rect(SCREEN, [40, 40, 40], tile)
                text_to_screen.draw_Text(SCREEN, " ", tile.x, tile.y + 8)










            
