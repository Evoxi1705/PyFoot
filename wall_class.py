import pygame
from base_classes import *
from constants import WALL_COLOR

WIDTH,HEIGHT = 1000,800
BW = 100 #block width
BH = 300 # block height
r = 20 #radius
TH = 50 #triangle height = triangle width


class Field(StaticObject):
    """
    Class for making the field
    
    Attributes:
        x,y : position of the top left corner of each rectangle
        width, height : dimension of the rectangle
        r_top_left, r_top_right, r_bot_left, r_bot_right : radius of each corner of the field, 
               these have to be smaller than half the size of the height
               
    This class actually makes an rectangle, we can use it to make four block on each
    corner to shape de field and to make goals
    
    """
    def __init__(self,x,y,width,height, color, r_top_left=0, r_top_right=0, r_bot_left=0, r_bot_right=0):
        self.rect = pygame.Rect(x, y, width, height) #door dit te gebruiken zal de botsing functie in ball_class makkelijker zijn

class Wall(StaticObject):
    def __init__(self, pos, width, height, color=WALL_COLOR):
        super().__init__(pos, height, width)
        self.color = color
        self.r_top_left = r_top_left 
        self.r_top_right = r_top_right
        self.r_bot_left = r_bot_left
        self.r_bot_right = r_bot_right
        
    def draw_rect(self,screen):
        pygame.draw.rect(screen, self.color, self.rect, 
            border_top_left_radius=self.r_top_left,
            border_top_right_radius=self.r_top_right,
            border_bottom_left_radius=self.r_bot_left,
            border_bottom_right_radius=self.r_bot_right)


class Triangle:
    
    """
    Class for making the little triangle that we used so we do,'t have 90° angles

    Attributes:
        point : list of three tuples indacting de position of the triangle
                the fist coordinate is de right angle, then we go clockwise
                als we point niet willen gebruiken kunnen we ook x,y,width,height
                en dan  self.points = [(x, y + height),(x + width, y + height),(x + width//2, y)]
        color : color of the triangles
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos.x, self.pos.y, self.width, self.height))
        
    """
    def __init__(self, points, color):
        self.points = points
        self.color = color
        
    def draw_triangle(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        





triangle_top_left = Triangle([(BW,0),(BW + TH,0),(BW, TH)], color=(0,0,0))
triangle_bottom_left = Triangle([(BW,HEIGHT), (BW, HEIGHT - TH), (BW + TH, HEIGHT)],color=(0,0,0))
triangle_top_right = Triangle([(WIDTH - BW,0),(WIDTH - BW, TH),(WIDTH - BW - TH,0)],color=(0,0,0))
triangle_bottom_right = Triangle([(WIDTH - BW, HEIGHT),(WIDTH - BW-TH, HEIGHT),(WIDTH - BW, HEIGHT - TH)],color=(0,0,0))
"""
we can do the exact same thing if we want triangle in the goals
"""

block_top_left     = Field(0,  0,  BW, BH, color=(0,0,0), r_bot_right=r)
block_bottom_left  = Field(0,  HEIGHT - BH, BW, BH, color=(0,0,0), r_top_right=r)
block_top_right    = Field(WIDTH - BW, 0,  BW, BH, color=(0,0,0), r_bot_left=r)
block_bottom_right = Field(WIDTH - BW, HEIGHT - BH , BW, BH, color=(0,0,0), r_top_left=r)





