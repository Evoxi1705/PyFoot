from base_classes import *
from constants import *
from wall_class import *
import pygame 

walls = [block_top_left, block_bottom_left, block_top_right, block_bottom_right, block_top, block_bottom]
triangles = [triangle_bottom_left, triangle_top_left, triangle_bottom_right, triangle_top_right]

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
    
    def update(self, dt, field, player, easy_bot,triangles):
        self._apply_gravity(dt)      
        self._apply_movement(dt)     
        self._apply_friction(dt, field)
        self._handle_borders(field)
        self.bounce_triangle(triangles)
        self.ball_player_collision(player)
        self.ball_player_collision(easy_bot)
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,0), (self.pos.x + self.radius, self.pos.y + self.radius), self.radius)
        
    def _handle_borders(self, field): 
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
        

    def bounce_triangle(self, triangles):

        cx = self.pos.x + self.radius
        cy = self.pos.y + self.radius
        
        for triangle in triangles:
          x, y, s = triangle.pos.x, triangle.pos.y, triangle.size
          
          if triangle.corner == "bottom-left":
              p1, p2 = (x, y), (x + s, y + s)
          elif triangle.corner == "bottom-right":
              p1, p2 = (x + s, y), (x, y + s)
          elif triangle.corner == "top-left":
              p1, p2 = (x + s, y), (x, y + s)
          elif triangle.corner == "top-right":
              p1, p2 = (x, y), (x + s, y + s)
          
          edge_x = p2[0] - p1[0]
          edge_y = p2[1] - p1[1]    
        
          edge_length_sqrt = edge_x**2 + edge_y**2
        
          t = ((cx - p1[0]) * edge_x + (cy - p1[1]) * edge_y) / edge_length_sqrt
          if t < 0:
              t = 0
          if t > 1:
              t = 1
        
          closest_x = p1[0] + t * edge_x
          closest_y = p1[1] + t * edge_y
        
          dx = cx - closest_x
          dy = cy - closest_y
          distance = (dx**2 + dy**2) ** 0.5
          

          if distance <= self.radius and distance != 0:
              normal_x = dx / distance
              normal_y = dy / distance
    
              overlap = self.radius - distance
              self.pos.x += normal_x * overlap
              self.pos.y += normal_y * overlap
              
              dot = self.velocity.x * normal_x + self.velocity.y * normal_y
              self.velocity.x = (self.velocity.x - 2 * dot * normal_x) * self.bounce_factor
              self.velocity.y = (self.velocity.y - 2 * dot * normal_y) * self.bounce_factor
            
            
    
    def ball_player_collision(self, player):
        
        cx = self.pos.x + self.radius
        cy = self.pos.y + self.radius
        
        closest_x = max(player.pos.x, min(cx, player.pos.x + player.width))
        closest_y = max(player.pos.y, min(cy, player.pos.y + player.width))
        
        dx = cx - closest_x
        dy = cy - closest_y
        
        distance = (dx**2 + dy**2) **0.5
        
        if distance <= self.radius and distance != 0:
            normal_x = dx / distance
            normal_y = dy / distance
  
            overlap = self.radius - distance
            self.pos.x += normal_x * overlap
            self.pos.y += normal_y * overlap
            
            dot = self.velocity.x * normal_x + self.velocity.y * normal_y
            self.velocity.x = (self.velocity.x - 2 * dot * normal_x) * self.bounce_factor
            self.velocity.y = (self.velocity.y - 2 * dot * normal_y) * self.bounce_factor
    
       
        
        