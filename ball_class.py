from base_classes import *
from constants import *
#from wall_class import *
import pygame 

#walls = [block_top_left, block_bottom_left, block_top_right, block_bottom_right]
"""
Class defining the ball and the bouncing of it

Attributes:
    pos : position of the ball
    velocity : velocity of the ball
    both of these attribute are inheritate of the dynamic object class
   
    radius : radius of the ball, needed for de boucing
    bounce_factor : "how much" de ball gain in velocity after the bounce
"""

class Ball(DynamicObject):
    def __init__(self,pos,velocity,radius,bounce_factor=BOUNCE_FACTOR):
        super().__init__(pos, velocity, radius*2, radius*2)
        self.radius = radius
        self.bounce_factor = bounce_factor
        self.friction = FRICTION_BALL
    
    def update(self, dt, field):    
        super().update(dt, field)
        #self.bounce_screen() # So that it gets updated every frame and it is not needed to be called in the main
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,0), (self.pos.x + self.radius, self.pos.y + self.radius), self.radius)
             
    """
    def bounce(self, walls):
         for wall in walls:
            
             rect = wall.rect 
            
             #van welke punt is de bal het dichtste ?
            

             dx = abs(self.pos.x - closest_x)
             dy = abs(self.pos.y - closest_y)
            
             if (dx**2)*0.5 < (self.radius**2)*0.5:
                 self.velocity.x *= -self.bounce_factor
                
             if (dx**2)*0.5 < (self.radius**2)*0.5:
                 self.velocity.y *= -self.bounce_factor
                
    """       
    def bounce_triangle():
        pass
        
        

        
                

        
       
        
        