import pygame

class Wall:
    def __init__(self,x,y,width,height,color=(255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.color = color
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        


