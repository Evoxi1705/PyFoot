from base_classes import *
import pygame 

class Ball(DynamicObject):
    """
    Class defining the ball
    """
    def __init__(self, pos, velocity, radius, bounce_factor):
        super().__init__(pos, radius*2, radius*2, velocity)
        self.radius = radius
        self.bounce_factor = bounce_factor
        
    def draw(self,screen):
        pygame.draw.circle(screen, (0,255,0), (self.pos.x, self.pos.y), self.radius)
        
    def bounce(self):
        if ...:
            self.velocity.y *= -self.bounce_factor
        elif ...:
            self.velocity.x *= -self.bounce_factor
        
        

        
        
       
        
        