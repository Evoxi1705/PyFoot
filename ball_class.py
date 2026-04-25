from base_classes import *
from constants import *
from wall_class import *
import pygame 

walls = [block_top_left, block_bottom_left, block_top_right, block_bottom_right, block_top, block_bottom]
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
        self._handle_borders(field) # So that it gets updated every frame and it is not needed to be called in the main
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,0), (self.pos.x + self.radius, self.pos.y + self.radius), self.radius)
        
    def _handle_borders(self, field): # The first _ means the method is meant to be local, not called outside the class
        """ Keeps the object inside the game world. """
        if self.get_bottom() > field.get_bottom():
            self.pos.y = field.get_bottom() - self.height 
            self.velocity.y = -abs(self.velocity.y) * self.bounce_factor

        if self.get_top() < field.get_top():
            self.pos.y = field.get_top()
            self.velocity.y = abs(self.velocity.y) * self.bounce_factor

        if self.get_right() > field.get_right():
            self.pos.x = field.get_right() - self.width
            self.velocity.x = -abs(self.velocity.x) * self.bounce_factor

        if self.get_left() < field.get_left():
            self.pos.x = field.get_left()
            self.velocity.x = abs(self.velocity.x) * self.bounce_factor
        

    def bounce_player(self, player):
        
        ball_pos = Vector2(self.pos.x, self.pos.y)
        
        closest_x = max(player.pos.x, min(ball_pos.x, player.pos.x + player.width))
        closest_y = max(player.pos.y, min(ball_pos.y, player.pos.y + player.height))
        
        dx = abs(ball_pos.x - closest_x)
        dy = abs(ball_pos.y - closest_y)
        
        if (dx**2)*0.5 < (self.radius**2)*0.5:
            self.velocity.x *= -self.bounce_factor
                
        if (dx**2)*0.5 < (self.radius**2)*0.5:
            self.velocity.y *= -self.bounce_factor 
        


    def bounce_triangle():
        pass
        
        

        
                
              

        
       
        
        