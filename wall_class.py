import pygame

class Wall:
    def __init__(self,x,y,width,height, color, radius=20):
        self.rect = pygame.Rect(x, y, width, height) #door dit te gebruiken zal de botsing functie in ball_class makkelijker zijn
        self.color = color
        self.radius = radius #pas op deze moet kleiner zijn dan de helft van de korste zijde van de muur
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius = self.radius)
        


#drawing four blocks in each corner to shape my terrain     
        
field = Wall(80, 60, 520, 300, color=(255,255,255))


block_top_left     = Wall(80,  60,  60, 100, color=(0,0,0))
block_bottom_left  = Wall(80,  260, 60, 100, color=(0,0,0))
block_top_right    = Wall(540, 60,  60, 100, color=(0,0,0))
block_bottom_right = Wall(540, 260, 60, 100, color=(0,0,0))


"""
in game loop:
field.draw(screen)
block_top_left.draw(screen)
block_bottom_left.draw(screen)
block_top_right.draw(screen)
block_bottom_right.draw(screen)
"""