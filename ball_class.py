from base_classes import *
import pygame 

class Ball(DynamicObject):
    def __init__(self,pos,velocity, radius):
        super().__init__(pos,velocity)
        self.radius = radius
        
    def draw(self,screen):
        pygame.draw.circle(screen,self.radius)
        
    def bounce(self):
        self.velocity *= -1

        
        
        
        
        
        
        