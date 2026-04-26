from base_classes import *
from constants import *
from wall_class import *
import pygame 

field = [block_top_left, block_bottom_left, block_top_right, block_bottom_right, block_top, block_bottom]
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
        self._handle_borders(field)
        #self.bounce(field) # So that it gets updated every frame and it is not needed to be called in the main

    def _handle_borders(self, field):
        """ Keeps the object inside the game world. """
        if self.get_bottom() > field.get_bottom():
            self.pos.y = field.get_bottom() - self.height 
            self.velocity.y = 0

        if self.get_top() < field.get_top():
            self.pos.y = field.get_top()
            self.velocity.y = 0

        if self.get_right() > field.get_right():
            self.pos.x = field.get_right() - self.width
            self.velocity.x = 0

        if self.get_left() < field.get_left():
            self.pos.x = field.get_left()
            self.velocity.x = 0
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,0), (self.pos.x + self.radius, self.pos.y + self.radius), self.radius)
         
    """ 
    def bounce(self, field):
        for wall in field:
 
            
            rect = wall.rect
            
            # Dichtstbijzijnde punt op de rechthoek t.o.v. het middelpunt van de bal
            cx = self.pos.x + self.radius
            cy = self.pos.y + self.radius
            
            closest_x = max(rect.left, min(cx, rect.right))
            closest_y = max(rect.top, min(cy, rect.bottom))
            
            dx = cx - closest_x
            dy = cy - closest_y
            
            dist = (dx**2 + dy**2) ** 0.5
            
            if dist == 0 or dist > self.radius:
                continue
            
            # Hoeveel overlappen ze?
            overlap = self.radius - dist
            
            # Normaliseer de richting
            nx = dx / dist
            ny = dy / dist
            
            # Duw de bal terug zodat hij niet meer overlapt
            self.pos.x += nx * overlap
            self.pos.y += ny * overlap
            
            # Reflecteer de velocity
            dot = self.velocity.x * nx + self.velocity.y * ny
            self.velocity.x = (self.velocity.x - 2 * dot * nx) * self.bounce_factor
            self.velocity.y = (self.velocity.y - 2 * dot * ny) * self.bounce_factor   
    
    
    def bounce_triangle():
        pass
        
        
"""
        
                
              

        
       
        
        