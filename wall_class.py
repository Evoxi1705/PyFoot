import pygame
from base_classes import *
from constants import WALL_COLOR

class Wall(StaticObject):
    def __init__(self, pos, width, height, color=WALL_COLOR):
        super().__init__(pos, height, width)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos.x, self.pos.y, self.width, self.height))
        


