import pygame
from base_classes import *
from constants import *

"""
This module is responsible for the boundaries of our game.
It initializes the perimeter blocks used for the arena.
"""

class Rectangle(StaticObject):
    """
    A static rectangular collision volume used for walls and boundaries.

    Attributes:
        color (tuple): RGB color value for rendering.
        rect (pygame.Rect): Pygame rect object used for optimized collision detection.
    """
    def __init__(self, pos,width,height, color,):
        super().__init__(pos, height, width)
        self.rect = pygame.Rect(pos.x, pos.y, width, height) #door dit te gebruiken zal de botsing functie in ball_class makkelijker zijn
        self.color = color
              
    def draw(self, screen):
        """
        Renders the rectangle to the screen.

        Args:
            screen (pygame.Surface): The surface to draw the rectangle upon.
        """
        pygame.draw.rect(screen, self.color, (self.pos.x, self.pos.y, self.width, self.height))

class Triangle(StaticObject):
    """
    A static right-angled triangle used primarily for arena corners.

    Triangles facilitate non-orthogonal bounces, requiring specialized 
    collision math compared to standard rectangles.

    Attributes:
        size (float): The length of the two legs forming the right angle.
        corner (str): Orientation of the triangle ("bottom-left", "bottom-right", 
                     "top-left", or "top-right").
        color (tuple): RGB color value for rendering.
    """
    def __init__(self, pos, size, corner, color=WALL_COLOR):
        super().__init__(pos, size, size)
        self.size = size
        self.corner = corner
        self.color = color

    def draw(self, screen):
        """
        Calculates vertex points based on orientation and renders the polygon.

        Args:
            screen (pygame.Surface): The surface to draw the triangle upon.
        """
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

class Field:
    """A utility class providing boundary coordinates for the playable area."""
    def get_top(self): return 0
    def get_bottom(self): return SCREEN_HEIGHT
    def get_left(self): return BW
    def get_right(self): return SCREEN_WIDTH - BW
    
# Defining the perimeter blocks
triangle_bottom_left  = Triangle(Vector2(BW, SCREEN_HEIGHT - TH), TH, "bottom-left", color=(255, 0, 0))
triangle_top_left     = Triangle(Vector2(BW, 0), TH, "top-left", color=(255, 0, 0))
triangle_bottom_right = Triangle(Vector2(SCREEN_WIDTH - BW - TH, SCREEN_HEIGHT - TH), TH, "bottom-right", color=(0, 0, 0))
triangle_top_right    = Triangle(Vector2(SCREEN_WIDTH - BW - TH, 0), TH, "top-right", color=(0, 0, 0))

block_top_left     = Rectangle(Vector2(0,  0),  BW, BH, color=(255, 0, 0))
block_bottom_left  = Rectangle(Vector2(0,  SCREEN_HEIGHT - BH), BW, BH, color=(255, 0, 0))
block_top_right    = Rectangle(Vector2(SCREEN_WIDTH - BW, 0),  BW, BH, color=(0, 0, 0))
block_bottom_right = Rectangle(Vector2(SCREEN_WIDTH - BW, SCREEN_HEIGHT - BH), BW, BH, color=(0, 0, 0))
block_top          = Rectangle(Vector2(0,-10),SCREEN_WIDTH,10,color=WALL_COLOR)
block_bottom       = Rectangle(Vector2(0, SCREEN_HEIGHT),SCREEN_WIDTH, 10, color=WALL_COLOR)


