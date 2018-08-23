import pygame

def draw_Text(SCREEN, text, x, y, size = 15,
            color = (255, 255, 255), font_type = 'monospace'):
        
    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    SCREEN.blit(text, (x, y))


  


        
    
