import base_classes
import pygame 

class Ball:
    def __init__(self,pos,velocity, radius, bounce):
        super().__init__(pos,velocity)
        self.radius = radius
        self.bounce = bounce
        
    def draw(self,screen):
        pygame.draw.circle(screen,self.radius)
        
    def bounce(self):
        self.velocity *= -1

        
        
        
        
        
        
        