from base_classes import *
from wall_class import *
import pygame 

walls = [field, block_top_left, block_bottom_left, block_top_right, block_bottom_right]

class Ball(DynamicObject):
    
    """
    Class defining the ball and the bouncing of it
    
    Attributes:
        pos : position of the ball
        velocity : velocity of the ball
        both of these attribute are inheritate of the dynamic object class
        
        radius : radius of the ball, needed for de boucing
        bounce_factor : "how much" de ball gain in velocity after the bounce

    
    """
    def __init__(self, pos, velocity, radius, bounce_factor):
        super().__init__(pos, velocity)
        self.radius = radius
        self.bounce_factor = bounce_factor
        
    def draw(self,screen):
        pygame.draw.circle(screen, (0,255,0), (self.pos.x, self.pos.y), self.radius)
        
    def bounce(self, walls):
        
        for wall in walls:   #it goes over all walls
            
            """
            here is an other option possible, we can make rectangle
            around the ball and then collision checken with colliderect
            """
            closest_x = 
        
        
                
"""               
not using elif because otherwise it would stop after one True
wall.rect.bottom (and the other ones) is an automatic pygame function, 
it works because i made an pygame.rect

so here i define walls, that contains the attributes and dimensions of 
my field. 



"""
        
       
        
        