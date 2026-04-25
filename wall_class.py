import pygame
from base_classes import *
from constants import *

WIDTH,HEIGHT = 1500,750
BW = 100 #block width
BH = 300 # block height
r = 20 #radius
TH = 50 #triangle height = triangle width


class Rectangle(StaticObject):
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
    def __init__(self, pos,width,height, color,):
        super().__init__(pos, height, width)
        self.rect = pygame.Rect(pos.x, pos.y, width, height) #door dit te gebruiken zal de botsing functie in ball_class makkelijker zijn
        self.color = color
        
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)



    
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



class Triangle(StaticObject):
    def __init__(self, pos, size, corner, color=WALL_COLOR):
        super().__init__(pos, size, size)
        self.size = size
        self.corner = corner
        self.color = color

    def draw(self, screen):
        x, y, s = self.pos.x, self.pos.y, self.size
        if self.corner == "bottom-left":
            pts = [(x, y), (x + s, y + s), (x, y + s)]
        elif self.corner == "bottom-right":
            pts = [(x + s, y), (x + s, y + s), (x, y + s)]
        elif self.corner == "top-left":
            pts = [(x, y), (x + s, y), (x, y + s)]
        elif self.corner == "top-right":
            pts = [(x, y), (x + s, y), (x + s, y + s)]
        pygame.draw.polygon(screen, self.color, pts)



triangle_bottom_left  = Triangle(Vector2(BW, HEIGHT - TH), TH, "bottom-left")
triangle_top_left     = Triangle(Vector2(BW, 0), TH, "top-left")
triangle_bottom_right = Triangle(Vector2(WIDTH - BW - TH, HEIGHT - TH), TH, "bottom-right")
triangle_top_right    = Triangle(Vector2(WIDTH - BW - TH, 0), TH, "top-right")
"""
we can do the exact same thing if we want triangle in the goals
"""

block_top_left = Rectangle(Vector2(0,  0),  BW, BH, color=WALL_COLOR)
block_bottom_left = Rectangle(Vector2(0,  HEIGHT - BH), BW, BH, color=WALL_COLOR)
block_top_right = Rectangle(Vector2(WIDTH - BW, 0),  BW, BH, color=WALL_COLOR)
block_bottom_right = Rectangle(Vector2(WIDTH - BW, HEIGHT - BH), BW, BH, color=WALL_COLOR)







